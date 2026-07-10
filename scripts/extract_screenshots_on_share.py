#!/usr/bin/env python3
"""
extract_screenshots_on_share.py

Post-processing script:
1. Reads Whisper JSON transcript (with timestamps)
2. Scans for screen-share keywords
3. Extracts video frames at those timestamps
4. Saves screenshots for the dashboard

Usage:
    python3 extract_screenshots_on_share.py <video_path> <transcript_json>
"""

import sys
import json
import subprocess
from pathlib import Path

# Keywords that indicate a screen share
SCREEN_SHARE_KEYWORDS = [
    "share my screen",
    "let me share",
    "let me show you",
    "pull up",
    "bring up",
    "open the slide",
    "show you the",
    "take a look at this",
    "screen share",
    "sharing my screen",
]

def find_screen_share_timestamps(transcript_json_path):
    """
    Scan Whisper JSON for screen-share keywords.
    Returns list of timestamps (seconds) where keywords were detected.
    """
    with open(transcript_json_path, 'r') as f:
        data = json.load(f)
    
    timestamps = []
    
    # Whisper JSON structure: data['segments'] = [{start, end, text}, ...]
    for segment in data.get('segments', []):
        text = segment.get('text', '').lower()
        start_time = segment.get('start', 0)
        
        # Check if any keyword is in this segment
        for keyword in SCREEN_SHARE_KEYWORDS:
            if keyword in text:
                timestamps.append(start_time)
                break  # Only add once per segment
    
    return timestamps

def extract_frames(video_path, timestamps, output_dir, seconds_before=5, seconds_after=5):
    """
    Extract video frames at given timestamps (± buffer).
    Saves as screenshot_<timestamp>.jpg
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    extracted = []
    
    for ts in timestamps:
        # Calculate start time (with buffer)
        start_time = max(0, ts - seconds_before)
        
        # Extract 3 frames: before, at, after
        for offset in [0, 2, 4]:
            frame_time = start_time + offset
            output_path = output_dir / f"screenshot_{int(ts)}_{int(offset)}.jpg"
            
            cmd = [
                'ffmpeg', '-ss', str(frame_time), '-i', str(video_path),
                '-vframes', '1', '-q:v', '2', str(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True)
            if result.returncode == 0:
                extracted.append(str(output_path))
    
    return extracted

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 extract_screenshots_on_share.py <video_path> <transcript_json>")
        sys.exit(1)
    
    video_path = sys.argv[1]
    transcript_json = sys.argv[2]
    
    print(f"📹 Video: {video_path}")
    print(f"📝 Transcript: {transcript_json}")
    
    # Step 1: Find screen-share timestamps
    print("\n🔍 Scanning transcript for screen-share keywords...")
    timestamps = find_screen_share_timestamps(transcript_json)
    
    if not timestamps:
        print("❌ No screen-share keywords found.")
        return
    
    print(f"✅ Found {len(timestamps)} potential screen-share moment(s):")
    for ts in timestamps:
        print(f"   - {ts:.1f}s")
    
    # Step 2: Extract frames
    output_dir = Path(video_path).parent / "screenshots"
    print(f"\n📸 Extracting frames to {output_dir}...")
    extracted = extract_frames(video_path, timestamps, output_dir)
    
    print(f"✅ Extracted {len(extracted)} screenshot(s)")
    for path in extracted:
        print(f"   - {path}")

if __name__ == "__main__":
    main()
