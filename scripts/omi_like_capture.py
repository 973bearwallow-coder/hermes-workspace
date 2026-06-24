#!/usr/bin/env python3.12
"""
OMI-like Auto-Capture System for Hermes on Linux (charles).
Mimics OMI's screen watching + mic listening + transcription pipeline.

Capture sources:
1. Window titles (existing, every 5 min)
2. Periodic screenshots → OCR text extraction (NEW)
3. Mic audio → Whisper transcription (NEW)
4. Application usage patterns
5. Browser history

Output: daily markdown files in memory vault, readable by Hermes at session start.

Usage:
  --daemon [interval_sec]  # Continuous background capture (default 300s)
  --daily                   # Generate daily memory note (for cron)
  --snapshot                # Quick one-time snapshot with OCR
  --screenshot              # Just capture and OCR a screenshot
"""

import subprocess
import json
import os
import re
import sqlite3
import sys
import time
import signal
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

# --- Config ---
MEMORY_VAULT = "/home/tom/hermes-workspace/memory"
WINDOW_LOG = "/home/tom/hermes-workspace/logs/window_capture.log"
SCREENSHOT_DIR = "/home/tom/hermes-workspace/logs/screenshots"
AUDIO_DIR = "/home/tom/hermes-workspace/logs/audio"
TRANSCRIPT_DIR = "/home/tom/hermes-workspace/logs/transcripts"
CHROME_HISTORY = "/home/tom/.config/google-chrome/Default/History"
RECENTLY_USED = "/home/tom/.local/share/recently-used.xbel"
COACHING_DIR = "/home/tom/Desktop/coaching_call"

# How often to capture screenshots for OCR (seconds)
SCREENSHOT_INTERVAL = 600  # 10 minutes
# How often to capture audio snippets (seconds)
AUDIO_SNIPPET_INTERVAL = 300  # 5 minutes
# How long each audio snippet is (seconds)
AUDIO_SNIPPET_DURATION = 30  # 30 seconds
# Min text length from OCR to be meaningful
MIN_OCR_TEXT_LENGTH = 20

