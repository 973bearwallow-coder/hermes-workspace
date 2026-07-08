#!/bin/bash
# monitor_gemini_usage.sh
# Checks Gemini usage and emits a warning if the free‑tier quota is >=80% used.

# Path to a simple usage file that the usage‑tracker will update.
USAGE_LOG="/home/tom/.hermes/usage/gemini_usage.log"
MAX=250   # free‑tier daily limit for Gemini (requests)

# ----------------------------------------------------------------------
# Initialise the usage file if it does not exist, ensuring directory exists.
if [ ! -f "$USAGE_LOG" ]; then
  mkdir -p "$(dirname "$USAGE_LOG")"
  echo "used=0" > "$USAGE_LOG"
  echo "limit=250" >> "$USAGE_LOG"
fi

# ----------------------------------------------------------------------
# Parse the usage values.
USED=$(grep -Eo 'used=[0-9]+' "$USAGE_LOG" | cut -d= -f2 || echo 0)
LIM=$(grep -Eo 'limit=[0-9]+' "$USAGE_LOG" | cut -d= -f2 || echo $MAX)

# Guard against division by zero.
if [ -z "$LIM" ] || [ "$LIM" -le 0 ]; then
  LIM=$MAX
fi

# Calculate integer percentage.
PCT=$(( USED * 100 / LIM ))

# ----------------------------------------------------------------------
# Emit a warning if we are at or above 80% of the quota.
if [ "$PCT" -ge 80 ]; then
  echo "⚠️ Gemini usage: $USED/$LIM requests ($PCT%). Approaching free‑tier limit."
fi