#!/usr/bin/env python3
"""
brain_picker.py — Daily "best free brain" detector + switch recommendation.

This is the workflow Tom asked for (2026-07-15):
  "using the benchmarks from all the free models we could give you the strongest
   free model available on that day... you'd know it and say 'this benchmark is
   better, let's try it' and then I'll switch."

What it does:
  1. Loads model_catalog.json (already patched daily with Artificial Analysis
     `aa_intelligence_index` by moa_benchmarks.py).
  2. Filters to FREE, general-purpose, usable text models (excludes
     coder-only, nvidia NIM cold-load, moderation/embedding roles).
  3. Ranks by real benchmark (aa_intelligence_index) falling back to heuristic
     `quality`. Excludes expiring-soon models (they'll vanish mid-task).
  4. Compares #1 against the CURRENT brain (read from config/brain_state.json).
  5. Returns a structured recommendation: keep | upgrade, with the delta and
     the exact switch command Tom would run.

It NEVER auto-switches Tom's live brain — it reports and waits for his "go".
The butler (atlas_butler) imports pick_brain() to choose its own ladder head.

USAGE:
  python3 brain_picker.py            # prints recommendation
  python3 brain_picker.py --json    # machine-readable
"""
import json, os, sys, datetime, argparse

MEMORY = "/home/tom/hermes-workspace/memory"
CATALOG = os.path.join(MEMORY, "model_catalog.json")
BRAIN_STATE = os.path.join(MEMORY, "brain_state.json")

# roles that are NOT general assistants — never pick as a brain/aggregator
BAD_ROLES = ["content-safety", "moderation", "safety", "embedding", "rerank", "classifier"]

def _nm(m):
    return (m["id"] + " " + (m.get("name") or "") + " " + " ".join(m.get("tags", []))).lower()

def is_general_brain(m):
    """A model usable as the main reasoning brain: general text, not coder-only,
    not a slow/cold NIM endpoint, not a safety/embedding role, and NOT a
    freellm meta-category (those are catalog placeholders like 'NVIDIA NIM'
    with no real callable endpoint)."""
    if not m.get("modalities", {}).get("text"):
        return False
    low = _nm(m)
    if any(b in low for b in BAD_ROLES):
        return False
    if "coder" in low or "code" in low or "codestral" in low or "deepcoder" in low:
        return False
    if m["home_provider"] == "nvidia":
        return False
    # freellm/* entries are aggregated provider labels, not callable chat models
    if m["home_provider"] == "freellm":
        return False
    return True

def score(m):
    """Benchmark score: real AA index if present, else heuristic quality."""
    return m.get("aa_intelligence_index") or m.get("quality", 0) or 0

def load_catalog():
    with open(CATALOG) as f:
        return json.load(f)["models"]

def get_current_brain():
    """Read the brain the system is currently pinned to."""
    if os.path.exists(BRAIN_STATE):
        try:
            return json.load(open(BRAIN_STATE)).get("current_brain")
        except Exception:
            pass
    # fallback: known default
    return "tencent/hy3:free"

def set_current_brain(model_id):
    state = {}
    if os.path.exists(BRAIN_STATE):
        try:
            state = json.load(open(BRAIN_STATE))
        except Exception:
            state = {}
    state["current_brain"] = model_id
    state["updated"] = datetime.date.today().isoformat()
    json.dump(state, open(BRAIN_STATE, "w"), indent=2)

def rank_free_brains(models):
    free = [m for m in models if m["tier"] == "free" and is_general_brain(m)]
    # exclude expiring-soon (they'll disappear mid-task)
    free = [m for m in free if not m.get("expiring_soon")]
    free.sort(key=lambda m: -score(m))
    return free

def pick_brain(models=None, current=None):
    """Return dict: {current, best, delta, verdict, switch_cmd, top5}."""
    if models is None:
        models = load_catalog()
    if current is None:
        current = get_current_brain()
    ranked = rank_free_brains(models)
    best = ranked[0] if ranked else None
    cur = next((m for m in models if m["id"] == current), None)
    cur_score = score(cur) if cur else 0
    best_score = score(best) if best else 0
    delta = round(best_score - cur_score, 1)
    if best and (cur is None or best["id"] != current) and delta >= 2.0:
        verdict = "UPGRADE"
    elif best and best["id"] == current:
        verdict = "KEEP (already best)"
    else:
        verdict = "KEEP (no meaningful gain)"
    switch_cmd = f'hermes config set model {best["id"]}' if best else "(no model)"
    return {
        "current": current,
        "current_score": cur_score,
        "best": best["id"] if best else None,
        "best_score": best_score,
        "best_provider": best["home_provider"] if best else None,
        "delta": delta,
        "verdict": verdict,
        "switch_cmd": switch_cmd,
        "top5": [
            {"id": m["id"], "score": score(m), "provider": m["home_provider"],
             "expiring": m.get("expiring_soon", False)}
            for m in ranked[:5]
        ],
    }

def report_text(rec):
    lines = []
    lines.append(f"# 🧠 Atlas Brain Picker — {datetime.date.today().isoformat()}")
    lines.append(f"Current brain: **{rec['current']}** (score {rec['current_score']})")
    lines.append(f"Best free brain today: **{rec['best']}** (score {rec['best_score']}) [{rec['best_provider']}]")
    lines.append(f"Delta: **{rec['delta']:+}**")
    lines.append(f"Verdict: **{rec['verdict']}**")
    if rec["verdict"].startswith("UPGRADE"):
        lines.append(f"\nRecommendation: try it. Switch command:\n`{rec['switch_cmd']}`")
        lines.append("I'll run it, test a live call, and report back. You approve the keep.")
    lines.append(f"\nTop 5 free brains by benchmark:")
    for i, t in enumerate(rec["top5"], 1):
        flag = " ⚠️expiring" if t["expiring"] else ""
        lines.append(f"  {i}. {t['id']} — {t['score']} [{t['provider']}]{flag}")
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    rec = pick_brain()
    if args.json:
        print(json.dumps(rec, indent=2))
    else:
        print(report_text(rec))

if __name__ == "__main__":
    main()
