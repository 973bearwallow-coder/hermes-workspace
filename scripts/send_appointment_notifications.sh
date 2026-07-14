#!/usr/bin/env bash
set -euo pipefail

TOKEN_FILE="/home/tom/.hermes/cron/telegram_bot_token"
CHAT_ID_FILE="/home/tom/.hermes/cron/telegram_chat_id"
APPOINTMENTS_FILE="/home/tom/.hermes/cron/output/email_appointments.txt"

if [[ ! -f "$TOKEN_FILE" || ! -f "$CHAT_ID_FILE" ]]; then
  echo "Missing credential files" >&2
  exit 1
fi

TOKEN=$(cat "$TOKEN_FILE")
CHAT_ID=$(cat "$CHAT_ID_FILE")

send_notification() {
  local subject="$1"
  local sender="$2"
  local message="📅 Appointment email: ${subject} from ${sender}
Add to Google Calendar? (yes/no)"
  curl -G "https://api.telegram.org/bot${TOKEN}/sendMessage" \
    --data-urlencode "chat_id=${CHAT_ID}" \
    --data-urlencode "text=${message}" \
    --data "parse_mode=HTML" > /dev/null
}

# Process each line in appointments file
while IFS= read -r line || [[ -n $line ]]; do
  [[ -z "$line" ]] && continue
  # Try to extract subject and sender using Bash regex
  if [[ $line =~ 📅[[:space:]]*Appointment[[:space:]]*email:[[:space:]]*\'([^\']*)\'[[:space:]]*from[[:space:]]*([^\ ]+) ]]; then
    subject="${BASH_REMATCH[1]}"
    sender="${BASH_REMATCH[2]}"
  else
    # Fallback: extract everything between "from" and the end, trim
    sender=$(echo "$line" | sed -n 's/.*from *\\([^[:space:]]*\\).*/\\1/p')
    # Extract subject as the part before " from"
    subject=$(echo "$line" | sed -n 's/.*Appointment email:[[:space:]]*\\([^ ]*\\)[[:space:]]*from.*/\\1/p')
  fi
  send_notification "$subject" "$sender"
done < "$APPOINTMENTS_FILE"

# Clear the file after processing
> "$APPOINTMENTS_FILE"