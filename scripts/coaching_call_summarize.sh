#!/bin/bash
# Coaching Call Transcriber & Summarizer
# Transcribes audio with Whisper and prepares summary for LLM analysis
# Usage: ./coaching_call_summarize.sh <audio_file> [call_focus_topics]

AUDIO_FILE="$1"
TOPICS="${2:-persistent memory for AI agents, local SEO ranking, blog content pipeline, tool recommendations, workflow patterns}"

if [ -z "$AUDIO_FILE" ] || [ ! -f "$AUDIO_FILE" ]; then
  echo "Usage: $0 <audio_file> [topics]"
  echo "Example: $0 /home/tom/Desktop/coaching_call/tuesday_audio.wav"
  exit 1
fi

OUTPUT_DIR=$(dirname "$AUDIO_FILE")
TIMESTAMP=$(basename "$AUDIO_FILE" | sed 's/_audio.wav//; s/_normalized.wav//; s/\.wav//')
NORMALIZED_FILE="$OUTPUT_DIR/${TIMESTAMP}_normalized.wav"

echo "=== Coaching Call Summarizer ==="
echo "Audio: $AUDIO_FILE"
echo "Topics: $TOPICS"
echo ""

# Step 1: Normalize audio (boost quiet recordings from pw-record)
echo "[1/3] Normalizing audio levels..."
ffmpeg -y -i "$AUDIO_FILE" \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11" \
  "$NORMALIZED_FILE" 2>&1 | tail -3
echo "✅ Normalized: $NORMALIZED_FILE"
echo ""

# Step 2: Transcribe with Whisper (turbo model for speed + quality)
echo "[2/3] Transcribing normalized audio with Whisper turbo..."
whisper "$NORMALIZED_FILE" \
  --model large-v3-turbo \
  --language en \
  --output_format txt \
  --output_dir "$OUTPUT_DIR" 2>&1

# Whisper outputs as <input_basename>.txt
EXPECTED_TRANSCRIPT="$OUTPUT_DIR/$(basename "$NORMALIZED_FILE" .wav).txt"
ACTUAL_TRANSCRIPT=""

if [ -f "$EXPECTED_TRANSCRIPT" ]; then
  ACTUAL_TRANSCRIPT="$EXPECTED_TRANSCRIPT"
else
  # Fallback: find latest txt with transcript content
  for f in "$OUTPUT_DIR"/*.txt; do
    if [ -f "$f" ] && grep -q '\[.*-->.*\]' "$f" 2>/dev/null; then
      ACTUAL_TRANSCRIPT="$f"
      break
    fi
  done
fi

if [ -z "$ACTUAL_TRANSCRIPT" ] || [ ! -f "$ACTUAL_TRANSCRIPT" ]; then
  echo "❌ Transcription failed — no output file found"
  exit 1
fi

echo "✅ Transcript: $ACTUAL_TRANSCRIPT"
echo ""

# Step 3: Output summary prompt for LLM
echo "[3/3] Ready for LLM analysis"
echo ""
echo "============================================="
echo "TRANSCRIPT READY FOR LLM ANALYSIS"
echo "============================================="
echo ""
echo "File: $ACTUAL_TRANSCRIPT"
echo "Focus topics: $TOPICS"
echo ""
echo "Transcript size: $(wc -l < "$ACTUAL_TRANSCRIPT") lines"
echo ""

cat <<PROMPT

--- LLM SUMMARY PROMPT ---

Analyze this coaching call transcript and extract ONLY actionable intelligence.

Focus on these topics: $TOPICS

FORMAT YOUR RESPONSE AS:

## 🎯 Key Takeaways
(2-3 sentences on the overall value of the call)

## 🛠️ Tools Mentioned
| Tool | What It Does | Relevance to Us |
|------|-------------|-----------------|

## 💡 Actionable Items
(Specific things we can do or try — numbered list)

## ⚠️ Fluff Detected
(Community/marketing talk that wasn't useful — so we know what to ignore next time)

## 📊 Verdict
(Was this call worth the time? What's the signal-to-noise ratio?)

--- END PROMPT ---

PROMPT

echo ""
echo "=== DONE ==="
echo "Transcript: $ACTUAL_TRANSCRIPT"
echo "Size: $(wc -l < "$ACTUAL_TRANSCRIPT") lines"
