#!/usr/bin/env bash
#
# Blocker Escalation Watchdog
# Monitors system logs for critical errors and creates an escalation
# notification file that can be routed to a sub‑agent or human.
#
# Usage: run continuously (e.g. via systemd or cron) or invoke manually.
#
# Configure the LOG FILE and ERROR PATTERNS below as needed.

# ---- Configuration -------------------------------------------------
LOG_FILE="/var/log/syslog"                     # file to monitor
ERROR_PATTERN="error|fail|panic|critical"      # regex for critical lines
ESCALATION_FILE="/home/tom/hermes-workspace/memory/coaching-calls/blocker_escalation.txt"
# -------------------------------------------------------------------

# Ensure escalation file exists
touch "$ESCALATION_FILE"

# Append a timestamped entry if any new error lines are found
if tail -n +0 -n 1000 "$LOG_FILE" 2>/dev/null | grep -iE "$ERROR_PATTERN" >>"$ESCALATION_FILE"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Blocked error logged." >>"$ESCALATION_FILE"
fi

# Optional: rotate the escalation file weekly (simple approach)
# You can extend this script with logrotate or keep it minimal.