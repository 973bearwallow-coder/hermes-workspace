#!/bin/bash
# Coaching Call Auto-Recorder
# Records screen + audio for unattended meeting capture
# Usage: ./coaching_call_record.sh <duration_seconds> [output_name]

set -e

export DISPLAY=:1
export XDG_RUNTIME_DIR=/run/user/1000
export XAUTHORITY=/run/user/1000/gdm/Xauthority

OUTPUT_DIR="/home/tom/Desktop/coaching_call"
mkdir -p "$OUTPUT_DIR"

DURATION=${1:-5400}
NAME=${2:-$(date +%Y%m%d_%H%M)}
VIDEO_FILE="$OUTPUT_DIR/${NAME}_video.mkv"
AUDIO_FILE="$OUTPUT_DIR/${NAME}_audio.wav"
FINAL_FILE="$OUTPUT_DIR/${NAME}_final.mp4"

echo "=== Coaching Call Recorder ==="
echo "Started: $(date)"
echo "Duration: ${DURATION}s (~$(( DURATION / 60 )) min)"
echo ""

# Kill any existing recordings
pkill -9 -f "ffmpeg.*x11grab" 2>/dev/null || true
pkill -9 -f "pw-record" 2>/dev/null || true
sleep 1

# --- Audio sink detection ---
# Try to find an active audio sink monitor.
# Common sinks on this machine:
#   - IEC958 S/PDIF (ALC892 Digital): alsa_output.pci-0000_2d_00.4.iec958-stereo.monitor
#   - HDMI (NVidia): alsa_output.pci-0000_2b_00.1.hdmi-stereo.monitor

MONITOR=""
for TRY in \
  "alsa_output.pci-0000_2d_00.4.iec958-stereo.monitor" \
  "alsa_output.pci-0000_2b_00.1.hdmi-stereo.monitor" \
  "alsa_output.pci-0000_00_1b.hdmi-stereo-extra1.monitor" \
  "@DEFAULT_MONITOR@"; do
  
  # Test if the monitor works by recording 1s to a temp file
  timeout 3 pw-record --format s16 --rate 16000 --channels 1 \
    --target "$TRY" /tmp/_sink_test.wav 2>/dev/null || true
  BYTES=$(stat -c %s /tmp/_sink_test.wav 2>/dev/null || echo 0)
  rm -f /tmp/_sink_test.wav
  if [ "$BYTES" -gt 1000 ]; then
    MONITOR="$TRY"
    echo "✅ Found working audio monitor: $MONITOR"
    break
  fi
done

if [ -z "$MONITOR" ]; then
  echo "⚠️ No working audio monitor found — video only"
  RECORD_AUDIO=false
else
  RECORD_AUDIO=true
fi

# Start audio recording
if [ "$RECORD_AUDIO" = true ]; then
  pw-record --format s16 --rate 48000 --channels 2 \
    --target "$MONITOR" \
    "$AUDIO_FILE" &
  AUD_PID=$!
  echo "Audio PID: $AUD_PID (from $MONITOR)"
else
  AUD_PID=""
fi

# Verify audio after 5 seconds
sleep 5
if [ "$RECORD_AUDIO" = true ]; then
  if [ -f "$AUDIO_FILE" ]; then
    BYTES=$(stat -c %s "$AUDIO_FILE" 2>/dev/null || echo 0)
    if [ "$BYTES" -gt 500 ]; then
      echo "✅ Audio: RECORDING (${BYTES} bytes in first 5s)"
    else
      echo "⚠️ Audio: file too small (${BYTES} bytes) — may not capture system audio"
    fi
  else
    echo "⚠️ Audio: file not created yet"
  fi
fi

# Start video recording
ffmpeg -f x11grab -video_size 1920x1080 -framerate 15 -i :1 \
  -c:v libx264 -preset ultrafast -crf 28 \
  -an \
  -t $DURATION \
  -y "$VIDEO_FILE" >> "$OUTPUT_DIR/${NAME}_record.log" 2>&1 &
VID_PID=$!
echo "Video PID: $VID_PID"

echo "$VID_PID ${AUD_PID:-0}" > "$OUTPUT_DIR/${NAME}.pids"

# Verify video
sleep 3
echo ""
echo "=== Status ==="
if kill -0 $VID_PID 2>/dev/null; then
  echo "✅ Video: RECORDING"
else
  echo "❌ Video: FAILED"
  tail -3 "$OUTPUT_DIR/${NAME}_record.log"
fi
[ "$RECORD_AUDIO" = true ] && echo "✅ Audio: RECORDING" || echo "ℹ️ Audio: SKIPPED"

echo ""
echo "Recording until: $(date -d "+${DURATION seconds}" '+%H:%M')"
echo ""

# Wait for video to finish
wait $VID_PID 2>/dev/null
echo "Video finished at $(date)"

# Kill audio
if [ "$RECORD_AUDIO" = true ] && [ -n "$AUD_PID" ]; then
  kill $AUD_PID 2>/dev/null
  wait $AUD_PID 2>/dev/null || true
  echo "Audio stopped"
fi

# Combine
if [ "$RECORD_AUDIO" = true ] && [ -f "$AUDIO_FILE" ]; then
  A_SIZE=$(stat -c %s "$AUDIO_FILE" 2>/dev/null || echo 0)
  if [ "$A_SIZE" -gt 100000 ]; then
    echo "Combining video + audio..."
    ffmpeg -i "$VIDEO_FILE" -i "$AUDIO_FILE" \
      -c:v copy -c:a aac -b:a 128k \
      -y "$FINAL_FILE" 2>&1 | tail -3
    rm -f "$VIDEO_FILE" "$AUDIO_FILE" "$OUTPUT_DIR/${NAME}.pids"
  else
    echo "⚠️ Audio too small (${A_SIZE}b) — video only"
    mv "$VIDEO_FILE" "$FINAL_FILE"
  fi
else
  mv "$VIDEO_FILE" "$FINAL_FILE"
  rm -f "$AUDIO_FILE" "$OUTPUT_DIR/${NAME}.pids"
fi

echo ""
echo "=== COMPLETE ==="
ls -lh "$FINAL_FILE"
echo "Finished: $(date)"
