#!/bin/bash
# Screen Recorder for Charles — captures screen + system audio to a single MP4
# Usage: ./screen_record.sh [duration_seconds]
# Default: 90 minutes

set -e

export DISPLAY=:1
export XDG_RUNTIME_DIR=/run/user/1000

OUTPUT_DIR="/home/tom/Desktop/coaching_call"
mkdir -p "$OUTPUT_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DURATION=${1:-5400}  # Default 90 minutes

VIDEO_FILE="$OUTPUT_DIR/screen_recording_${TIMESTAMP}.mkv"
AUDIO_FILE="$OUTPUT_DIR/audio_${TIMESTAMP}.wav"
FINAL_FILE="$OUTPUT_DIR/screen_recording_${TIMESTAMP}.mp4"

echo "=== Screen Recorder ==="
echo "Started: $(date)"
echo "Duration: ${DURATION}s (~$(( DURATION / 60 )) minutes)"
echo "Video: $VIDEO_FILE"
echo "Audio: $AUDIO_FILE"
echo "Final: $FINAL_FILE"
echo ""

# Kill any existing recordings
pkill -9 -f "ffmpeg.*x11grab" 2>/dev/null || true
pkill -9 -f "pw-record" 2>/dev/null || true
sleep 1

# Start audio recording (monitor of HDMI sink = Chrome/system audio)
pw-record --format s16 --rate 48000 --channels 2 \
  --target alsa_output.pci-0000_2b_00.1.hdmi-stereo.monitor \
  "$AUDIO_FILE" &
AUD_PID=$!
echo "Audio PID: $AUD_PID"

sleep 1

# Start video recording
ffmpeg -f x11grab -video_size 1920x1080 -framerate 15 -i :1 \
  -c:v libx264 -preset ultrafast -crf 28 \
  -an \
  -t $DURATION \
  -y "$VIDEO_FILE" >> "$OUTPUT_DIR/record_${TIMESTAMP}.log" 2>&1 &
VID_PID=$!
echo "Video PID: $VID_PID"

# Verify
sleep 3
if kill -0 $VID_PID 2>/dev/null; then
  echo "✅ Video recording: ACTIVE"
else
  echo "❌ Video recording: FAILED"
  tail -5 "$OUTPUT_DIR/record_${TIMESTAMP}.log"
fi

if kill -0 $AUD_PID 2>/dev/null; then
  echo "✅ Audio recording: ACTIVE"
else
  echo "⚠️ Audio recording: NOT RUNNING (video-only mode)"
fi

echo ""
echo "RECORDING IN PROGRESS — output will be combined when done"
echo "To stop early: kill $VID_PID $AUD_PID"
echo "PIDs saved to: $OUTPUT_DIR/recording_pids_${TIMESTAMP}.txt"
echo "$VID_PID $AUD_PID $TIMESTAMP" > "$OUTPUT_DIR/recording_pids_${TIMESTAMP}.txt"

# Wait for video to finish (audio will be killed after)
wait $VID_PID 2>/dev/null
echo ""
echo "Video recording finished at $(date)"

# Kill audio recording
kill $AUD_PID 2>/dev/null
wait $AUD_PID 2>/dev/null
echo "Audio recording stopped"

# Combine video + audio into final MP4
echo "Combining video + audio into final MP4..."
ffmpeg -i "$VIDEO_FILE" -i "$AUDIO_FILE" \
  -c:v copy -c:a aac -b:a 128k \
  -y "$FINAL_FILE" 2>&1 | tail -5

# Clean up temp files
rm -f "$VIDEO_FILE" "$AUDIO_FILE"

echo ""
echo "=== COMPLETE ==="
echo "Final file: $FINAL_FILE"
ls -lh "$FINAL_FILE"
