#!/bin/bash
# Fully detached recording script - survives Hermes gateway restarts
# Usage: bash detached_record.sh [duration_seconds]

export DISPLAY=:1
export XDG_RUNTIME_DIR=/run/user/1000

OUTPUT_DIR="/home/tom/Desktop/coaching_call"
mkdir -p "$OUTPUT_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DURATION=${1:-7200}
VIDEO_FILE="$OUTPUT_DIR/screen_recording_${TIMESTAMP}.mkv"
AUDIO_FILE="$OUTPUT_DIR/audio_${TIMESTAMP}.wav"
FINAL_FILE="$OUTPUT_DIR/coaching_${TIMESTAMP}_final.mp4"

echo "=== Recording started $(date) ===" > "$OUTPUT_DIR/record_${TIMESTAMP}.log"
echo "Script PID: $$" >> "$OUTPUT_DIR/record_${TIMESTAMP}.log"

# Trap signals to prevent being killed
trap '' SIGTERM SIGINT SIGHUP

# Start audio recording
pw-record --format s16 --rate 48000 --channels 2 \
  --target alsa_output.pci-0000_2b_00.1.hdmi-stereo.monitor \
  "$AUDIO_FILE" &
AUD_PID=$!

# Start video recording
ffmpeg -f x11grab -video_size 1920x1080 -framerate 15 -i :1 \
  -c:v libx264 -preset ultrafast -crf 28 -an \
  -t $DURATION -y "$VIDEO_FILE" >> "$OUTPUT_DIR/record_${TIMESTAMP}.log" 2>&1 &
VID_PID=$!

# Save PIDs
echo "$VID_PID $AUD_PID $TIMESTAMP $AUDIO_FILE $VIDEO_FILE $FINAL_FILE" > "$OUTPUT_DIR/recording_pids_${TIMESTAMP}.log"
echo "Video PID: $VID_PID | Audio PID: $AUD_PID" >> "$OUTPUT_DIR/record_${TIMESTAMP}.log"

# Wait for video to finish
wait $VID_PID 2>/dev/null

# Stop audio
kill $AUD_PID 2>/dev/null
wait $AUD_PID 2>/dev/null

# Combine
echo "Combining video + audio..." >> "$OUTPUT_DIR/record_${TIMESTAMP}.log"
ffmpeg -i "$VIDEO_FILE" -i "$AUDIO_FILE" \
  -c:v copy -c:a aac -b:a 128k \
  -y "$FINAL_FILE" 2>&1 | tail -3 >> "$OUTPUT_DIR/record_${TIMESTAMP}.log"

# Cleanup temp files
rm -f "$VIDEO_FILE" "$AUDIO_FILE"

echo "=== DONE: $FINAL_FILE ===" >> "$OUTPUT_DIR/record_${TIMESTAMP}.log"
ls -lh "$FINAL_FILE" >> "$OUTPUT_DIR/record_${TIMESTAMP}.log"
