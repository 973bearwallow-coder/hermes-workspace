#!/usr/bin/env python3
"""Extract evidence-focused review frames near visual-demo transcript cues.

Usage: extract_screenshots_on_share.py VIDEO TRANSCRIPT_JSON [OUT_DIR]
Writes a manifest explaining why each frame was captured. The frames must be
reviewed alongside the transcript; they do not validate spoken claims alone.
"""
import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

SCREEN_SHARE_KEYWORDS = (
    "share my screen", "let me share", "let me show you", "pull up",
    "bring up", "open the slide", "show you the", "take a look at this",
    "screen share", "sharing my screen", "look at this", "on the screen",
    "this dashboard", "this demo",
)


def find_visual_moments(transcript_json_path, minimum_gap=30):
    """Return deduplicated moments with timestamp and supporting transcript."""
    data = json.loads(Path(transcript_json_path).read_text(encoding="utf-8"))
    moments = []
    for segment in data.get("segments", []):
        text = str(segment.get("text", "")).strip()
        lowered = text.lower()
        hits = [keyword for keyword in SCREEN_SHARE_KEYWORDS if keyword in lowered]
        if not hits:
            continue
        timestamp = float(segment.get("start", 0.0))
        if moments and timestamp - moments[-1]["timestamp_seconds"] < minimum_gap:
            moments[-1]["keywords"] = sorted(set(moments[-1]["keywords"] + hits))
            moments[-1]["transcript_evidence"] += " " + text
            continue
        moments.append({
            "timestamp_seconds": timestamp,
            "keywords": hits,
            "transcript_evidence": text[:500],
        })
    return moments


def find_screen_share_timestamps(transcript_json_path):
    """Backward-compatible timestamp-only API."""
    return [m["timestamp_seconds"] for m in find_visual_moments(transcript_json_path)]


def video_duration(video_path):
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(video_path),
    ], check=True, capture_output=True, text=True)
    return float(result.stdout.strip())


def extract_frames(video_path, moments, output_dir, offsets=(-3, 0, 5)):
    """Capture a small before/at/after cluster for every visual moment."""
    video_path = Path(video_path)
    if not video_path.is_file():
        raise FileNotFoundError(f"Video not found: {video_path}")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    duration = video_duration(video_path)
    frames = []
    for index, moment in enumerate(moments, 1):
        timestamp = float(moment["timestamp_seconds"])
        for offset in offsets:
            frame_time = min(max(0.0, timestamp + offset), max(0.0, duration - 0.05))
            output_path = output_dir / f"visual_{index:02d}_{frame_time:08.2f}s.jpg"
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-ss", f"{frame_time:.3f}", "-i", str(video_path),
                "-frames:v", "1", "-q:v", "2", str(output_path),
            ], check=True)
            frames.append({
                "path": str(output_path), "moment": index,
                "timestamp_seconds": frame_time, "offset_seconds": offset,
            })
    return frames, duration


def run_review(video_path, transcript_json_path, output_dir):
    moments = find_visual_moments(transcript_json_path)
    frames, duration = extract_frames(video_path, moments, output_dir) if moments else ([], video_duration(video_path))
    manifest = {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "video": str(Path(video_path)),
        "transcript": str(Path(transcript_json_path)),
        "video_duration_seconds": duration,
        "method": "transcript-cue clustered keyframes",
        "review_warning": "Frames are visual evidence to review; their existence does not validate spoken claims.",
        "moments": moments,
        "frames": frames,
    }
    manifest_path = Path(output_dir) / "review_manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("transcript_json", type=Path)
    parser.add_argument("output_dir", type=Path, nargs="?")
    args = parser.parse_args(argv)
    output_dir = args.output_dir or args.video.parent / "screenshots" / args.video.stem
    manifest = run_review(args.video, args.transcript_json, output_dir)
    print(f"Extracted {len(manifest['frames'])} frame(s) from {len(manifest['moments'])} visual moment(s).")
    print(f"Manifest: {output_dir / 'review_manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
