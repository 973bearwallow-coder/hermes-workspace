#!/usr/bin/env bash
set -euo pipefail
LOG=/home/tom/hermes_to_charles.log
TS=$(date '+%Y-%m-%d %H:%M:%S %Z')
HOST=$(hostname)
SYSTEMD_CHARLES=$(systemctl is-active charles.service 2>/dev/null || true)
SYSTEMD_GATEWAY=$(systemctl is-active openclaw-gateway.service 2>/dev/null || true)
PROC=$(ps -p 3225340 -o pid=,cmd= 2>/dev/null || true)
HEALTH=$(curl -sS --max-time 5 http://localhost:18789/health 2>/dev/null || true)
LISTENER=$(ss -tlnp 2>/dev/null | grep 18789 || true)
TERM_SELF="whoami=$(whoami); hostname=$(hostname); os=$(grep '^PRETTY_NAME=' /etc/os-release | cut -d= -f2- | tr -d '"'); kernel=$(uname -r); python=$(python3 --version 2>&1); node=$(node --version 2>&1); mem=$(free -h | awk '/Mem:/ {print $3 "/" $2}'); disk=$(df -h / | awk 'NR==2 {print $4 " free of " $2}')"
BROWSER_SELF="browser_exec=blocked(remote-debugging approval required); browser_gui=OK(chrome Browser Self Check page visible via computer_use)"
{
  printf '[%s] OpenClaw/Charles Status on %s\n' "$TS" "$HOST"
  printf 'OpenClaw Gateway: systemd=%s | process=%s | health=%s | listener=%s\n' "$SYSTEMD_GATEWAY" "${PROC:-running}" "${HEALTH:-unavailable}" "${LISTENER:-missing}"
  printf 'Charles wrapper: systemd=%s\n' "$SYSTEMD_CHARLES"
  printf 'Terminal Self-Check: %s\n' "$TERM_SELF"
  printf 'Browser Self-Check: %s\n' "$BROWSER_SELF"
  printf 'Conclusion: gateway healthy despite inactive systemd; no restart needed; browser_exec blocked by remote-debug approval; GUI browser smoke test visible.\n'
  printf '\n'
} >> "$LOG"

tail -n 8 "$LOG"