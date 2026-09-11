#!/usr/bin/env python3
"""Read the live ChatGPT/Codex subscription allowance safely.

Makes one minimal Sol request through the existing OAuth credential, then prints
only plan and rate-limit metadata. It never prints or modifies credentials.
"""
import json
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

AUTH = Path.home() / ".hermes" / "auth.json"
URL = "https://chatgpt.com/backend-api/codex/responses"


def fmt_reset(epoch: str) -> str:
    try:
        return datetime.fromtimestamp(int(epoch), ZoneInfo("America/New_York")).strftime(
            "%Y-%m-%d %I:%M %p %Z"
        )
    except (TypeError, ValueError, OSError):
        return "unknown"


def main() -> None:
    data = json.loads(AUTH.read_text())
    creds = data.get("credential_pool", {}).get("openai-codex", [])
    active = next((c for c in creds if c.get("is_active")), None)
    if active is None and creds:
        active = sorted(creds, key=lambda c: c.get("priority", 0))[0]
    if not active:
        raise SystemExit("No openai-codex OAuth credential found")

    payload = {
        "model": "gpt-5.6-sol",
        "instructions": "Reply with OK.",
        "input": [{"role": "user", "content": [{"type": "input_text", "text": "OK"}]}],
        "store": False,
        "stream": True,
    }
    headers = {
        "Authorization": f"Bearer {active['access_token']}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
        "originator": "codex_cli_rs",
        "ChatGPT-Account-ID": active.get("account_id", ""),
    }
    request = urllib.request.Request(URL, data=json.dumps(payload).encode(), headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            response.read()
            h = response.headers
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"Quota probe failed: HTTP {exc.code}") from exc

    print(f"plan={h.get('x-codex-plan-type', 'unknown')}")
    print(f"weekly_used_percent={h.get('x-codex-primary-used-percent', 'unknown')}")
    print(f"weekly_resets={fmt_reset(h.get('x-codex-primary-reset-at'))}")
    print(f"secondary_used_percent={h.get('x-codex-secondary-used-percent', 'not_reported')}")
    print(f"secondary_resets={fmt_reset(h.get('x-codex-secondary-reset-at'))}")
    print(f"credits_unlimited={h.get('x-codex-credits-unlimited', 'unknown')}")
    print(f"credits_balance={h.get('x-codex-credits-balance', '0')}")


if __name__ == "__main__":
    main()
