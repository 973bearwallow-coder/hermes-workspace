#!/bin/bash
# Start the auto-memory capture daemon
# Run this at session start or via screen/tmux

SCRIPT="/home/tom/hermes-workspace/scripts/auto_memory_capture.py"
LOG="/home/tom/hermes-workspace/logs/memory_capture_daemon.log"
PIDFILE="/home/tom/hermes-workspace/logs/memory_capture.pid"

# Check if already running
if [ -f "$PIDFILE" ]; then
    OLD_PID=$(cat "$PIDFILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
        echo "Memory capture daemon already running (PID: $OLD_PID)"
        exit 0
    else
        rm -f "$PIDFILE"
    fi
fi

# Start the daemon (captures window activity every 5 minutes)
nohup python3.12 "$SCRIPT" --daemon 300 >> "$LOG" 2>&1 &
DAEMON_PID=$!
echo "$DAEMON_PID" > "$PIDFILE"
echo "Auto-memory capture daemon started (PID: $DAEMON_PID)"
echo "Logging to: $LOG"
