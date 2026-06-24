#!/bin/bash

LOG_FILE="/home/tom/hermes-workspace/logs/foreman_check.log"

timestamp() {
  date +"%Y-%m-%d %H:%M:%S"
}

log() {
  echo "$(timestamp) $1" >> "$LOG_FILE"
}

check_and_restart_user() {
  local service="$1"
  if ! systemctl --user is-active --quiet "$service"; then
    log "User service '$service' is down. Attempting restart..."
    systemctl --user restart "$service"
    if systemctl --user is-active --quiet "$service"; then
      log "User service '$service' restarted successfully."
    else
      log "FAILED to restart user service '$service'."
    fi
  else
    log "User service '$service' is running."
  fi
}

check_and_restart_system() {
  local service="$1"
  if ! systemctl is-active --quiet "$service"; then
    log "System service '$service' is down. Attempting restart..."
    sudo systemctl restart "$service"
    if systemctl is-active --quiet "$service"; then
      log "System service '$service' restarted successfully."
    else
      log "FAILED to restart system service '$service'."
    fi
  else
    log "System service '$service' is running."
  fi
}

check_and_restart_user "hermes-gateway"
check_and_restart_system "ollama"
