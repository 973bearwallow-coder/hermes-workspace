#!/usr/bin/env python3
"""
fathom_keyframes.py — Extract sparse screen-share keyframes from a coaching-call
video, OCR/vision each, and link them to transcript timestamps.

Pipeline:
  1. Get video (from local MP4 path, OR attempt yt-dlp on a Fathom /share/ URL)
  2. ffmpeg scene-change frame extraction (cap ~1 frame / 30s, max 40 frames)
  3. Vision-OCR each frame -> short caption
  4. Pull Fathom transcript (timestamps) from the /share/ page
  5. Write <name>.keyframes.md: timestamp | caption | screenshot
  6. Clean up video + temp frames (keep only small screenshots + md)

Usage:
  python3 fathom_keyframes.py --url <fathom_share_url> [--out <dir>]
  python3 fathom_keyframes.py --video <local.mp4> --transcript <txt> [--out <dir>]

Storage: ~40 frames * ~50KB = ~2MB vs 500MB+ raw video.
"""
import os, sys, re, json, subprocess, argparse, shutil
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_KEYFRAMES = os.path.expanduser("~/hermes-workspace/coaching-calls/keyframes")
MAX_FRAMES = 40
MIN_SCENE_INTERVAL = 30  # seconds between frames (min)

def extract_frames(video_path, out_dir):
    """Scene-change detection with min interval cap. Returns list of (timestamp_sec, img_path)."""
    frames_dir = os.path.join(out_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)
    # ffmpeg select scene-change, but throttle to MIN_SCENE_INTERVAL via fps filter trick:
    # Use select='gte(scene,0.3)' then fps=1/MIN_SCENE_INTERVAL to cap density.
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", f"select='gte(scene,0.1)',metadata=print:key=lavfi.scene_score,fps=1/{MIN_SCENE_INTERVAL}",
        "-vsync", "vfr",
        os.path.join(frames_dir, "frame_%04d.jpg")
    ]
    subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    frames = sorted(
        [f for f in os.listdir(frames_dir) if f.endswith(".jpg")],
        key=lambda x: int(re.search(r"(\d+)", x).group(1))
    )
    # fallback: if scene-detection found <3 frames, do fixed-interval extraction
    if len(frames) < 3:
        subprocess.run([
            "ffmpeg", "-y", "-i", video_path,
            "-vf", f"fps=1/{MIN_SCENE_INTERVAL}",
            os.path.join(frames_dir, "frame_%04d.jpg")
        ], capture_output=True, text=True, timeout=300)
        frames = sorted(
            [f for f in os.listdir(frames_dir) if f.endswith(".jpg")],
            key=lambda x: int(re.search(r"(\d+)", x).group(1))
        )
    # cap to MAX_FRAMES evenly
    if len(frames) > MAX_FRAMES:
        step = len(frames) / MAX_FRAMES
        frames = [frames[int(i * step)] for i in range(MAX_FRAMES)]
    # map filename -> approx timestamp via frame index * MIN_SCENE_INTERVAL (approx)
    result = []
    for i, f in enumerate(frames):
        ts = i * MIN_SCENE_INTERVAL  # approximate; refined if transcript has real timestamps
        result.append((ts, os.path.join(frames_dir, f)))
    return result

def vision_caption(image_path):
    """OCR the frame with tesseract (best-effort). For richer captioning, Atlas
    (native vision) captions interactively. Autonomous cron uses OCR text."""
    tesseract = "/home/linuxbrew/.linuxbrew/bin/tesseract"
    if not os.path.exists(tesseract):
        tesseract = "tesseract"  # hope it's on PATH
    try:
        out = subprocess.run([tesseract, image_path, "stdout"],
                             capture_output=True, text=True, timeout=30)
        text = out.stdout.strip()
        if text:
            return text[:300].replace("\n", " ")
    except Exception:
        pass
    return "[OCR_UNAVAILABLE]"

def pull_fathom_transcript(share_url):
    """Best-effort: scrape Fathom /share/ page for transcript. Returns list of
    (timestamp_str, text) if found, else []. Requires browser (handled by caller)."""
    # This function is a placeholder — the cron prompt does browser scraping.
    # When called standalone with --url, we attempt yt-dlp + note transcript pulled separately.
    return []

def write_keyframes_md(name, frames_data, out_dir, transcript=None):
    """frames_data: list of (ts_sec, img_path, caption). Write markdown + copy small imgs."""
    base = out_dir if out_dir else VAULT_KEYFRAMES
    keep_dir = os.path.join(base, name)
    os.makedirs(keep_dir, exist_ok=True)
    md = [f"# Keyframes — {name}", ""]
    md.append(f"Generated: {datetime.now(timezone.utc).isoformat()}")
    md.append(f"Frames: {len(frames_data)} (sparse scene-change capture)")
    md.append("")
    md.append("| Timestamp | What's on screen | Screenshot |")
    md.append("|---|---|---|")
    for ts, img_path, caption in frames_data:
        # copy small screenshot into vault
        dest = os.path.join(keep_dir, os.path.basename(img_path))
        shutil.copy(img_path, dest)
        mmss = f"{ts//60:02d}:{ts%60:02d}"
        md.append(f"| {mmss} | {caption} | ![frame]({dest}) |")
    md_path = os.path.join(base, f"{name}.keyframes.md")
    with open(md_path, "w") as f:
        f.write("\n".join(md))
    return md_path

def attempt_download(share_url, out_dir):
    """Try yt-dlp on Fathom share URL. Returns local mp4 path or None."""
    try:
        out_tmpl = os.path.join(out_dir, "video.%(ext)s")
        r = subprocess.run(["yt-dlp", "-f", "mp4", "-o", out_tmpl, share_url],
                           capture_output=True, text=True, timeout=240)
        if r.returncode == 0:
            for f in os.listdir(out_dir):
                if f.startswith("video.") and f.endswith(".mp4"):
                    return os.path.join(out_dir, f)
    except Exception:
        pass
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", help="Fathom /share/ URL")
    ap.add_argument("--video", help="Local MP4 path")
    ap.add_argument("--transcript", help="Transcript txt (optional)")
    ap.add_argument("--name", help="Output name (default: from url or video)")
    ap.add_argument("--out", default=VAULT_KEYFRAMES)
    args = ap.parse_args()

    work = os.path.join(args.out, "_work")
    os.makedirs(work, exist_ok=True)

    video = args.video
    if not video and args.url:
        print(f"Attempting download from {args.url} ...")
        video = attempt_download(args.url, work)
        if not video:
            print("DOWNLOAD_FAILED: yt-dlp could not grab Fathom video. "
                  "Provide local MP4 via --video, or use browser-capture.")
            return 1

    if not video or not os.path.exists(video):
        print("NO_VIDEO: need --video <mp4> or --url that downloads.")
        return 1

    name = args.name or os.path.splitext(os.path.basename(video))[0]
    print(f"Extracting keyframes from {video} ...")
    frames = extract_frames(video, work)
    print(f"  got {len(frames)} frames")
    frames_data = []
    for ts, img in frames:
        cap = vision_caption(img)
        frames_data.append((ts, img, cap))
    md = write_keyframes_md(name, frames_data, args.out)
    # cleanup work dir (video + temp frames)
    shutil.rmtree(work, ignore_errors=True)
    print(f"KEYFRAMES_WRITTEN: {md}")
    print(f"Storage: {len(frames_data)} screenshots (~{len(frames_data)*50}KB) vs raw video.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
