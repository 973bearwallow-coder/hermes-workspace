#!/bin/bash
# foreman_check.sh - Health check and auto-restart for all AI services
# Runs every 5 minutes via systemd timer

set -euo pipefail

LOGFILE="/home/tom/hermes-workspace/logs/foreman_check.log"
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

# Check Ollama (system-level) — DISABLED: voice co-worker now uses a local
# brain (qwen3:4b) on the 3090; ollama squatting VRAM starved chatterbox TTS.
# Leave ollama off so the co-worker has headroom. (2026-07-14)
# check_system_service "ollama" || exit_code=1

log "=== Foreman health check complete (exit: $exit_code) ==="
exit $exit_code
