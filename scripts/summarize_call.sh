#!/bin/bash
# Coaching call summarizer
# Usage: bash summarize_call.sh <transcript_file>

TRANSCRIPT="$1"
OUTPUT_DIR="/home/tom/Desktop/coaching_call"
DATE=$(date +%Y-%m-%d)

if [ -z "$TRANSCRIPT" ] || [ ! -f "$TRANSCRIPT" ]; then
  echo "Usage: $0 <transcript_file>"
  exit 1
fi

echo "=== Coaching Call Summary ===" > "$OUTPUT_DIR/summary_${DATE}.md"
echo "Date: $DATE" >> "$OUTPUT_DIR/summary_${DATE}.md"
echo "" >> "$OUTPUT_DIR/summary_${DATE}.md"

# Word count
WORDS=$(wc -w < "$TRANSCRIPT")
echo "**Transcript length:** $WORDS words" >> "$OUTPUT_DIR/summary_${DATE}.md"
echo "" >> "$OUTPUT_DIR/summary_${DATE}.md"

echo "Summary written to $OUTPUT_DIR/summary_${DATE}.md"
