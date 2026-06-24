#!/bin/bash
# Pet Community Intelligence Monitor
# Uses ddgs CLI to search for pet business content across the web.
# Run weekly via cron. Outputs are analyzed by the LLM in the cron prompt.

set -e

OUTPUT_DIR="/home/tom/Desktop/coaching_call/pet_community"
mkdir -p "$OUTPUT_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M)
RESULTS_FILE="$OUTPUT_DIR/intelligence_${TIMESTAMP}.txt"

echo "=== Pet Community Monitor — $(date) ===" > "$RESULTS_FILE"
echo "" >> "$RESULTS_FILE"

# Search queries — each run searches fresh (ddgs has no state, no need)
QUERIES=(
  "site:reddit.com r/doggrooming business tips"
  "site:reddit.com r/EtsySellers pet products"
  "site:reddit.com r/smallbusiness dog grooming"
  "dog grooming business tips pricing revenue 2025"
  "custom pet products Etsy print on demand marketing"
  "local pet business SEO marketing"
  "paw print merchandise custom dog products seller"
  "pet industry trends 2025 2026"
  "dog groomer local business advertising tips"
  "pet business ideas profitable 2025"
)

TOTAL=0
for i in "${!QUERIES[@]}"; do
  Q="${QUERIES[$i]}"
  NUM=$((i + 1))
  echo "[$NUM/${#QUERIES[@]}] $Q"
  
  # ddgs text outputs numbered results to stdout
  RESULT=$(ddgs text -q "$Q" -m 5 2>/dev/null || true)
  
  if [ -n "$RESULT" ]; then
    echo "--- Query $NUM: $Q ---" >> "$RESULTS_FILE"
    echo "$RESULT" >> "$RESULTS_FILE"
    echo "" >> "$RESULTS_FILE"
    
    # Count results (lines starting with number.)
    COUNT=$(echo "$RESULT" | grep -cE '^[0-9]+\.' || true)
    TOTAL=$((TOTAL + COUNT))
    echo "  Found: $COUNT results"
  else
    echo "  No results"
  fi
done

echo "" >> "$RESULTS_FILE"
echo "=== Summary ===" >> "$RESULTS_FILE"
echo "Total results: $TOTAL" >> "$RESULTS_FILE"

echo ""
echo "=== DONE ==="
echo "Results: $TOTAL"
echo "File: $RESULTS_FILE"