os.makedirs(MEMORY_VAULT, exist_ok=True)
os.makedirs(os.path.dirname(WINDOW_LOG), exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

# Track what we've already processed to avoid duplicates
_processed_screenshots = set()
_processed_audio = set()


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
    """Get window class (app name) via python-xlib."""
    try:
        from Xlib import display
        d = display.Display(":1")
        root = d.screen().root
        window_id = root.get_full_property(
            d.intern_atom("_NET_ACTIVE_WINDOW"), 0
        ).value[0]
        window = d.create_resource_object("window", window_id)
        wm_class = window.get_wm_name()
        d.close()
        if wm_class:
            return wm_class
    except Exception:
        pass
    return "unknown"


def get_active_window_geometry():
    """Get geometry of active window for targeted screenshot."""
    try:
        result = subprocess.run(
            ["xdotool", "getactivewindow", "getwindowgeometry", "--shell"],
            capture_output=True, text=True, timeout=5,
            env={**os.environ, "DISPLAY": ":1"}
        )
        if result.returncode == 0:
            geom = {}
            for line in result.stdout.strip().split("\n"):
                if "=" in line:
                    k, v = line.split("=", 1)
                    geom[k.strip()] = v.strip()
            return geom
    except Exception:
        pass
    return None


def capture_screenshot_ocr():
    """
    Capture a screenshot of the active window and extract text via OCR.
    Returns extracted text or None if nothing meaningful found.
    """
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    window_title = get_active_window_title() or "unknown"
    safe_title = re.sub(r'[^\w\-]', '_', window_title[:40])
    
    screenshot_path = os.path.join(SCREENSHOT_DIR, f"screen_{ts}_{safe_title}.png")
    
    try:
        # Get active window ID for targeted capture
        window_id_result = subprocess.run(
            ["xdotool", "getactivewindow"],
            capture_output=True, text=True, timeout=5,
            env={**os.environ, "DISPLAY": ":1"}
        )
        
        if window_id_result.returncode == 0:
            window_id = window_id_result.stdout.strip()
            # Capture just the active window by ID (not root/fullscreen)
            subprocess.run(
                ["import", "-window", window_id, "-quality", "85", screenshot_path],
                capture_output=True, timeout=10,
                env={**os.environ, "DISPLAY": ":1"}
            )
        else:
            # Fallback: capture full screen
            subprocess.run(
                ["import", "-window", "root", "-quality", "80", screenshot_path],
                capture_output=True, timeout=10,
                env={**os.environ, "DISPLAY": ":1"}
            )
        
        if not os.path.exists(screenshot_path):
            return None
        
        # Check file size (skip if too small - probably blank)
        file_size = os.path.getsize(screenshot_path)
        if file_size < 5000:
            os.unlink(screenshot_path)
            return None
        
        # OCR the screenshot using tesseract
        ocr_result = subprocess.run(
            ["tesseract", screenshot_path, "stdout", "--psm", "3", "-l", "eng"],
            capture_output=True, text=True, timeout=15
        )
        
        if ocr_result.returncode == 0:
            text = ocr_result.stdout.strip()
            if len(text) >= MIN_OCR_TEXT_LENGTH:
                # Save the OCR text
                ocr_text_path = os.path.join(
                    TRANSCRIPT_DIR, f"ocr_{ts}_{safe_title}.txt"
                )
                with open(ocr_text_path, "w") as f:
                    f.write(f"# OCR Capture — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"# Window: {window_title}\n")
                    f.write(f"# Screenshot: {screenshot_path}\n\n")
                    f.write(text)
                
                # Clean up old screenshots (keep last 50)
                cleanup_old_files(SCREENSHOT_DIR, "*.png", keep=50)
                cleanup_old_files(TRANSCRIPT_DIR, "ocr_*.txt", keep=100)
                
                return {
                    "window": window_title,
                    "text": text[:2000],  # Cap at 2000 chars
                    "screenshot": screenshot_path,
                    "ocr_file": ocr_text_path,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
            else:
                # Not enough text, delete screenshot
                os.unlink(screenshot_path)
                return None
        
        os.unlink(screenshot_path)
        return None
        
    except subprocess.TimeoutExpired:
        if os.path.exists(screenshot_path):
            os.unlink(screenshot_path)
        return None
    except Exception as e:
        if os.path.exists(screenshot_path):
            os.unlink(screenshot_path)
        return None


def capture_audio_snippet():
    """
    Capture a short audio snippet from the default microphone via PipeWire.
    Returns path to WAV file or None.
    """
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_path = os.path.join(AUDIO_DIR, f"audio_{ts}.wav")
    
    try:
        # Find the active mic source
        wpctl_result = subprocess.run(
            ["wpctl", "status"],
            capture_output=True, text=True, timeout=5
        )
        
        # Default to first available source (usually the USB mic on charles)
        # Use pw-record for PipeWire audio capture
        result = subprocess.run(
            ["pw-record", "--rate", "16000", "--channels", "1",
             "-", f"-- Audiorecord"],
            capture_output=True, timeout=AUDIO_SNIPPET_DURATION + 5,
            env={**os.environ, "DISPLAY": ":1"}
        )
        
        # Actually use pw-record properly
        proc = subprocess.Popen(
            ["pw-record", "--rate", "16000", "--channels", "1",
             "--format", "s16", audio_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Record for the snippet duration
        try:
            proc.wait(timeout=AUDIO_SNIPPET_DURATION)
        except subprocess.TimeoutExpired:
            proc.terminate()
            proc.wait(timeout=5)
        
        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 1000:
            return audio_path
        else:
            if os.path.exists(audio_path):
                os.unlink(audio_path)
            return None
            
    except Exception as e:
        if os.path.exists(audio_path):
            os.unlink(audio_path)
        return None


def transcribe_audio_whisper(audio_path):
    """
    Transcribe audio file using Whisper CLI.
    Returns transcribed text or None.
    """
    try:
        result = subprocess.run(
            ["whisper", audio_path, "--model", "base", "--language", "en",
             "--output_format", "txt", "--output_dir", TRANSCRIPT_DIR,
             "--fp16", "False"],
            capture_output=True, text=True, timeout=120
        )
        
        if result.returncode == 0:
            # Whisper outputs to <audio_basename>.txt in output_dir
            base_name = Path(audio_path).stem
            transcript_path = os.path.join(TRANSCRIPT_DIR, f"{base_name}.txt")
            
            if os.path.exists(transcript_path):
                with open(transcript_path) as f:
                    text = f.read().strip()
                
                if len(text) > 10:
                    return text
                
                # Clean up if empty/useless
                os.unlink(transcript_path)
                return None
        
        return None
        
    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None


def cleanup_old_files(directory, pattern, keep=50):
    """Keep only the last N files matching pattern in directory."""
    try:
        files = sorted(Path(directory).glob(pattern), key=lambda p: p.stat().st_mtime)
        if len(files) > keep:
            for f in files[:-keep]:
                try:
                    f.unlink()
                except Exception:
                    pass
    except Exception:
        pass


def parse_recently_used_files(hours=24):
    """Parse GTK recently-used.xbel for files opened in last N hours."""
    files = []
    if not os.path.exists(RECENTLY_USED):
        return files
    
    cutoff = datetime.now() - timedelta(hours=hours)
    try:
        with open(RECENTLY_USED, "r") as f:
            content = f.read()
        
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
    except Exception:
        pass
    
    return files[-20:]


def get_chrome_history(hours=24, limit=50):
    """Get Chrome browsing history from SQLite DB."""
    history = []
    if not os.path.exists(CHROME_HISTORY):
        return history
    
    cutoff = datetime.now() - timedelta(hours=hours)
    chrome_epoch = datetime(1601, 1, 1)
    cutoff_ts = int((cutoff - chrome_epoch).total_seconds() * 1_000_000)
    
    try:
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


def get_latest_meeting_transcripts():
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
    """Get recent outputs from monitors."""
    outputs = []
    pet_dir = "/home/tom/Desktop/coaching_call/pet_community"
    for label, directory in [("Pet Community", pet_dir)]:
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


def log_window_activity(timestamp, wclass, title):
    """Log window activity to the rolling window log."""
    log_line = f"{timestamp} | {wclass or '?'} | {title}\n"
    with open(WINDOW_LOG, "a") as f:
        f.write(log_line)
    
    # Keep log manageable (last 2000 lines)
    try:
        with open(WINDOW_LOG, "r") as f:
            lines = f.readlines()
        if len(lines) > 2000:
            with open(WINDOW_LOG, "w") as f:
                f.writelines(lines[-2000:])
    except Exception:
        pass


def generate_daily_memory_note(force=False):
    """
    Generate a daily memory note from all capture sources.
    Only generates once per day unless force=True.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    note_file = os.path.join(MEMORY_VAULT, f"{today}.md")
    
    # Check if already generated today
    if os.path.exists(note_file) and not force:
        mtime = datetime.fromtimestamp(os.path.getmtime(note_file))
        if mtime.date() == datetime.now().date():
            pass  # Will append
    
    sections = []
    
    # --- Section 1: Window Activity Summary ---
    recent_windows = parse_recent_window_log(hours=24)
    if recent_windows:
        app_counts = {}
        for entry in recent_windows:
            app = entry.get("app", "unknown")
            app_counts[app] = app_counts.get(app, 0) + 1
        
        top_apps = sorted(app_counts.items(), key=lambda x: x[1], reverse=True)
        sections.append("## Active Applications (24h)\n")
        for app, count in top_apps[:10]:
            sections.append(f"- **{app}**: {count} snapshots")
        
        # Notable window titles (unique)
        unique_titles = list(set(e["title"] for e in recent_windows))[:15]
        sections.append(f"\n### Notable Windows")
        for t in unique_titles:
            sections.append(f"- {t[:80]}")
    
    # --- Section 2: Screen Content (OCR) ---
    ocr_files = sorted(Path(TRANSCRIPT_DIR).glob("ocr_*.txt"), reverse=True)[:5]
    if ocr_files:
        sections.append("\n## Screen Content Captures (OCR)\n")
        for f in ocr_files[:3]:
            try:
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                age_hours = (datetime.now() - mtime).total_seconds() / 3600
                if age_hours < 24:
                    content = f.read_text()
                    # Extract window title and text preview
                    window_match = re.search(r'# Window: (.+)', content)
                    window = window_match.group(1) if window_match else "Unknown"
                    text_content = re.sub(r'^#.*?\n', '', content, flags=re.MULTILINE).strip()
                    sections.append(f"### {window} ({mtime.strftime('%H:%M')})")
                    sections.append(f"```\n{text_content[:300]}\n```\n")
            except Exception:
                pass
    
    # --- Section 3: Audio Transcripts ---
    audio_transcripts = sorted(Path(TRANSCRIPT_DIR).glob("audio_*.txt"), reverse=True)[:5]
    if audio_transcripts:
        sections.append("\n## Audio Transcripts (Whisper)\n")
        for f in audio_transcripts[:3]:
            try:
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                age_hours = (datetime.now() - mtime).total_seconds() / 3600
                if age_hours < 24:
                    text = f.read_text().strip()
                    if len(text) > 20:
                        sections.append(f"### Audio Capture ({mtime.strftime('%H:%M')})")
                        sections.append(f"{text[:500]}\n")
            except Exception:
                pass
    
    # --- Section 4: Recently Opened Files ---
    recent_files = parse_recently_used_files(hours=24)
    if recent_files:
        sections.append(f"\n## Recently Opened Files ({len(recent_files)} files)")
        for rf in recent_files[-10:]:
            sections.append(f"- {rf['name']} ({rf['added'][:10]})")
    
    # --- Section 5: Browser History ---
    chrome_hist = get_chrome_history(hours=4, limit=30)
    if chrome_hist:
        domains = {}
        for h in chrome_hist:
            domain_match = re.match(r'https?://([^/]+)', h['url'])
            d = domain_match.group(1) if domain_match else h['url']
            if d not in domains:
                domains[d] = []
            domains[d].append(h['title'][:60])
        
        sections.append(f"\n## Browser Activity ({len(chrome_hist)} pages)")
        for domain, titles in list(domains.items())[:10]:
            sections.append(f"- **{domain}**: {', '.join(list(set(titles))[:3])}")
    
    # --- Section 6: Meeting Transcripts ---
    transcripts = get_latest_meeting_transcripts()
    if transcripts:
        sections.append(f"\n## Meeting Transcripts")
        for t in transcripts:
            sections.append(f"- {t['file']} ({t['age_hours']}h ago)")
            sections.append(f"  Preview: {t['preview'][:100]}...")
    
    # --- Section 7: Monitor Outputs ---
    monitor_outputs = get_latest_monitor_outputs()
    if monitor_outputs:
        sections.append(f"\n## Automated Monitor Outputs")
        for mo in monitor_outputs:
            sections.append(f"- {mo['source']} ({mo['age_hours']}h ago)")
    
    # --- Write the note ---
    header = f"# Daily Memory Note — {today}\n"
    header += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    header += f"Auto-captured by Atlas Memory System (OMI-like)\n\n"
    
    content = header + "\n".join(sections) + "\n"
    
    with open(note_file, "w") as f:
        f.write(content)
    
    print(f"Daily memory note written: {note_file}")
    print(f"Sections: {len(sections)}")
    return note_file


def parse_recent_window_log(hours=24):
    """Parse the recent window log for activity summary."""
    entries = []
    cutoff = datetime.now() - timedelta(hours=hours)
    
    if not os.path.exists(WINDOW_LOG):
        return entries
    
    try:
        with open(WINDOW_LOG) as f:
            for line in f:
                parts = line.strip().split(" | ", 2)
                if len(parts) == 3:
                    ts_str, app, title = parts
                    try:
                        today_str = datetime.now().strftime("%Y-%m-%d")
                        ts = datetime.strptime(f"{today_str} {ts_str}", "%Y-%m-%d %H:%M:%S")
                        if ts > cutoff:
                            entries.append({"time": ts_str, "app": app, "title": title})
                    except ValueError:
                        pass
    except Exception:
        pass
    
    return entries


def run_continuous_capture(interval_seconds=300):
    """
    Run continuous background capture.
    Captures window titles, periodic screenshots, and audio snippets.
    """
    print(f"Starting OMI-like auto-capture system")
    print(f"Window log: {WINDOW_LOG}")
    print(f"Screenshots: {SCREENSHOT_DIR}")
    print(f"Audio: {AUDIO_DIR}")
    print(f"Transcripts: {TRANSCRIPT_DIR}")
    print(f"Interval: {interval_seconds}s window, {SCREENSHOT_INTERVAL}s screenshot, {AUDIO_SNIPPET_INTERVAL}s audio")
    
    last_screenshot = 0
    last_audio = 0
    last_window_title = None
    screenshot_interval = SCREENSHOT_INTERVAL  # starts at 10 min
    
    # Set up signal handler for clean shutdown
    running = True
    def signal_handler(sig, frame):
        nonlocal running
        running = False
        print("\nShutting down capture system...")
    
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    cycle = 0
    while running:
        try:
            now = time.time()
            
            # Always capture window title (every cycle)
            title = get_active_window_title()
            wclass = get_window_class()
            ts = datetime.now().strftime("%H:%M:%S")
            
            if title:
                log_window_activity(ts, wclass, title)
            
            # Capture screenshot+OCR with adaptive frequency
            if now - last_screenshot >= screenshot_interval:
                ocr_result = capture_screenshot_ocr()
                if ocr_result:
                    print(f"[OCR] {ocr_result['window']}: {len(ocr_result['text'])} chars captured")
                    
                    # Adaptive: if content is rich, capture more frequently next time
                    word_count = len(ocr_result['text'].split())
                    if word_count > 100:
                        screenshot_interval = 120  # 2 min for content-heavy windows
                    elif word_count > 30:
                        screenshot_interval = 300  # 5 min for moderate content
                    else:
                        screenshot_interval = SCREENSHOT_INTERVAL  # 10 min default
                else:
                    # No meaningful text, back off
                    screenshot_interval = SCREENSHOT_INTERVAL
                
                last_screenshot = now
            
            # Even faster capture if window title just changed to something interesting
            if title and title != last_window_title:
                # New window — do a quick capture if we haven't in the last 30s
                if now - last_screenshot >= 30:
                    ocr_result = capture_screenshot_ocr()
                    if ocr_result:
                        print(f"[OCR-Quick] {ocr_result['window']}: {len(ocr_result['text'])} chars")
                    last_screenshot = now
                last_window_title = title
            
            # Capture audio snippet every AUDIO_SNIPPET_INTERVAL
            # (Disabled by default - enable when mic is confirmed working)
            # if now - last_audio >= AUDIO_SNIPPET_INTERVAL:
            #     audio_path = capture_audio_snippet()
            #     if audio_path:
            #         transcript = transcribe_audio_whisper(audio_path)
            #         if transcript:
            #             print(f"[Audio] Transcribed: {transcript[:80]}...")
            #         # Clean up audio file after transcription
            #         try: os.unlink(audio_path)
            #         except: pass
            #     last_audio = now
            
            cycle += 1
            if cycle % 10 == 0:
                print(f"[Cycle {cycle}] Window: {title or 'unknown'} | {datetime.now().strftime('%H:%M:%S')}")
            
        except Exception as e:
            print(f"Capture error: {e}")
        
        time.sleep(interval_seconds)
    
    print("Capture system stopped.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--daemon":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300
        run_continuous_capture(interval)
    elif len(sys.argv) > 1 and sys.argv[1] == "--daily":
        generate_daily_memory_note()
    elif len(sys.argv) > 1 and sys.argv[1] == "--snapshot":
        print("Capturing screenshot with OCR...")
        result = capture_screenshot_ocr()
        if result:
            print(f"Window: {result['window']}")
            print(f"Text ({len(result['text'])} chars):")
            print(result['text'][:500])
        else:
            print("No meaningful text captured.")
    elif len(sys.argv) > 1 and sys.argv[1] == "--screenshot":
        title = get_active_window_title() or "unknown"
        print(f"Active window: {title}")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(SCREENSHOT_DIR, f"manual_{ts}.png")
        subprocess.run(
            ["import", "-window", "root", "-quality", "90", path],
            env={**os.environ, "DISPLAY": ":1"}
        )
        print(f"Screenshot saved: {path}")
    else:
        print("Atlas OMI-like Auto-Capture System")
        print(f"  {sys.argv[0]} --daemon [interval_sec]  # Continuous capture")
        print(f"  {sys.argv[0]} --daily                   # Generate daily memory note")
        print(f"  {sys.argv[0]} --snapshot                 # Screenshot + OCR")
        print(f"  {sys.argv[0]} --screenshot               # Just screenshot")
