#!/bin/bash
# Backup Google OAuth tokens to a secondary location
# Also refreshes tokens to keep them active

BACKUP_DIR="/home/tom/.hermes/google/backups"
mkdir -p "$BACKUP_DIR"

# Refresh both tokens first
/home/tom/.hermes/hermes-agent/venv/bin/python3 /home/tom/hermes-workspace/scripts/google_token_manager.py personal refresh 2>/dev/null
/home/tom/.hermes/hermes-agent/venv/bin/python3 /home/tom/hermes-workspace/scripts/google_token_manager.py atlas refresh 2>/dev/null

# Backup with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cp /home/tom/.hermes/google/token.json "$BACKUP_DIR/token_$TIMESTAMP.json"
cp /home/tom/.hermes/google/atlas_token.json "$BACKUP_DIR/atlas_token_$TIMESTAMP.json"

# Keep only last 10 backups
ls -t "$BACKUP_DIR"/token_*.json 2>/dev/null | tail -n +11 | xargs rm -f
ls -t "$BACKUP_DIR"/atlas_token_*.json 2>/dev/null | tail -n +11 | xargs rm -f

# Secure permissions
chmod 600 "$BACKUP_DIR"/*.json 2>/dev/null

echo "✅ Tokens refreshed and backed up at $TIMESTAMP"
