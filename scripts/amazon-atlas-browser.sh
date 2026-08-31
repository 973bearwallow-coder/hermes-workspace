#!/usr/bin/env bash
set -euo pipefail

PROFILE_DIR="${HOME}/.local/share/atlas-amazon-chrome"
DEBUG_PORT="9224"

mkdir -p "$PROFILE_DIR"
chmod 700 "$PROFILE_DIR"

exec /usr/bin/google-chrome \
  --user-data-dir="$PROFILE_DIR" \
  --profile-directory=Default \
  --remote-debugging-address=127.0.0.1 \
  --remote-debugging-port="$DEBUG_PORT" \
  --no-first-run \
  --no-default-browser-check \
  --disable-sync \
  --disable-features=OptimizationHints,AutofillServerCommunication \
  --new-window "https://www.amazon.com/"
