#!/bin/bash
# atlas_watchdog.sh — Charles-side watchdog for Atlas (Hermes on Vision)
# Place on Charles: /home/tom/hermes-workspace/scripts/atlas_watchdog.sh
# Schedule via cron: */5 * * * * /home/tom/hermes-workspace/scripts/atlas_watchdog.sh

LOG="/home/tom/hermes-workspace/logs/atlas_watchdog.log"
VISION_IP="192.168.1.33"  # Adjust to Vision's real IP
GATEWAY_PORT="18789"
HEALTH_URL="http://${VISION_IP}:${GATEWAY_PORT}/health"
MAX_RESPONSE_SEC=10

timestamp() { date '+%Y-%m-%d %H:%M:%S'; }
log() { echo "$(timestamp) $1" | tee -a "$LOG"; }

mkdir -p "$(dirname "$LOG")"

log "=== Checking Atlas health ==="

# Step 1: Check if Vision host is reachable
if ! ping -c 1 -W 3 "$VISION_IP" &>/dev/null; then
    log "FAIL: Vision host ($VISION_IP) is unreachable — may be powered off"
    exit 1
fi
log "OK: Vision host reachable"

# Step 2: Check gateway health endpoint
HTTP_CODE=$(curl -sf -o /dev/null -w "%{http_code}" --max-time "$MAX_RESPONSE_SEC" "$HEALTH_URL" 2>/dev/null || echo "000")

if [ "$HTTP_CODE" = "200" ]; then
    log "OK: Atlas gateway healthy"
else
    log "FAIL: Gateway HTTP $HTTP_CODE — restarting via SSH"
    if ssh -o ConnectTimeout=5 vision "systemctl --user restart openclaw-gateway.service" 2>/dev/null; then
        sleep 5
        HTTP_CODE2=$(curl -sf -o /dev/null -w "%{http_code}" --max-time "$MAX_RESPONSE_SEC" "$HEALTH_URL" 2>/dev/null || echo "000")
        if [ "$HTTP_CODE2" = "200" ]; then
            log "SUCCESS: Gateway restarted and healthy"
        else
            log "WARN: Still unhealthy after restart (HTTP $HTTP_CODE2)"
        fi
    else
        log "ERROR: Cannot SSH to Vision"
    fi
fi

log "=== Check complete ==="
