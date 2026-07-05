#!/usr/bin/env bash
# Analyze a video URL or local file using claude-real-video pipeline
# Usage: analyze_video.sh <url_or_path> [output_dir]
# Output: frames/ + MANIFEST.txt (with transcript if available)
set -euo pipefail

SRC="${1:?Usage: analyze_video.sh <url_or_path> [output_dir]}"
OUT="${2:-crv-out}"

VENV="/home/tom/hermes-workspace/skills/approved/claude-real-video/venv"
source "$VENV/bin/activate"

# Run crv — scene-aware extraction + dedup + optional full audio
# --report: keep dropped frames for tuning feedback
# --max-frames 150: enough for analysis, not overwhelming
exec claude-real-video "$SRC" -o "$OUT" --max-frames 150 --report 2>&1