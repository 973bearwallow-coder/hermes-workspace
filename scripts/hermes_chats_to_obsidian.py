#!/usr/bin/env python3
"""
Auto-save Hermes chat sessions to Obsidian vault.
Runs as a cron job — exports recent Hermes session summaries to daily markdown files.
"""

import json
import os
import sqlite3
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

OBSIDIAN_VAULT = Path.home() / "Documents" / "ObsidianVault"
HERMES_HOME = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
SESSIONS_DB = Path(os.environ.get("HERMES_STATE_DB", HERMES_HOME / "state.db"))
OUTPUT_DIR = OBSIDIAN_VAULT / "Hermes_Logs"

def ensure_dirs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def get_recent_sessions(hours=24):
    """Get sessions from the Hermes state.db modified in the last N hours."""
    if not SESSIONS_DB.exists():
        return []
    
    sessions = []
    try:
        conn = sqlite3.connect(str(SESSIONS_DB))
        # started_at is a REAL (unix timestamp), filter by started_at
        cutoff = (datetime.now() - timedelta(hours=hours)).timestamp()
        rows = conn.execute(
            """SELECT id, title, started_at, ended_at, message_count 
               FROM sessions 
               WHERE started_at > ? AND archived = 0
               ORDER BY started_at DESC""",
            (cutoff,)
        ).fetchall()
        for row in rows:
            started = datetime.fromtimestamp(row[2]).strftime("%Y-%m-%d %H:%M") if row[2] else "Unknown"
            ended = datetime.fromtimestamp(row[3]).strftime("%Y-%m-%d %H:%M") if row[3] else "Active"
            sessions.append({
                "id": row[0],
                "title": row[1] or "Untitled",
                "created": started,
                "updated": ended,
                "messages": row[4] or 0,
            })
        conn.close()
    except Exception as e:
        print(f"Warning: Could not read sessions DB: {e}")
    
    return sessions

def get_session_messages(session_id, limit=50):
    """Get messages from a specific session."""
    messages = []
    try:
        conn = sqlite3.connect(str(SESSIONS_DB))
        rows = conn.execute(
            """SELECT role, content, timestamp 
               FROM messages 
               WHERE session_id = ? AND active = 1
               ORDER BY timestamp ASC 
               LIMIT ?""",
            (session_id, limit)
        ).fetchall()
        for row in rows:
            ts = datetime.fromtimestamp(row[2]).strftime("%H:%M") if row[2] else ""
            messages.append({
                "role": row[0],
                "content": row[1],
                "time": ts,
            })
        conn.close()
    except Exception as e:
        print(f"Warning: Could not read messages for session {session_id}: {e}")
    
    return messages

def format_session_markdown(session, messages):
    """Format a session as Obsidian markdown."""
    now = datetime.now()
    lines = [
        f"# Hermes Chat: {session['title']}",
        "",
        f"- **Date:** {now.strftime('%Y-%m-%d')}",
        f"- **Session ID:** {session['id']}",
        f"- **Messages:** {len(messages)}",
        f"- **Exported:** {now.strftime('%H:%M:%S')}",
        "",
        "---",
        "",
    ]
    
    for msg in messages:
        role = msg["role"].capitalize()
        time_str = msg["time"][:16] if msg["time"] else ""
        lines.append(f"### {role} ({time_str})")
        lines.append("")
        content = msg["content"] or ""
        # Truncate very long messages
        if len(content) > 2000:
            content = content[:2000] + "\n\n... [truncated]"
        lines.append(content)
        lines.append("")
        lines.append("---")
        lines.append("")
    
    return "\n".join(lines)

def save_to_obsidian(date_str, content):
    """Save markdown to Obsidian vault."""
    filename = OUTPUT_DIR / f"hermes_chats_{date_str}.md"
    
    # If file exists, append; otherwise create new
    if filename.exists():
        existing = filename.read_text()
        # Check if this is a new export for the same day
        separator = f"\n\n---\n\n## Export Batch: {datetime.now().strftime('%H:%M:%S')}\n\n"
        with open(filename, "a") as f:
            f.write(separator + content)
    else:
        header = f"# Hermes Chat Log — {date_str}\n\nAuto-exported from Hermes sessions.\n\n---\n\n"
        filename.write_text(header + content)
    
    print(f"  Saved to: {filename}")
    return filename

def main():
    ensure_dirs()
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    
    print(f"[{now.strftime('%H:%M:%S')}] Exporting Hermes sessions to Obsidian...")
    
    # Get sessions from last 24 hours
    sessions = get_recent_sessions(hours=24)
    
    if not sessions:
        print("  No recent sessions found. Nothing to export.")
        return
    
    print(f"  Found {len(sessions)} recent session(s)")
    
    all_content = []
    for session in sessions:
        print(f"  Processing: {session['title'][:50]}")
        messages = get_session_messages(session["id"])
        if messages:
            md = format_session_markdown(session, messages)
            all_content.append(md)
    
    if all_content:
        combined = "\n\n".join(all_content)
        filepath = save_to_obsidian(date_str, combined)
        print(f"  ✅ Exported {len(sessions)} session(s) to {filepath.name}")
    else:
        print("  No messages found in recent sessions.")

if __name__ == "__main__":
    main()
