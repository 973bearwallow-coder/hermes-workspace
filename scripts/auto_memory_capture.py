#!/usr/bin/env python3.12
"""
Auto-Memory Capture System for Atlas/Hermes.
Captures work context automatically and stores as markdown in memory vault.

Mimics OMI's approach but runs locally on Linux (charles).
Lightweight alternative to OMI desktop (macOS-only) + cloud backend.

Capture sources:
1. Active window titles (what Tom is working on)
2. Recently opened files (from GTK recently-used.xbel)
3. Browser history (Chrome — what sites were visited)
4. Meeting transcripts (from our coaching_call pipeline)
5. Cron job outputs (what monitors found)

Output: daily markdown files in memory vault, readable by Hermes at session start.
"""

import subprocess
import json
import os
import re
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path

# --- Config ---
MEMORY_VAULT = "/home/tom/hermes-workspace/memory"
DAILY_NOTES_DIR = MEMORY_VAULT
WINDOW_LOG = "/home/tom/hermes-workspace/logs/window_capture.log"
COACHING_DIR = "/home/tom/Desktop/coaching_call"
PET_COMMUNITY_DIR = "/home/tom/Desktop/coaching_call/pet_community"
CHROME_HISTORY = "/home/tom/.config/google-chrome/Default/History"
RECENTLY_USED = "/home/tom/.local/share/recently-used.xbel"

os.makedirs(MEMORY_VAULT, exist_ok=True)
os.makedirs(os.path.dirname(WINDOW_LOG), exist_ok=True)


def get_active_window_title():
    """Get current active window title via python-xlib."""
    try:
        from Xlib import display
        d = display.Display(":1")
        root = d.screen().root
        window_id = root.get_full_property(
            d.intern_atom("_NET_ACTIVE_WINDOW"), 0
        ).value[0]
        window = d.create_resource_object("window", window_id)
        # Try _NET_WM_NAME first (UTF-8), fall back to WM_NAME
        try:
            net_name = window.get_full_property(
                d.intern_atom("_NET_WM_NAME"),
                d.intern_atom("UTF8_STRING")
            )
            if net_name and net_name.value:
                title = net_name.value.decode("utf-8", errors="replace")
                d.close()
                return title
        except Exception:
            pass
        title = window.get_wm_name()
        d.close()
        return title if title else None
    except Exception:
        pass
    return None


def get_window_class():
    """Get window class (app name) using python-xlib for better reliability."""
    try:
        from Xlib import display
        d = display.Display(":1")
        root = d.screen().root
        window_id = root.get_full_property(
            d.intern_atom("_NET_ACTIVE_WINDOW"), 0
        ).value[0]
        window = d.create_resource_object("window", window_id)
        wm_class = window.get_wm_class()
        d.close()
        if wm_class:
            return wm_class[1]  # Return the class name (e.g., "Firefox", "Chrome")
    except Exception:
        pass
    return "unknown"


def capture_windows_snapshot(sample_interval=30, samples=10):
    """
    Take multiple window snapshots over time to track what was being worked on.
    Returns a list of (timestamp, window_title, window_class) tuples.
    """
    snapshots = []
    for i in range(samples):
        title = get_active_window_title()
        wclass = get_window_class()
        if title:
            snapshots.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "title": title,
                "app": wclass or "unknown"
            })
        if i < samples - 1:
            time.sleep(sample_interval)
    return snapshots


def parse_recently_used_files(hours=24):
    """Parse GTK recently-used.xbel for files opened in last N hours."""
    files = []
    if not os.path.exists(RECENTLY_USED):
        return files

    cutoff = datetime.now() - timedelta(hours=hours)
    try:
        with open(RECENTLY_USED, "r") as f:
            content = f.read()

        # Parse xbel entries
        entries = re.findall(
            r'<bookmark href="file://([^"]+)" added="([^"]+)"',
            content
        )
        for filepath, added_str in entries:
            try:
                added_dt = datetime.fromisoformat(added_str.replace("Z", "+00:00"))
                if added_dt.replace(tzinfo=None) > cutoff:
                    files.append({
                        "file": filepath,
                        "added": added_str,
                        "name": os.path.basename(filepath)
                    })
            except ValueError:
                pass
    except Exception as e:
        pass

    return files[-20:]  # Last 20 files


