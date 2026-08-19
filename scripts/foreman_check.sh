#!/bin/bash
# foreman_check.sh - Health check and auto-restart for all AI services
# Runs every 5 minutes via systemd timer

set -euo pipefail

LOGFILE="/home/tom/hermes-workspace/logs/foreman_check.log"
ALERTFILE="/home/tom/hermes-workspace/logs/voice_alert.json"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOGFILE"
}

ensure_log_dir() {
    mkdir -p "$(dirname "$LOGFILE")"
}

check_user_service() {
    local service_name="$1"
    local status
    status=$(sudo -u tom XDG_RUNTIME_DIR=/run/user/1000 systemctl --user is-active "$service_name" 2>/dev/null || echo "inactive")
    
    if [ "$status" != "active" ]; then
        log "WARNING: $service_name is $status - attempting restart (user-level)"
        if sudo -u tom XDG_RUNTIME_DIR=/run/user/1000 systemctl --user restart "$service_name" 2>/dev/null; then
            sleep 2
            if sudo -u tom XDG_RUNTIME_DIR=/run/user/1000 systemctl --user is-active --quiet "$service_name"; then
                log "SUCCESS: $service_name restarted (user-level)"
                return 0
            fi
        fi
        log "ERROR: Failed to restart $service_name"
        return 1
    else
        log "OK: $service_name is running"
        return 0
    fi
}

check_system_service() {
    local service_name="$1"
    local status
    status=$(systemctl is-active "$service_name" 2>/dev/null || echo "inactive")
    
    if [ "$status" != "active" ]; then
        log "WARNING: $service_name is $status - attempting restart (system-level)"
        if sudo systemctl restart "$service_name" 2>/dev/null; then
            sleep 2
            if sudo systemctl is-active --quiet "$service_name"; then
                log "SUCCESS: $service_name restarted (system-level)"
                return 0
            fi
        fi
        log "ERROR: Failed to restart $service_name"
        return 1
    else
        log "OK: $service_name is running"
        return 0
    fi
}

check_voice_service() {
    local service_name="$1"
    local status
    status=$(sudo -u tom XDG_RUNTIME_DIR=/run/user/1000 systemctl --user is-active "$service_name" 2>/dev/null || echo "inactive")
    if [ "$status" != "active" ]; then
        log "VOICE ALERT: $service_name is $status - leaving it untouched while a live call may be attached"
        python3 - "$ALERTFILE" "$service_name" "$status" <<'PY'
import json, sys, time
path, service, status = sys.argv[1:]
try:
    data = json.load(open(path))
except Exception:
    data = {}
data.update({"active": False, "service": service, "status": status,
             "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
             "message": "Voice service stopped; manual/transport-safe recovery required."})
with open(path, "w") as f:
    json.dump(data, f, indent=2)
PY
        return 1
    fi
    return 0
}

# Main execution
ensure_log_dir
log "=== Starting foreman health check ==="

exit_code=0

# Check OpenClaw node host (user-level)
check_user_service "openclaw-node.service" || exit_code=1

# Check Hermes gateway (user-level)
check_user_service "hermes-gateway.service" || exit_code=1

# Check Charles orchestrator (system-level, idle marker)
check_system_service "charles.service" || exit_code=1

# Voice lane checks are detection-only. The live-transport guard deliberately
# prevents Foreman from restarting these services underneath an attached call.
for voice_service in atlas-voice-worker.service atlas-voice-gateway.service atlas-voice-web.service; do
    check_voice_service "$voice_service" || exit_code=1
done

if [ "$exit_code" -eq 0 ] && [ -f "$ALERTFILE" ]; then
    python3 - "$ALERTFILE" <<'PY'
import json, sys, time
path = sys.argv[1]
try: data = json.load(open(path))
except Exception: data = {}
data.update({"active": True, "status": "recovered", "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z")})
with open(path, "w") as f: json.dump(data, f, indent=2)
PY
fi

# Check Ollama (system-level) — DISABLED: voice co-worker now uses a local
# brain (qwen3:4b) on the 3090; ollama squatting VRAM starved chatterbox TTS.
# Leave ollama off so the co-worker has headroom. (2026-07-14)
# check_system_service "ollama" || exit_code=1

log "=== Foreman health check complete (exit: $exit_code) ==="
exit $exit_code
