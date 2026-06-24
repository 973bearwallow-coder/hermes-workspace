#!/bin/bash
# Pre-call setup for coaching calls
# 1. Find Meet link from calendar
# 2. If not found, check recent email for Meet link
# 3. Open Meet in Chrome so audio captures on charles
# 4. Start recording

export DISPLAY=:1
export XDG_RUNTIME_DIR=/run/user/1000

OUTPUT_DIR="/home/tom/Desktop/coaching_call"
mkdir -p "$OUTPUT_DIR"

echo "=== Pre-Call Setup $(date) ==="

# Step 1: Try to find Meet link from calendar
echo "[1/3] Checking calendar for Meet link..."
MEET_LINK=$(python3 /home/tom/hermes-workspace/scripts/find_meeting_link.py --hours 24 --keyword "coaching" 2>/dev/null)

if [ -z "$MEET_LINK" ]; then
    # Try broader keywords
    for kw in "call" "meet" "boardroom" "profit"; do
        MEET_LINK=$(python3 /home/tom/hermes-workspace/scripts/find_meeting_link.py --hours 24 --keyword "$kw" 2>/dev/null)
        if [ -n "$MEET_LINK" ]; then
            echo "Found with keyword '$kw': $MEET_LINK"
            break
        fi
    done
fi

if [ -z "$MEET_LINK" ]; then
    echo "⚠️ No Meet link found in calendar"
    echo "Checking email for recent Meet invites..."
    
    # Step 2: Check recent email for Meet link
    # Using gws or himalaya to search recent emails
    if command -v himalaya &>/dev/null; then
        MEET_LINK=$(himalaya search "meet.google.com" --max 5 2>/dev/null | grep -oP 'https://meet\.google\.com/[a-z0-9-]+' | head -1)
    fi
    
    if [ -n "$MEET_LINK" ]; then
        echo "Found in email: $MEET_LINK"
    else
        echo "❌ No Meet link found anywhere"
        echo "Recording will still start — make sure to open Meet manually"
        echo "SAVE_LINK_NOW" > "$OUTPUT_DIR/need_link.flag"
    fi
fi

if [ -n "$MEET_LINK" ]; then
    echo "✅ Meet link: $MEET_LINK"
    echo "$MEET_LINK" > "$OUTPUT_DIR/current_meet_link.txt"
    
    # Step 3: Open Meet in Chrome
    echo "[2/3] Opening Meet in Chrome..."
    # Use google-chrome directly (needs to run as tom with display)
    nohup google-chrome --no-first-run --disable-default-apps "$MEET_LINK" &
    CHROME_PID=$!
    echo "Chrome PID: $CHROME_PID"
    
    # Wait for Chrome to load
    echo "[3/3] Waiting 30s for Chrome to load Meet page..."
    sleep 30
fi

# Step 4: Start recording (always runs)
echo ""
echo "=== Starting recording ==="
bash /home/tom/hermes-workspace/scripts/coaching_call_record.sh 5400 "$(date +%Y%m%d_%H%M)" &
REC_PID=$!
echo "Recording setup complete. PID: $REC_PID"
echo "Meet link saved to: $OUTPUT_DIR/current_meet_link.txt"
