#!/usr/bin/env python3
"""Wake the canonical Atlas session after the Hermes gateway starts.

The script waits for the loopback Sessions API, resumes the canonical session
through its lease-protected endpoint, and delivers the authoritative final
response to Tom's Telegram DM. It never logs credentials or SSE text.
"""

from __future__ import annotations

import argparse
import fcntl
import json
import math
import os
import re
import secrets
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import BinaryIO

HERMES_BASE = "http://127.0.0.1:8642"
SESSION_ID = "20260722_145434_7a2f78"
SESSION_KEY = "agent:main:telegram:dm:7602246023"
EXPECTED_PROVIDER = "openai-codex"
EXPECTED_MODEL = "gpt-5.6-sol"
TELEGRAM_TARGET = "telegram:7602246023"
ENV_PATH = Path("/home/tom/.hermes/.env")
STATE_PATH = Path("/home/tom/.hermes/restart-recovery-state.json")
LOCK_PATH = Path("/home/tom/.hermes/restart-recovery.lock")
LOG_PATH = Path("/home/tom/hermes-workspace/logs/atlas-post-restart-recovery.log")
HERMES_BIN = "/home/tom/.hermes/hermes-agent/venv/bin/hermes"
# Recovery gets one canonical-session turn. Repeated reasoning turns can hold the
# same lease used by live Telegram/voice traffic for minutes, so asynchronous
# work must be made durable by that first turn rather than polled through the
# user's active session.
MAX_RECOVERY_CYCLES = 1
TERMINAL_PATTERN = re.compile(r"(?m)^RECOVERY_TERMINAL:\s*(yes|no)\s*$", re.IGNORECASE)


class RecoveryError(RuntimeError):
    pass


def read_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def append_log(message: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] {message}\n")


