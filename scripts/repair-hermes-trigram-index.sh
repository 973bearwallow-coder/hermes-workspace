#!/usr/bin/env bash
set -Eeuo pipefail

DB=/home/tom/.hermes/state.db
STAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=/home/tom/.hermes/backups
BACKUP="$BACKUP_DIR/state-pre-trigram-rebuild-$STAMP.db"
LOG=/home/tom/hermes-workspace/logs/state-db-trigram-repair-$STAMP.log
mkdir -p "$BACKUP_DIR" "$(dirname "$LOG")"
exec > >(tee -a "$LOG") 2>&1

restart_gateway() {
  systemctl --user start hermes-gateway.service || true
}
trap restart_gateway EXIT

echo "[$(date -Is)] stopping hermes-gateway"
systemctl --user stop hermes-gateway.service

echo "[$(date -Is)] backing up $DB to $BACKUP"
sqlite3 "$DB" ".timeout 60000" ".backup '$BACKUP'"

echo "[$(date -Is)] rebuilding derived messages_fts_trigram index"
sqlite3 "$DB" ".timeout 60000" "INSERT INTO messages_fts_trigram(messages_fts_trigram) VALUES('rebuild');"

echo "[$(date -Is)] validating database"
CHECK=$(sqlite3 "$DB" "PRAGMA quick_check;")
printf '%s\n' "$CHECK"
if [[ "$CHECK" != "ok" ]]; then
  echo "[$(date -Is)] ERROR: quick_check did not return ok"
  exit 1
fi

COUNTS=$(sqlite3 "$DB" "SELECT (SELECT count(*) FROM messages) || '|' || (SELECT count(*) FROM messages_fts_trigram_content);")
echo "counts=$COUNTS"
LEFT=${COUNTS%%|*}; RIGHT=${COUNTS##*|}
if [[ "$LEFT" != "$RIGHT" ]]; then
  echo "[$(date -Is)] ERROR: canonical/index content counts differ"
  exit 1
fi

echo "[$(date -Is)] repair complete; backup=$BACKUP"
