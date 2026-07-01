#!/usr/bin/env bash
# coaching_call_pipeline.sh
# One-click: record Google Meet → transcribe → summarize → deliver to Tom
# All local, all free (Whisper + Ollama on RTX 3090)
#
# Usage:
#   ./coaching_call_pipeline.sh record [duration_min]  — start recording
#   ./coaching_call_pipeline.sh process               — transcribe + summarize latest recording
#   ./coaching_call_pipeline.sh full [duration_min]   — record, then auto-process
#   ./coaching_call_pipeline.sh status                — check if recording is active

set -uo pipefail

OUTPUT_DIR="/home/tom/Desktop/coaching_call"
mkdir -p "$OUTPUT_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M)
SUMMARY_MODEL="mistral-nemo"  # Fast, good quality, fits GPU alongside Whisper
WHISPER_MODEL="large-v3-turbo"

# Focus topics for the LLM summary
TOPICS="AI Profit Boardroom coaching, AI agents and tools, local SEO, business automation, workflow optimization, revenue growth strategies"

# ─── RECORD ───────────────────────────────────────────────────────────
cmd_record() {
    local duration_min="${1:-90}"
    local duration_sec=$((duration_min * 60))

    echo "🔴 Starting coaching call recording (${duration_min} min)"
    echo "   Time: $(date '+%H:%M') → $(date -d "+${duration_min} minutes" '+%H:%M')"

    # Use the existing recording script
    bash /home/tom/hermes-workspace/scripts/coaching_call_record.sh "$duration_sec" "$TIMESTAMP"
}