def api_request(
    path: str,
    api_key: str,
    *,
    method: str = "GET",
    body: dict | None = None,
    timeout: float = 15,
) -> BinaryIO:
    url = HERMES_BASE + path
    payload = None if body is None else json.dumps(body).encode()
    headers = {"Authorization": f"Bearer {api_key}"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "text/event-stream"
        headers["X-Hermes-Session-Key"] = SESSION_KEY
    request = urllib.request.Request(url, data=payload, headers=headers, method=method)
    return urllib.request.urlopen(request, timeout=timeout)


def wait_for_api(api_key: str, timeout: float = 180) -> None:
    deadline = time.monotonic() + timeout
    last_error = "not attempted"
    encoded = urllib.parse.quote(SESSION_ID, safe="")
    while time.monotonic() < deadline:
        try:
            with api_request("/health", api_key, timeout=5) as response:
                health = json.load(response)
            if health.get("status") != "ok":
                raise RecoveryError("health endpoint did not report ok")
            with api_request(f"/api/sessions/{encoded}", api_key, timeout=10) as response:
                session_payload = json.load(response)
            session = session_payload.get("session", session_payload)
            if not isinstance(session, dict):
                raise RecoveryError("canonical session metadata was malformed")
            if session.get("id") != SESSION_ID:
                raise RecoveryError("canonical session metadata mismatch")
            if session.get("model") != EXPECTED_MODEL:
                raise RecoveryError("canonical session model mismatch")
            return
        except (OSError, ValueError, RecoveryError, urllib.error.URLError) as exc:
            last_error = type(exc).__name__
            time.sleep(2)
    raise RecoveryError(f"Sessions API was not ready after {timeout:.0f}s ({last_error})")


def parse_completed_sse(response: BinaryIO) -> dict:
    event_name = ""
    data_lines: list[str] = []
    completed: dict | None = None

    def consume() -> None:
        nonlocal completed, event_name, data_lines
        if not data_lines:
            event_name = ""
            return
        try:
            payload = json.loads("\n".join(data_lines))
        except json.JSONDecodeError as exc:
            raise RecoveryError("Hermes emitted malformed SSE JSON") from exc
        if event_name == "assistant.completed":
            completed = payload
        elif event_name == "error":
            error_type = payload.get("error_type", "HermesError")
            raise RecoveryError(f"Hermes recovery stream failed ({error_type})")
        event_name = ""
        data_lines = []

    for raw in response:
        line = raw.decode("utf-8", errors="strict").rstrip("\r\n")
        if not line:
            consume()
        elif line.startswith("event:"):
            event_name = line[6:].strip()
        elif line.startswith("data:"):
            data_lines.append(line[5:].lstrip())
    consume()
    if completed is None:
        raise RecoveryError("Hermes recovery stream ended without assistant.completed")
    runtime = completed.get("runtime") or {}
    if runtime.get("provider") != EXPECTED_PROVIDER or runtime.get("model") != EXPECTED_MODEL:
        raise RecoveryError("Hermes recovery authority mismatch")
    content = completed.get("content")
    if not isinstance(content, str) or not content.strip():
        raise RecoveryError("Hermes recovery returned no final user-facing content")
    return completed


def recovery_prompt(recovery_id: str, cycle: int) -> str:
    return f"""POST-RESTART RECOVERY EVENT {recovery_id}
Recovery cycle: {cycle} of {MAX_RECOVERY_CYCLES}.
The Hermes gateway has restarted. This is an autonomous wake-up for the continuing canonical Atlas session, not a user request.

Inspect the immediately preceding session context and durable cron-run history. If an explicitly in-progress task or interrupted one-shot job remains unfinished, safely continue it from verified state. Never repeat a completed side effect. Do not restart or stop the Hermes gateway. Do not modify credentials, accounts, SSH, encryption, boot settings, or expose services beyond their existing interfaces. If there is no unfinished work, perform no changes.

Diagnose and fix failures rather than merely reporting them. Do not call work complete while a timer, service, cron run, delegated task, or background process launched for this recovery is still pending. If work must continue asynchronously, make it durable and return RECOVERY_TERMINAL: no; the recovery service will then defer without injecting another turn into Tom's live session. Return RECOVERY_TERMINAL: yes only when all recovered work is complete, or when a concrete blocker genuinely requires Tom.

Return a concise status for Tom stating whether work was resumed, completed, blocked, or there was nothing to resume. Include this recovery event ID. Do not ask Tom to nudge Atlas merely because the gateway restarted. End with exactly one machine-readable line:
RECOVERY_TERMINAL: yes
or
RECOVERY_TERMINAL: no"""


def run_recovery(api_key: str, recovery_id: str, cycle: int) -> str:
    encoded = urllib.parse.quote(SESSION_ID, safe="")
    body = {
        "message": recovery_prompt(recovery_id, cycle),
        "provider": EXPECTED_PROVIDER,
        "model": EXPECTED_MODEL,
        "require_model_lock": True,
        "include_diagnostics": True,
    }
    with api_request(
        f"/api/sessions/{encoded}/chat/stream",
        api_key,
        method="POST",
        body=body,
        timeout=900,
    ) as response:
        completed = parse_completed_sse(response)
    return completed["content"].strip()


def parse_recovery_status(final: str) -> tuple[str, bool]:
    matches = list(TERMINAL_PATTERN.finditer(final))
    terminal = bool(matches and matches[-1].group(1).lower() == "yes")
    cleaned = TERMINAL_PATTERN.sub("", final).strip()
    return cleaned, terminal


def send_telegram(message: str) -> None:
    result = subprocess.run(
        [HERMES_BIN, "send", "--quiet", "--to", TELEGRAM_TARGET, message],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
        env={**os.environ, "HERMES_HOME": "/home/tom/.hermes"},
    )
    if result.returncode != 0:
        raise RecoveryError(f"Telegram delivery failed (exit {result.returncode})")


def read_state() -> dict:
    try:
        state = json.loads(STATE_PATH.read_text())
        return state if isinstance(state, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def write_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary = STATE_PATH.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    os.chmod(temporary, 0o600)
    temporary.replace(STATE_PATH)


def self_test() -> None:
    import io

    sample = (
        b"event: diagnostic.timing\n"
        b'data: {"stage":"provider.completed","elapsed_seconds":1.0}\n\n'
        b"event: assistant.completed\n"
        b'data: {"content":"Recovered","runtime":{"provider":"openai-codex","model":"gpt-5.6-sol"}}\n\n'
    )
    parsed = parse_completed_sse(io.BytesIO(sample))
    assert parsed["content"] == "Recovered"
    cleaned, terminal = parse_recovery_status("Recovered\nRECOVERY_TERMINAL: yes")
    assert cleaned == "Recovered" and terminal is True
    _, terminal = parse_recovery_status("Still running\nRECOVERY_TERMINAL: no")
    assert terminal is False
    assert MAX_RECOVERY_CYCLES == 1
    assert SESSION_ID in f"/api/sessions/{SESSION_ID}"
    assert math.isfinite(1.0)
    print("self-test: ok")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true", help="verify prerequisites without running Atlas")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0

    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    lock_handle = LOCK_PATH.open("w")
    try:
        fcntl.flock(lock_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        append_log("another recovery invocation is already active; exiting")
        return 0

    env = read_env(ENV_PATH)
    api_key = env.get("API_SERVER_KEY", "").strip()
    if not api_key:
        raise RecoveryError("API_SERVER_KEY is unavailable")

    wait_for_api(api_key)
    if args.probe:
        append_log("probe passed: health, auth, canonical session, and model verified")
        print("probe: ok")
        return 0

    state = read_state()
    recovery_id = state.get("pending_recovery_id")
    if not isinstance(recovery_id, str) or not recovery_id:
        recovery_id = f"restart-{time.strftime('%Y%m%dT%H%M%S')}-{secrets.token_hex(4)}"
    write_state(
        {
            "pending_recovery_id": recovery_id,
            "status": "running",
            "started_at": time.time(),
        }
    )
    starting_cycle = state.get("cycle", 1) if state.get("status") == "failed" else 1
    if not isinstance(starting_cycle, int) or not 1 <= starting_cycle <= MAX_RECOVERY_CYCLES:
        starting_cycle = 1
    append_log(f"{recovery_id}: Sessions API healthy; waking canonical Atlas session")
    cycle = starting_cycle
    try:
        terminal = False
        for cycle in range(starting_cycle, MAX_RECOVERY_CYCLES + 1):
            write_state(
                {
                    "pending_recovery_id": recovery_id,
                    "status": "running",
                    "cycle": cycle,
                    "started_at": time.time(),
                }
            )
            append_log(f"{recovery_id}: starting recovery cycle {cycle}")
            final = run_recovery(api_key, recovery_id, cycle)
            message, terminal = parse_recovery_status(final)
            if message:
                send_telegram(message)
            append_log(
                f"{recovery_id}: cycle {cycle} completed; terminal={'yes' if terminal else 'no'}"
            )
            if terminal:
                break
        if not terminal:
            write_state(
                {
                    "last_recovery_id": recovery_id,
                    "status": "deferred",
                    "cycle": cycle,
                    "deferred_at": time.time(),
                }
            )
            append_log(
                f"{recovery_id}: deferred after one non-terminal cycle; "
                "no canonical-session polling"
            )
            return 0
    except Exception as exc:
        write_state(
            {
                "pending_recovery_id": recovery_id,
                "status": "failed",
                "cycle": cycle,
                "failed_at": time.time(),
                "error_type": type(exc).__name__,
            }
        )
        append_log(f"{recovery_id}: failed ({type(exc).__name__})")
        try:
            send_telegram(
                f"Atlas gateway restarted, but automatic session recovery failed "
                f"({type(exc).__name__}; event {recovery_id}). Your next message will wake me normally."
            )
        except Exception:  # noqa: BLE001 - fallback must never mask the original failure
            append_log(f"{recovery_id}: fallback Telegram delivery also failed")
        raise

    write_state(
        {
            "last_recovery_id": recovery_id,
            "status": "completed",
            "completed_at": time.time(),
        }
    )
    append_log(f"{recovery_id}: completed and delivered to Telegram")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001 - systemd boundary records a safe summary
        print(
            f"atlas post-restart recovery failed: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(1) from None