def get_chrome_history(hours=24, limit=50):
    """Get Chrome browsing history from SQLite DB."""
    history = []
    if not os.path.exists(CHROME_HISTORY):
        return history

    cutoff = datetime.now() - timedelta(hours=hours)
    # Chrome timestamp is microseconds since 1601-01-01
    chrome_epoch = datetime(1601, 1, 1)
    cutoff_ts = int((cutoff - chrome_epoch).total_seconds() * 1_000_000)

    try:
        # Copy DB first (Chrome may have it locked)
        tmp_db = "/tmp/chrome_history_copy.db"
        shutil_copy = subprocess.run(
            ["cp", CHROME_HISTORY, tmp_db],
            capture_output=True, timeout=5
        )
        if shutil_copy.returncode != 0:
            return history

        conn = sqlite3.connect(tmp_db)
        cursor = conn.execute(
            """SELECT url, title, last_visit_time 
               FROM urls 
               WHERE last_visit_time > ? 
               ORDER BY last_visit_time DESC 
               LIMIT ?""",
            (cutoff_ts, limit)
        )
        for row in cursor:
            url, title, ts = row
            visit_dt = chrome_epoch + timedelta(microseconds=ts)
            history.append({
                "url": url,
                "title": title or url,
                "visited": visit_dt.strftime("%H:%M")
            })
        conn.close()
        os.unlink(tmp_db)
    except Exception:
        pass

    return history


def get_latest_meeting_transcript():
    """Check for any new meeting transcripts from the coaching call pipeline."""
    transcripts = []
    if os.path.exists(COACHING_DIR):
        for f in sorted(Path(COACHING_DIR).glob("transcript_*.txt"), reverse=True)[:3]:
            try:
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                age_hours = (datetime.now() - mtime).total_seconds() / 3600
                if age_hours < 48:
                    with open(f) as fh:
                        content = fh.read()[:500]
                    transcripts.append({
                        "file": str(f.name),
                        "age_hours": round(age_hours, 1),
                        "preview": content[:200]
                    })
            except Exception:
                pass
    return transcripts


def get_latest_monitor_outputs():
    """Get recent outputs from pet community monitor and other scrapes."""
    outputs = []
    for label, directory in [
        ("Pet Community", PET_COMMUNITY_DIR),
    ]:
        if os.path.exists(directory):
            files = sorted(Path(directory).glob("intelligence_*.txt"), reverse=True)[:1]
            for f in files:
                try:
                    mtime = datetime.fromtimestamp(f.stat().st_mtime)
                    age_hours = (datetime.now() - mtime).total_seconds() / 3600
                    if age_hours < 48:
                        with open(f) as fh:
                            content = fh.read()[:300]
                        outputs.append({
                            "source": label,
                            "file": f.name,
                            "age_hours": round(age_hours, 1),
                            "preview": content
                        })
                except Exception:
                    pass
    return outputs


