#!/bin/bash
# gemini_health_check.sh
# Checks if Gemini model is reachable; if not, switches to a free fallback model.

# ---- Configuration -------------------------------------------------
# Path to the Gemini API key (stored securely)
GEMINI_KEY_FILE="/home/tom/.hermes/api_keys/google_gemini.key"

# Fallback free model to switch to
FALLBACK_MODEL="nvidia/nemotron-3-nano-30b-a3b:free"

# Gemini model identifier as used in the config file
GEMINI_MODEL="gemini 2.5 flash"

# Log file for health‑check events
LOG_FILE="/home/tom/hermes/workspace/logs/gemini_health.log"

# Simple test payload
TEST_PAYLOAD='{"prompt":"Hello"}'

# ------------------------------------------------------------------- 
# Ensure the key file exists and is non-empty
if [ ! -f "$GEMINI_KEY_FILE" ] || [ ! -s "$GEMINI_KEY_FILE" ]; then
  echo "$(date): WARNING: Gemini API key file not found or empty, proceeding to fallback" >> "$LOG_FILE"
  # Switch to fallback model and restart gateway
  hermes config set model "$FALLBACK_MODEL"
  if [ $? -ne 0 ]; then
    echo "$(date): ERROR: Failed to set fallback model" >> "$LOG_FILE"
    exit 1
  fi
  systemctl --user restart openclaw-gateway.service
  if [ $? -ne 0 ]; then
    echo "$(date): ERROR: Failed to restart gateway" >> "$LOG_FILE"
    exit 1
  fi
  echo "$(date): Switched to fallback model $FALLBACK_MODEL and restarted gateway" >> "$LOG_FILE"
  exit 0
fi

API_KEY=$(cat "$GEMINI_KEY_FILE")

# Perform a lightweight request to the Gemini endpoint
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "$TEST_PAYLOAD" \
  "https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:predict")

# Log the outcome
if [ "$HTTP_STATUS" -ge 200 ] && [ "$HTTP_STATUS" -lt 300 ]; then
  echo "$(date): Gemini healthy (HTTP $HTTP_STATUS)" >> "$LOG_FILE"
  exit 0
else
  echo "$(date): Gemini unhealthy (HTTP $HTTP_STATUS) – switching to fallback" >> "$LOG_FILE"
  # Switch to the fallback model
  hermes config set model "$FALLBACK_MODEL"
  if [ $? -ne 0 ]; then
    echo "$(date): ERROR: Failed to set fallback model" >> "$LOG_FILE"
    exit 1
  fi
  systemctl --user restart openclaw-gateway.service
  if [ $? -ne 0 ]; then
    echo "$(date): ERROR: Failed to restart gateway" >> "$LOG_FILE"
    exit 1
  fi
  echo "$(date): Switched to fallback model $FALLBACK_MODEL and restarted gateway" >> "$LOG_FILE"
fi