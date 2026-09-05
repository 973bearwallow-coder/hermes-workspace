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

# After a reboot Linux may reuse the recorded gateway PID for an unrelated
# process. The CLI intentionally refuses to clear any lock whose PID exists,
# so handle only the provably stale reboot/PID-collision case here. The port
# and exact gateway-process checks above must both have passed first.
LOCK_DIR="$HERMES_HOME/tasks-v1.json.lock"
OWNER_FILE="$LOCK_DIR/owner.json"
if [ -f "$OWNER_FILE" ] && python3 - "$OWNER_FILE" <<'PY'
import json
import pathlib
import sys

owner = json.loads(pathlib.Path(sys.argv[1]).read_text())
pid = int(owner["pid"])
acquired = float(owner["acquiredAt"]) / 1000.0
boot_time = next(
    int(line.split()[1])
    for line in pathlib.Path("/proc/stat").read_text().splitlines()
    if line.startswith("btime ")
)
try:
    cmdline = pathlib.Path(f"/proc/{pid}/cmdline").read_bytes().replace(b"\0", b" ").decode(errors="replace")
except OSError:
    cmdline = ""

is_gateway = "hermes-live-testbed/dist/cli.js" in cmdline and " serve" in cmdline
raise SystemExit(0 if acquired < boot_time and not is_gateway else 1)
PY
then
  rm -f -- "$OWNER_FILE"
  rmdir -- "$LOCK_DIR"
  echo "Cleared stale pre-reboot task-store lock with reused owner PID"
fi

exec /usr/bin/node "$CLI" tasks unlock --confirm-no-gateway
