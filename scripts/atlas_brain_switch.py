#!/usr/bin/env python3
"""
atlas_brain_switch.py — Manages Atlas's own reasoning model (the agent loop),
NOT the MoA task-execution stack.

CONTEXT:
  - Atlas's default brain is set in ~/.hermes/config.yaml (profile: default)
  - Currently: tencent/hy3:free (expires 2026-07-21)
  - Plan: on Jul 21, switch default -> deepseek/deepseek-v4-flash (free, stable)
  - For HIGH-REASONING tasks, Atlas can escalate its OWN brain to the ChatGPT
    Plus OAuth route (gpt-5.6-sol via openai-codex) — $0 marginal, already paid.

This script:
  1. switch_to_flash()  — called by the Jul 21 cron; flips config to DeepSeek V4 Flash
  2. escalate_check(task_text, recent_complexity) — decides if Atlas should use
     codex brain for THIS reasoning task (based on keywords + self-tracked load)
  3. record_brain_usage() — logs each reasoning call so we self-regulate and
     never blow the codex credit limit before month-end

USAGE (imported byAtlas's own loop or called by cron):
  python3 atlas_brain_switch.py switch-to-flash
  python3 atlas_brain_switch.py status
"""
import json, os, sys, time, datetime, subprocess

CONFIG = "/home/tom/.hermes/config.yaml"
STATE_FILE = "/home/tom/hermes-workspace/memory/atlas_brain_state.json"
FLASH_MODEL = "deepseek/deepseek-v4-flash"
CODEX_MODEL = "openai-codex/gpt-5.6-sol"
HY3_MODEL = "tencent/hy3:free"
HY3_EXPIRY = datetime.date(2026, 7, 21)

# Reasoning-escalation keywords: when Atlas's OWN thinking needs more horsepower
REASONING_KEYWORDS = [
    "architect", "design", "strategy", "reasoning", "complex", "debug", "analyze",
    "synthesis", "tradeoff", "optimize", "plan", "research", "why", "hypothesis",
    "evaluate", "compare", "diagnose", "root cause", "decision", "framework",
]

def _load_state():
    if os.path.exists(STATE_FILE):
        try:
            return json.load(open(STATE_FILE))
        except Exception:
            pass
    return {"codex_brain_calls": [], "last_switch": None, "escalations_today": 0}

def _save_state(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    json.dump(s, open(STATE_FILE, "w"), indent=2)

def current_model():
    import yaml
    c = yaml.safe_load(open(CONFIG))
    return c.get("model", {}).get("default", "unknown")

def switch_to_flash():
    """Flip Atlas's default brain to DeepSeek V4 Flash. Called by Jul 21 cron."""
    try:
        subprocess.run(
            ["hermes", "config", "set", "model", FLASH_MODEL],
            check=True, capture_output=True, text=True
        )
        s = _load_state()
        s["last_switch"] = datetime.datetime.now().isoformat()
        s["switched_from"] = HY3_MODEL
        s["switched_to"] = FLASH_MODEL
        _save_state(s)
        return f"✅ Atlas brain switched to {FLASH_MODEL}"
    except subprocess.CalledProcessError as e:
        return f"❌ switch failed: {e.stderr}"

def should_escalate_brain(task_text, complexity_score=0):
    """Return True if Atlas should use codex brain (gpt-5.6-sol) for THIS reasoning.
    Self-regulating: if we've used codex brain heavily today, conserve."""
    s = _load_state()
    # Prune to today
    today = time.time() - 86400
    s["codex_brain_calls"] = [t for t in s["codex_brain_calls"] if t > today]
    _save_state(s)
    calls_today = len(s["codex_brain_calls"])

    # Soft self-cap: don't use codex brain more than ~15 reasoning calls/day
    # (reserves the $20/mo sub for when it truly matters, survives the month)
    if calls_today >= 15:
        return False

    t = task_text.lower()
    keyword_hit = any(k in t for k in REASONING_KEYWORDS)
    return keyword_hit or complexity_score >= 7

def record_codex_brain_call():
    s = _load_state()
    s["codex_brain_calls"].append(time.time())
    _save_state(s)

def status():
    s = _load_state()
    today = time.time() - 86400
    calls_today = sum(1 for t in s["codex_brain_calls"] if t > today)
    return {
        "current_brain": current_model(),
        "hy3_expiry": HY3_EXPIRY.isoformat(),
        "days_until_hy3_expiry": (HY3_EXPIRY - datetime.date.today()).days,
        "codex_brain_calls_today": calls_today,
        "codex_brain_soft_cap": 15,
        "last_switch": s.get("last_switch"),
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "switch-to-flash":
            print(switch_to_flash())
        elif cmd == "status":
            print(json.dumps(status(), indent=2))
        else:
            print(f"unknown command: {cmd}")
    else:
        print("usage: atlas_brain_switch.py [switch-to-flash|status]")
