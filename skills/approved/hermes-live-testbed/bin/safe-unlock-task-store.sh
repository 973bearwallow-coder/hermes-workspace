#!/usr/bin/env bash
set -euo pipefail

PORT=8789
CLI=/home/tom/hermes-workspace/skills/approved/hermes-live-testbed/dist/cli.js

if ss -ltnH "sport = :${PORT}" | grep -q .; then
  echo "Refusing stale-lock cleanup: port ${PORT} already has a listener." >&2
  exit 1
fi

if pgrep -u "$(id -u)" -f '/home/tom/hermes-workspace/skills/approved/hermes-live-testbed/dist/[c]li.js serve' >/dev/null; then
  echo "Refusing stale-lock cleanup: another Hermes Live gateway process exists." >&2
  exit 1
fi

exec /usr/bin/node "$CLI" tasks unlock --confirm-no-gateway
