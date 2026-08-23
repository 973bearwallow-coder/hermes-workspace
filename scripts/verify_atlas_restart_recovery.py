#!/usr/bin/env python3
import json
import subprocess
import time
from pathlib import Path

STATE = Path('/home/tom/.hermes/restart-recovery-state.json')
LOG = Path('/home/tom/hermes-workspace/logs/atlas-post-restart-recovery.log')
HERMES = '/home/tom/.hermes/hermes-agent/venv/bin/hermes'
TARGET = 'telegram:7602246023'

try:
    state = json.loads(STATE.read_text())
except (OSError, json.JSONDecodeError):
    state = {}
status = state.get('status', 'missing')
recovery_id = state.get('last_recovery_id') or state.get('pending_recovery_id') or 'unknown'
completed_at = state.get('completed_at')
recent = isinstance(completed_at, (int, float)) and time.time() - completed_at < 900
if status == 'completed' and recent:
    message = f'Restart recovery loop test passed and reached terminal state automatically. Event {recovery_id}.'
    exit_code = 0
else:
    message = (
        f'Restart recovery loop test did not reach terminal state within the verification window '
        f'(status={status}, event={recovery_id}). Atlas preserved logs at {LOG}.'
    )
    exit_code = 1
result = subprocess.run(
    [HERMES, 'send', '--quiet', '--to', TARGET, message],
    capture_output=True,
    text=True,
    timeout=60,
    check=False,
)
raise SystemExit(exit_code if result.returncode == 0 else 2)
