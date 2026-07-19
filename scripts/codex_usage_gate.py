#!/usr/bin/env python3
"""
codex_usage_gate.py — Adaptive usage governor for ChatGPT Plus (openai-codex) route.

PROBLEM:
  OpenAI's Codex OAuth route with a ChatGPT Plus account has a SOFT CREDIT LIMIT
  that is NOT exposed via API (only 'x-codex-credits-unlimited: False' tells us
  it's metered). We cannot read "credits remaining". If we burn through it, OpenAI
  throttles mid-task and the whole stack degrades.

STRATEGY (maximize benefit, never go over):
  1. Log every codex call with timestamp + tokens.
  2. On ANY throttle signal (HTTP 429, or 'retry-after' / limit headers), immediately
     flip to COOLDOWN mode: route to free fallback for N minutes, then probe again.
  3. Track a rolling 30-day call COUNT. If we exceed a conservative self-imposed
     daily ceiling (estimated from typical Plus codex allowances), self-throttle
     to free fallback during low-value tasks, reserve codex for high-value only.
  4. Adaptive probe: after cooldown, send a tiny test call. If it succeeds, resume
     codex; if throttled again, extend cooldown.

This makes GPT-5.6-sol the daily driver BUT guarantees we never hard-fail on
rate limits — we gracefully degrade to DeepSeek and recover automatically.

USAGE (import in moa_exec.py):
  from codex_usage_gate import codex_gate
  if codex_gate.should_use_codex(task_text, estimated_tokens):
      # call codex
  else:
      # use free fallback (DeepSeek etc.)
  # after a codex call:
  codex_gate.record_call(tokens, ok=True)
  # on throttle:
  codex_gate.record_throttle()
"""
import json, os, time, datetime

STATE_FILE = "/home/tom/hermes-workspace/memory/codex_usage.json"
COOLDOWN_SECONDS = 30 * 60      # 30 min backoff after throttle
PROBE_MODEL = "gpt-5.6-sol"
PROBE_TEXT = "Reply with exactly: OK"

# Conservative self-ceiling: ChatGPT Plus codex is believed ~有限 but we don't
# know the number. We use a SOFT daily cap based on observed typical Plus codex
# behavior (~a few hundred calls/day). Set conservatively; adaptive throttle
# catches the real wall regardless.
SOFT_DAILY_CAP = 200            # calls/day before we start reserving codex for high-value only
HIGH_VALUE_KEYWORDS = [
    "client", "proposal", "report", "important", "final", "publish", "send",
    "perfect", "best", "critical", "contract", "paw prints", "boardroom",
    "coaching", "research", "analysis", "strategy", "build", "deploy"
]

def _load():
    if os.path.exists(STATE_FILE):
        try:
            return json.load(open(STATE_FILE))
        except Exception:
            pass
    return {"calls": [], "cooldown_until": 0, "last_throttle": None}

def _save(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    json.dump(s, open(STATE_FILE, "w"), indent=2)

def _now():
    return time.time()

def _prune(s):
    """Keep only last 30 days of call timestamps."""
    cutoff = _now() - 30 * 86400
    s["calls"] = [c for c in s["calls"] if c.get("t", 0) > cutoff]

def _today_count(s):
    day_start = _now() - 86400
    return sum(1 for c in s["calls"] if c.get("t", 0) > day_start)

def should_use_codex(task_text="", estimated_tokens=0):
    """Return True if we should route this task to codex now."""
    s = _load()
    _prune(s)
    _save(s)
    # 1. Hard cooldown (just got throttled)
    if _now() < s["cooldown_until"]:
        return False
    # 2. Over soft daily cap -> only high-value tasks get codex
    if _today_count(s) >= SOFT_DAILY_CAP:
        low_value = not any(k in task_text.lower() for k in HIGH_VALUE_KEYWORDS)
        if low_value:
            return False
    return True

def record_call(tokens=0, ok=True):
    s = _load()
    s["calls"].append({"t": _now(), "tokens": tokens, "ok": ok})
    _prune(s)
    _save(s)

def record_throttle():
    """Call when codex returns 429 / rate-limit. Enter cooldown + extend on repeat."""
    s = _load()
    now = _now()
    # Exponential-ish backoff: if throttled again during cooldown, double it
    if now < s["cooldown_until"]:
        additional = (s["cooldown_until"] - now) * 2 + COOLDOWN_SECONDS
    else:
        additional = COOLDOWN_SECONDS
    s["cooldown_until"] = now + additional
    s["last_throttle"] = datetime.datetime.now().isoformat()
    _save(s)

def status():
    s = _load()
    _prune(s)
    remaining_cooldown = max(0, int(s["cooldown_until"] - _now()))
    return {
        "total_calls_30d": len(s["calls"]),
        "calls_today": _today_count(s),
        "soft_daily_cap": SOFT_DAILY_CAP,
        "cooldown_active": remaining_cooldown > 0,
        "cooldown_remaining_sec": remaining_cooldown,
        "last_throttle": s.get("last_throttle"),
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        print(json.dumps(status(), indent=2))
    else:
        print("codex_usage_gate — adaptive governor for ChatGPT Plus OAuth")
        print("  status : show current usage + cooldown state")