def generate_daily_memory_note(force=False):
    """
    Generate a daily memory note from all capture sources.
    Only generates once per day unless force=True.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    note_file = os.path.join(DAILY_NOTES_DIR, f"{today}.md")

    # Check if already generated today
    if os.path.exists(note_file) and not force:
        mtime = datetime.fromtimestamp(os.path.getmtime(note_file))
        if mdate := mtime.date() == datetime.now().date():
            # Already written today, append only
            pass

    sections = []

    # --- Section 1: Window Activity Summary ---
    window_snapshots = capture_windows_snapshot(sample_interval=2, samples=5)
    if window_snapshots:
        # Count unique apps and windows
        app_counts = {}
        window_titles = []
        for snap in window_snapshots:
            app = snap.get("app", "unknown")
            app_counts[app] = app_counts.get(app, 0) + 1
            window_titles.append(snap["title"])

        top_apps = sorted(app_counts.items(), key=lambda x: x[1], reverse=True)
        sections.append(f"## Active Applications\n")
        for app, count in top_apps:
            sections.append(f"- **{app}**: {count} snapshots")
        sections.append(f"\nRecent windows: {', '.join(t[:40] for t in window_titles[:5])}")

    # --- Section 2: Recently Opened Files ---
    recent_files = parse_recently_used_files(hours=24)
    if recent_files:
        sections.append(f"\n## Recently Opened Files ({len(recent_files)} files)")
        for rf in recent_files[-10:]:
            sections.append(f"- {rf['name']} ({rf['added'][:10]})")

    # --- Section 3: Browser History (last 4 hours) ---
    chrome_hist = get_chrome_history(hours=4, limit=20)
    if chrome_hist:
        # Deduplicate by domain
        domains = {}
        for h in chrome_hist:
            domain = re.match(r'https?://([^/]+)', h['url'])
            d = domain.group(1) if domain else h['url']
            if d not in domains:
                domains[d] = []
            domains[d].append(h['title'][:60])

        sections.append(f"\n## Browser Activity ({len(chrome_hist)} pages)")
        for domain, titles in list(domains.items())[:10]:
            sections.append(f"- **{domain}**: {', '.join(list(set(titles))[:3])}")

    # --- Section 4: Meeting Transcripts ---
    transcripts = get_latest_meeting_transcript()
    if transcripts:
        sections.append(f"\n## Meeting Transcripts")
        for t in transcripts:
            sections.append(f"- {t['file']} ({t['age_hours']}h ago): {t['preview'][:100]}...")

    # --- Section 5: Monitor Outputs ---
    monitor_outputs = get_latest_monitor_outputs()
    if monitor_outputs:
        sections.append(f"\n## Automated Monitor Outputs")
        for mo in monitor_outputs:
            sections.append(f"- {mo['source']} ({mo['age_hours']}h ago): {mo['preview'][:80]}...")

    # --- Write the note ---
    header = f"# Daily Memory Note — {today}\n"
    header += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    header += f"Auto-captured by Atlas Memory System\n\n"

    content = header + "\n".join(sections) + "\n"

    with open(note_file, "w") as f:
        f.write(content)

    print(f"Daily memory note written: {note_file}")
    print(f"Sections: {len(sections)}")
    return note_file


def run_continuous_capture(interval_seconds=300):
    """
    Run continuous background capture.
    Logs window activity every N seconds to a rolling log.
    """
    print(f"Starting continuous memory capture (interval: {interval_seconds}s)")
    print(f"Window log: {WINDOW_LOG}")

    while True:
        try:
            title = get_active_window_title()
            wclass = get_window_class()
            ts = datetime.now().strftime("%H:%M:%S")

            if title:
                log_line = f"{ts} | {wclass or '?'} | {title}\n"
                with open(WINDOW_LOG, "a") as f:
                    f.write(log_line)

                # Keep log manageable (last 1000 lines)
                try:
                    with open(WINDOW_LOG, "r") as f:
                        lines = f.readlines()
                    if len(lines) > 1000:
                        with open(WINDOW_LOG, "w") as f:
                            f.writelines(lines[-1000:])
                except Exception:
                    pass

        except Exception as e:
            pass

        time.sleep(interval_seconds)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--daemon":
        # Run as continuous background process
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300
        run_continuous_capture(interval)
    elif len(sys.argv) > 1 and sys.argv[1] == "--daily":
        # Generate daily memory note (for cron)
        generate_daily_memory_note()
    elif len(sys.argv) > 1 and sys.argv[1] == "--snapshot":
        # Quick one-time window snapshot
        snaps = capture_windows_snapshot(sample_interval=5, samples=3)
        print(json.dumps(snaps, indent=2))
    else:
        print("Usage:")
        print(f"  {sys.argv[0]} --daemon [interval_sec]  # Continuous background capture")
        print(f"  {sys.argv[0]} --daily                   # Generate daily memory note")
        print(f"  {sys.argv[0]} --snapshot                 # Quick window snapshot")