# ─── PROCESS (Transcribe + Summarize) ────────────────────────────────
cmd_process() {
    # Find latest audio/recording
    local latest_audio=""
    local latest_video=""

    # Check for wav files first (preferred by Whisper)
    latest_audio=$(ls -t "$OUTPUT_DIR"/*_audio.wav 2>/dev/null | head -1)
    if [ -z "$latest_audio" ]; then
        # Check for mp4/mkv — extract audio if needed
        local latest_media=$(ls -t "$OUTPUT_DIR"/*_final.mp4 "$OUTPUT_DIR"/*.mkv 2>/dev/null | head -1)
        if [ -n "$latest_media" ]; then
            echo "📹 Found video recording: $(basename "$latest_media")"
            echo "   Extracting audio..."
            latest_audio="$OUTPUT_DIR/${TIMESTAMP}_extracted.wav"
            ffmpeg -y -i "$latest_media" -vn -acodec pcm_s16le -ar 16000 -ac 1 \
                "$latest_audio" 2>/dev/null
            if [ ! -s "$latest_audio" ]; then
                echo "❌ Audio extraction failed"
                exit 1
            fi
        else
            echo "❌ No recordings found in $OUTPUT_DIR"
            exit 1
        fi
    fi

    local audio_size=$(stat -c %s "$latest_audio" 2>/dev/null || echo 0)
    local audio_mb=$((audio_size / 1048576))
    echo "🎵 Audio: $(basename "$latest_audio") (${audio_mb} MB)"

    # Step 1: Normalize audio
    echo ""
    echo "[1/3] Normalizing audio levels..."
    local normalized="$OUTPUT_DIR/${TIMESTAMP}_normalized.wav"
    ffmpeg -y -i "$latest_audio" \
        -af "loudnorm=I=-16:TP=-1.5:LRA=11" \
        "$normalized" 2>&1 | tail -1

    # Step 2: Transcribe with Whisper
    echo "[2/3] Transcribing with Whisper ${WHISPER_MODEL}..."
    local transcript_start=$(date +%s)
    
    whisper "$normalized" \
        --model "$WHISPER_MODEL" \
        --language en \
        --output_format txt \
        --output_dir "$OUTPUT_DIR" 2>&1 | tail -3

    local transcript_end=$(date +%s)
    local transcript_time=$((transcript_end - transcript_start))

    # Find the transcript file
    local transcript="$OUTPUT_DIR/${TIMESTAMP}_normalized.txt"
    if [ ! -f "$transcript" ]; then
        transcript=$(ls -t "$OUTPUT_DIR"/*.txt 2>/dev/null | head -1)
    fi

    if [ -z "$transcript" ] || [ ! -f "$transcript" ]; then
        echo "❌ Transcription failed — no output file found"
        exit 1
    fi

    local transcript_lines=$(wc -l < "$transcript")
    local transcript_chars=$(wc -c < "$transcript")
    echo "✅ Transcript: ${transcript_lines} lines, ${transcript_chars} chars (${transcript_time}s)"

    # Step 3: Summarize with local LLM via Ollama
    echo "[3/3] Summarizing with ${SUMMARY_MODEL}..."

    # Build the prompt
    local SUMMARY_PROMPT
    read -r -d '' SUMMARY_PROMPT << 'PROMPT_EOF' || true
You are an expert business coaching call analyst. Analyze this transcript and extract ONLY actionable intelligence that benefits our business.

Focus areas: TOPICS_PLACEHOLDER

Format your response EXACTLY as:

## 🎯 Key Takeaways
(2-3 sentences on the overall value of the call)

## 🛠️ Tools & Resources Mentioned
(List any tools, software, services, or resources mentioned with what they do and relevance)

## 💡 Actionable Items
(Numbered list of specific things we can DO or TRY — be concrete)

## 💰 Revenue/Cost Insights
(Any money-making or cost-saving ideas mentioned)

## ⚠️ Skip Next Time
(What was fluff/marketing/irrelevant — so we know what to ignore)

## 📊 Verdict
(Was this call worth the time? Signal-to-noise ratio? 1-10 rating)

---
TRANSCRIPT:
PROMPT_EOF

    SUMMARY_PROMPT="${SUMMARY_PROMPT/TOPICS_PLACEHOLDER/$TOPICS}"

    # Send transcript to Ollama
    local summary_file="$OUTPUT_DIR/summary_${TIMESTAMP}.md"
    
    # Truncate transcript if very long (keep first 24K chars for the LLM context)
    local truncated_transcript
    if [ "$transcript_chars" -gt 24000 ]; then
        truncated_transcript=$(head -c 24000 "$transcript")
        echo "   (Truncated transcript from ${transcript_chars} to 24000 chars)"
    else
        truncated_transcript=$(cat "$transcript")
    fi

    echo "${SUMMARY_PROMPT}" > /tmp/coaching_prompt.txt
    echo "${truncated_transcript}" >> /tmp/coaching_prompt.txt

    curl -s http://127.0.0.1:11434/v1/chat/completions \
        -H "Content-Type: application/json" \
        -d "$(python3 -c "
import json, sys
with open('/tmp/coaching_prompt.txt') as f:
    full = f.read()
# Split at TRANSCRIPT: line
parts = full.split('---\nTRANSCRIPT:\n', 1)
sys_text = parts[0] if len(parts) > 1 else ''
user_text = parts[1] if len(parts) > 1 else full
payload = {
    'model': '${SUMMARY_MODEL}',
    'messages': [
        {'role': 'system', 'content': sys_text.strip()},
        {'role': 'user', 'content': user_text.strip()[:22000]}
    ],
    'temperature': 0.3,
    'max_tokens': 2000,
    'stream': False
}
print(json.dumps(payload))
")" | python3 -c "
import sys, json
data = json.load(sys.stdin)
content = data.get('choices', [{}])[0].get('message', {}).get('content', 'Summary generation failed')
print(content)
" > "$summary_file"

    if [ -s "$summary_file" ]; then
        local summary_lines=$(wc -l < "$summary_file")
        echo "✅ Summary: ${summary_lines} lines → $summary_file"
        echo ""
        echo "═══════════════════════════════════════"
        echo "  COACHING CALL SUMMARY — $(date +%F)"
        echo "═══════════════════════════════════════"
        cat "$summary_file"
    else
        echo "❌ Summarization failed"
        echo "Transcript is at: $transcript"
    fi

    # Clean up
    rm -f /tmp/coaching_prompt.txt
}

# ─── STATUS ───────────────────────────────────────────────────────────
cmd_status() {
    echo "=== Coaching Call Pipeline Status ==="
    echo ""
    
    # Check for active recording
    if pgrep -f "ffmpeg.*x11grab" > /dev/null 2>&1; then
        echo "🔴 Recording: ACTIVE"
        local pid=$(pgrep -f "ffmpeg.*x11grab" | head -1)
        echo "   PID: $pid"
    else
        echo "⚪ Recording: Not active"
    fi

    echo ""
    echo "=== Recent Recordings ==="
    ls -lht "$OUTPUT_DIR"/*_final.mp4 "$OUTPUT_DIR"/*.mkv 2>/dev/null | head -5
    
    echo ""
    echo "=== Recent Transcripts ==="
    ls -lht "$OUTPUT_DIR"/*_normalized.txt 2>/dev/null | head -5

    echo ""
    echo "=== Recent Summaries ==="
    ls -lht "$OUTPUT_DIR"/summary_*.md 2>/dev/null | head -5

    echo ""
    echo "=== GPU Status ==="
    nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv,noheader 2>/dev/null
}

# ─── MAIN ─────────────────────────────────────────────────────────────
case "${1:-status}" in
    record)
        cmd_record "${2:-90}"
        ;;
    process)
        cmd_process
        ;;
    full)
        # Record, then auto-process
        cmd_record "${2:-90}"
        echo ""
        echo "⏳ Recording complete — starting transcription + summarization..."
        cmd_process
        ;;
    status)
        cmd_status
        ;;
    *)
        echo "Usage: $0 {record|process|full|status} [duration_minutes]"
        echo ""
        echo "  record [90]   — Record screen+audio for N minutes"
        echo "  process       — Transcribe + summarize latest recording"
        echo "  full [90]     — Record then auto-process"
        echo "  status        — Check recording status and recent files"
        exit 1
        ;;
esac
