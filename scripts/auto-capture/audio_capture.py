#!/usr/bin/env python3
"""
Auto-Capture: Audio Recorder → Whisper → Obsidian
Records audio from USB mic in chunks, transcribes with Whisper,
and saves notes to the Obsidian vault.

Usage: python3 audio_capture.py [--interval 30] [--duration 60]
  --interval: seconds between recording chunks (default: 30)
  --duration: seconds to record each chunk (default: 60)
"""

import argparse
import os
import sys
import time
import subprocess
import json
import signal
import tempfile
from datetime import datetime
from pathlib import Path

# Configuration
OBSIDIAN_VAULT = Path.home() / "Documents" / "ObsidianVault"
CAPTURE_DIR = Path.home() / "hermes-workspace" / "scripts" / "auto-capture"
AUDIO_CACHE = CAPTURE_DIR / "audio_cache"
WHISPER_MODEL = "small"  # Good balance of speed/accuracy on RTX 3090
AUDIO_DEVICE = "hw:1,0"  # USB PnP Audio Device (card 1, device 0)
SAMPLE_RATE = 16000
CHANNELS = 1

# Ensure directories exist
AUDIO_CACHE.mkdir(parents=True, exist_ok=True)
(OBSIDIAN_VAULT / "Captures" / "Audio").mkdir(parents=True, exist_ok=True)


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def get_daily_note_path():
    """Get the path to today's daily note in Obsidian."""
    today = datetime.now().strftime("%Y-%m-%d")
    return OBSIDIAN_VAULT / "Captures" / "Audio" / f"{today}.md"


def record_audio(output_path: Path, duration: int) -> bool:
    """Record audio from USB mic using arecord."""
    cmd = [
        "arecord",
        "-D", AUDIO_DEVICE,
        "-f", "S16_LE",
        "-r", str(SAMPLE_RATE),
        "-c", str(CHANNELS),
        "-d", str(duration),
        str(output_path)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=duration + 10)
        if result.returncode != 0:
            print(f"[ERROR] arecord failed: {result.stderr}", file=sys.stderr)
            return False
        return True
    except subprocess.TimeoutExpired:
        print("[ERROR] arecord timed out", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[ERROR] arecord exception: {e}", file=sys.stderr)
        return False


def transcribe_audio(audio_path: Path) -> str:
    """Transcribe audio using Whisper CLI."""
    cmd = [
        "whisper",
        str(audio_path),
        "--model", WHISPER_MODEL,
        "--language", "en",
        "--output_format", "txt",
        "--output_dir", str(tempfile.gettempdir()),
        "--fp16", "True"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            print(f"[ERROR] Whisper failed: {result.stderr[-500:]}", file=sys.stderr)
            return ""
        
        # Read the output txt file
        txt_path = Path(tempfile.gettempdir()) / f"{audio_path.stem}.txt"
        if txt_path.exists():
            text = txt_path.read_text().strip()
            txt_path.unlink()  # Clean up
            return text
        return ""
    except subprocess.TimeoutExpired:
        print("[ERROR] Whisper timed out", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"[ERROR] Whisper exception: {e}", file=sys.stderr)
        return ""


def save_to_obsidian(text: str, timestamp: str):
    """Append transcribed text to today's daily note in Obsidian."""
    note_path = get_daily_note_path()
    
    # Format the entry
    entry = f"\n## 🎙️ Audio Capture — {timestamp}\n\n{text}\n"
    
    # Append to daily note (create if doesn't exist)
    if not note_path.exists():
        note_path.write_text(f"# Audio Captures — {datetime.now().strftime('%Y-%m-%d')}\n")
    
    with open(note_path, "a") as f:
        f.write(entry)
    
    print(f"[OK] Saved to {note_path}")


def cleanup_audio(audio_path: Path):
    """Remove temporary audio file."""
    try:
        if audio_path.exists():
            audio_path.unlink()
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description="Auto-capture audio → Whisper → Obsidian")
    parser.add_argument("--interval", type=int, default=30, help="Seconds between recordings")
    parser.add_argument("--duration", type=int, default=60, help="Seconds to record each chunk")
    parser.add_argument("--once", action="store_true", help="Record once and exit")
    args = parser.parse_args()

    print(f"[INFO] Auto-Capture Audio starting...")
    print(f"[INFO] Device: {AUDIO_DEVICE}, Model: {WHISPER_MODEL}")
    print(f"[INFO] Interval: {args.interval}s, Duration: {args.duration}s")
    print(f"[INFO] Obsidian vault: {OBSIDIAN_VAULT}")
    print(f"[INFO] Press Ctrl+C to stop\n")

    running = True

    def signal_handler(sig, frame):
        nonlocal running
        print("\n[INFO] Shutting down...")
        running = False

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while running:
        timestamp = get_timestamp()
        audio_path = AUDIO_CACHE / f"capture_{timestamp}.wav"

        print(f"[{timestamp}] Recording {args.duration}s...")
        if not record_audio(audio_path, args.duration):
            print("[WARN] Recording failed, retrying next interval...")
            time.sleep(args.interval)
            continue

        print(f"[{timestamp}] Transcribing...")
        text = transcribe_audio(audio_path)
        cleanup_audio(audio_path)

        if text:
            print(f"[{timestamp}] Transcribed: {text[:100]}...")
            save_to_obsidian(text, timestamp)
        else:
            print(f"[WARN] No transcription result")

        if args.once:
            break

        # Wait for next interval
        print(f"[INFO] Next capture in {args.interval}s...")
        for _ in range(args.interval):
            if not running:
                break
            time.sleep(1)

    print("[INFO] Auto-Capture Audio stopped.")


if __name__ == "__main__":
    main()
