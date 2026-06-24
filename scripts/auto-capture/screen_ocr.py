#!/usr/bin/env python3
"""
Auto-Capture: Screen OCR → Obsidian
Takes periodic screenshots, extracts text via OCR, and saves to Obsidian.
Only saves when meaningful text changes are detected (avoids duplicates).

Usage: python3 screen_ocr.py [--interval 120] [--min-chars 50]
  --interval: seconds between screenshots (default: 120 = 2 min)
  --min-chars: minimum characters to consider worth saving (default: 50)
"""

import argparse
import hashlib
import os
import subprocess
import sys
import time
import tempfile
from datetime import datetime
from pathlib import Path

try:
    import pytesseract
    from PIL import Image
except ImportError:
    print("[ERROR] pytesseract/Pillow not installed. Run: uv pip install pytesseract Pillow", file=sys.stderr)
    sys.exit(1)

# Configuration
OBSIDIAN_VAULT = Path.home() / "Documents" / "ObsidianVault"
CAPTURE_DIR = Path.home() / "hermes-workspace" / "scripts" / "auto-capture"
STATE_FILE = CAPTURE_DIR / "screen_ocr_state.json"
SCREEN_NOTES_DIR = OBSIDIAN_VAULT / "Captures" / "Screen"

# Ensure directories exist
SCREEN_NOTES_DIR.mkdir(parents=True, exist_ok=True)

# Minimum time between saves to the same note (seconds)
MIN_SAVE_INTERVAL = 300  # 5 minutes


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def get_daily_note_path():
    today = datetime.now().strftime("%Y-%m-%d")
    return SCREEN_NOTES_DIR / f"{today}.md"


def take_screenshot():
    """Take a screenshot using ImageMagick import. Returns PIL Image or None."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        result = subprocess.run(
            ["import", "-window", "root", tmp_path],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            print(f"[ERROR] Screenshot failed: {result.stderr}", file=sys.stderr)
            return None
        
        img = Image.open(tmp_path)
        return img
    except Exception as e:
        print(f"[ERROR] Screenshot exception: {e}", file=sys.stderr)
        return None
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass


def ocr_image(img):
    """Extract text from a PIL Image using Tesseract OCR."""
    try:
        # Resize if too large for faster OCR
        max_dim = 2000
        if max(img.size) > max_dim:
            ratio = max_dim / max(img.size)
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size, Image.LANCZOS)
        
        text = pytesseract.image_to_string(img).strip()
        return text
    except Exception as e:
        print(f"[ERROR] OCR failed: {e}", file=sys.stderr)
        return ""


def is_meaningful_text(text, min_chars=50):
    """Check if extracted text is meaningful enough to save."""
    if len(text) < min_chars:
        return False
    # Check it's not just UI chrome (menu bars, etc.)
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if len(lines) < 3:
        return False
    return True


def text_hash(text):
    """Get a hash of the text for change detection."""
    return hashlib.md5(text.encode()).hexdigest()


def load_state():
    """Load the OCR state."""
    if STATE_FILE.exists():
        import json
        return json.loads(STATE_FILE.read_text())
    return {"last_hash": "", "last_save_time": 0}


def save_state(state):
    """Save the OCR state."""
    import json
    STATE_FILE.write_text(json.dumps(state, indent=2))


def save_to_obsidian(text, timestamp):
    """Append OCR text to today's daily note."""
    note_path = get_daily_note_path()
    
    entry = f"\n## 🖥️ Screen Capture — {timestamp}\n\n```\n{text}\n```\n"
    
    if not note_path.exists():
        note_path.write_text(f"# Screen Captures — {datetime.now().strftime('%Y-%m-%d')}\n")
    
    with open(note_path, "a") as f:
        f.write(entry)
    
    print(f"[OK] Saved to {note_path}")


def main():
    parser = argparse.ArgumentParser(description="Screen OCR → Obsidian auto-capture")
    parser.add_argument("--interval", type=int, default=120, help="Seconds between screenshots")
    parser.add_argument("--min-chars", type=int, default=50, help="Minimum characters to save")
    parser.add_argument("--once", action="store_true", help="Capture once and exit")
    args = parser.parse_args()

    print(f"[INFO] Screen OCR → Obsidian starting...")
    print(f"[INFO] Interval: {args.interval}s, Min chars: {args.min_chars}")
    print(f"[INFO] Obsidian notes: {SCREEN_NOTES_DIR}")
    print(f"[INFO] Press Ctrl+C to stop\n")

    state = load_state()
    running = True

    def signal_handler(sig, frame):
        nonlocal running
        print("\n[INFO] Shutting down...")
        running = False

    import signal
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while running:
        timestamp = get_timestamp()
        print(f"[{timestamp}] Capturing screen...")
        
        img = take_screenshot()
        if img is None:
            print("[WARN] Screenshot failed, retrying next interval...")
            time.sleep(args.interval)
            continue
        
        text = ocr_image(img)
        
        if is_meaningful_text(text, args.min_chars):
            current_hash = text_hash(text)
            now = time.time()
            
            # Only save if text changed and enough time has passed
            if (current_hash != state["last_hash"] and 
                now - state["last_save_time"] > MIN_SAVE_INTERVAL):
                print(f"[{timestamp}] OCR: {len(text)} chars, saving...")
                save_to_obsidian(text, timestamp)
                state["last_hash"] = current_hash
                state["last_save_time"] = now
                save_state(state)
            else:
                if current_hash == state["last_hash"]:
                    print(f"[{timestamp}] No change detected, skipping...")
                else:
                    print(f"[{timestamp}] Too soon since last save, skipping...")
        else:
            print(f"[{timestamp}] Text too short ({len(text)} chars), skipping...")
        
        if args.once:
            break
        
        print(f"[INFO] Next capture in {args.interval}s...")
        for _ in range(args.interval):
            if not running:
                break
            time.sleep(1)

    print("[INFO] Screen OCR stopped.")


if __name__ == "__main__":
    main()
