#!/bin/bash
# Watchdog: restart Hermes gateway if it becomes unresponsive
# Run via cron: */5 * * * * /home/tom/hermes-workspace/scripts/hermes-watchdog.sh

LOG="/tmp/hermes-watchdog.log"
HEALTH_URL="http://127.0.0.1:18789/health"
RESTART_CMD="hermes gateway restart"

echo "$(date): Watchdog check" >> "$LOG"

# Check if gateway responds
if ! curl -s --max-time 5 "$HEALTH_URL" > /dev/null 2>&1; then
    echo "$(date): Gateway unresponsive — restarting" >> "$LOG"
    $RESTART_CMD >> "$LOG" 2>&1
    sleep 10
    # Notify Tom via Telegram
    curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage?chat_id=7602246023&text=⚠️ Hermes gateway restarted by watchdog" > /dev/null 2>&1
fi
