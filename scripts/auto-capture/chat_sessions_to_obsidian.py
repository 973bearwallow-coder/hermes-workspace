#!/usr/bin/env python3
"""
Auto-Capture: Hermes Chat → Obsidian Daily Notes
Watches Hermes session files and appends conversation summaries to Obsidian daily notes.

Usage: python3 chat_sessions_to_obsidian.py [--watch] [--interval 300]
  --watch: continuously watch for new sessions (default: one-shot)
  --interval: seconds between checks in watch mode (default: 300 = 5 min)
"""

import argparse
import json
import os
import sys
import time
import hashlib
from datetime import datetime
from pathlib import Path

# Configuration
OBSIDIAN_VAULT = Path.home() / "Documents" / "ObsidianVault"
SESSIONS_DIR = Path.home() / ".hermes" / "sessions"
STATE_FILE = Path.home() / "hermes-workspace" / "scripts" / "auto-capture" / "chat_sync_state.json"
CHAT_NOTES_DIR = OBSIDIAN_VAULT / "Captures" / "Chat"

# Ensure directories exist
CHAT_NOTES_DIR.mkdir(parents=True, exist_ok=True)


def get_session_files():
    """Get all session JSONL files sorted by modification time."""
    files = sorted(SESSIONS_DIR.glob("*.jsonl"), key=lambda f: f.stat().st_mtime)
    return files


def get_file_hash(filepath):
    """Get MD5 hash of a file for change detection."""
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_session(filepath):
    """Parse a session JSONL file and extract conversation messages."""
    messages = []
    session_id = filepath.stem
    
    with open(filepath, "r") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                role = entry.get("role")
                if role == "session_meta":
                    continue
                if role in ("user", "assistant"):
                    content = entry.get("content", "")
                    if isinstance(content, list):
                        # Handle multi-modal content (text + images)
                        text_parts = []
                        for part in content:
                            if isinstance(part, dict) and part.get("type") == "text":
                                text_parts.append(part.get("text", ""))
                        content = " ".join(text_parts)
                    if content and content.strip():
                        messages.append({
                            "role": role,
                            "content": content.strip()[:500]  # Truncate long messages
                        })
            except (json.JSONDecodeError, KeyError):
                continue
    
    return {"session_id": session_id, "messages": messages}


def session_to_markdown(session_data, filepath):
    """Convert session data to Obsidian markdown."""
    session_id = session_data["session_id"]
    messages = session_data["messages"]
    
    if not messages:
        return None
    
    # Extract date from session filename (format: YYYYMMDD_HHMMSS_hash)
    try:
        date_str = session_id[:8]
        date_obj = datetime.strptime(date_str, "%Y%m%d")
        display_date = date_obj.strftime("%Y-%m-%d")
        time_str = session_id[9:13]
        display_time = f"{time_str[:2]}:{time_str[2:]}"
    except (ValueError, IndexError):
        display_date = datetime.now().strftime("%Y-%m-%d")
        display_time = "unknown"
    
    # Build markdown
    lines = [f"## 💬 Chat Session — {display_date} {display_time}", ""]
    lines.append(f"*Session: {session_id}*")
    lines.append(f"*Messages: {len(messages)}*")
    lines.append("")
    
    for msg in messages:
        role_icon = "👤" if msg["role"] == "user" else "🤖"
        lines.append(f"### {role_icon} {msg['role'].title()}")
        lines.append("")
        lines.append(msg["content"])
        lines.append("")
    
    lines.append("---")
    lines.append("")
    
    return "\n".join(lines)


def save_to_obsidian(markdown: str, date_str: str):
    """Append chat summary to the appropriate daily note."""
    note_path = CHAT_NOTES_DIR / f"{date_str}.md"
    
    if not note_path.exists():
        note_path.write_text(f"# Chat Sessions — {date_str}\n")
    
    with open(note_path, "a") as f:
        f.write(markdown)
    
    print(f"[OK] Saved chat to {note_path}")


def load_state():
    """Load the sync state (tracking which files have been processed)."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"processed": {}}


def save_state(state):
    """Save the sync state."""
    STATE_FILE.write_text(json.dumps(state, indent=2))


def process_sessions(state, force_all=False):
    """Process new or changed session files."""
    sessions = get_session_files()
    new_count = 0
    
    for session_file in sessions:
        file_key = str(session_file)
        current_hash = get_file_hash(session_file)
        
        # Skip if already processed and not changed
        if not force_all and file_key in state["processed"]:
            if state["processed"][file_key] == current_hash:
                continue
        
        # Parse and convert
        session_data = parse_session(session_file)
        markdown = session_to_markdown(session_data, session_file)
        
        if markdown:
            try:
                date_str = session_file.stem[:8]
                date_obj = datetime.strptime(date_str, "%Y%m%d")
                display_date = date_obj.strftime("%Y-%m-%d")
            except ValueError:
                display_date = datetime.now().strftime("%Y-%m-%d")
            
            save_to_obsidian(markdown, display_date)
            new_count += 1
        
        # Update state
        state["processed"][file_key] = current_hash
    
    save_state(state)
    return new_count


def main():
    parser = argparse.ArgumentParser(description="Sync Hermes chat sessions to Obsidian")
    parser.add_argument("--watch", action="store_true", help="Continuously watch for new sessions")
    parser.add_argument("--interval", type=int, default=300, help="Seconds between checks in watch mode")
    parser.add_argument("--force-all", action="store_true", help="Re-process all sessions")
    args = parser.parse_args()

    print(f"[INFO] Hermes Chat → Obsidian starting...")
    print(f"[INFO] Sessions dir: {SESSIONS_DIR}")
    print(f"[INFO] Obsidian notes: {CHAT_NOTES_DIR}")
    
    state = load_state()
    
    if args.force_all:
        state["processed"] = {}
    
    if args.watch:
        print(f"[INFO] Watch mode: checking every {args.interval}s (Ctrl+C to stop)\n")
        try:
            while True:
                new = process_sessions(state)
                if new:
                    print(f"[INFO] Synced {new} new/updated session(s)")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n[INFO] Stopped.")
    else:
        new = process_sessions(state, force_all=args.force_all)
        print(f"[INFO] Synced {new} session(s)")
        print("[INFO] Done.")


if __name__ == "__main__":
    main()
