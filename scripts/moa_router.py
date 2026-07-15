#!/usr/bin/env python3
"""
moa_router.py — Task -> Mixture-of-Agents selector + cost/benefit estimator
Part of Atlas MoA Router (2026-07-14).

USAGE
  python3 moa_router.py "look at this photo of my workshop and write a safety doc"
  python3 moa_router.py "build a flask app that scrapes reddit" --cost
  python3 moa_router.py "research the RTX 5090 vs 4090" --paid-ok

OUTPUT
  - Detected task type (vision_doc / coding / research / chat)
  - Recommended FREE/cheap MoA mixture (parallel reference models + aggregator)
  - If --paid-ok: a PAID-upgraded mix + ESTIMATED COST per task + tradeoff verdict
  - If --menu: prints both options and exits (caller asks user which to run)

COST MODEL (estimate only)
  OpenRouter pricing is USD PER TOKEN. We estimate from per-task token assumptions.
  Clearly labeled ESTIMATE. Real cost is measured by moa_exec.py at runtime.
"""
import json, os, sys, datetime, re

MEMORY = "/home/tom/hermes-workspace/memory"
CATALOG = os.path.join(MEMORY, "model_catalog.json")

TOKEN_ASSUMPTIONS = {
    "vision_doc": {"in_per_ref": 4000, "out_per_ref": 1500, "in_agg": 6000, "out_agg": 2000, "n_ref": 3},
    "coding":     {"in_per_ref": 3000, "out_per_ref": 1000, "in_agg": 4500, "out_agg": 1500, "n_ref": 3},
    "research":   {"in_per_ref": 6000, "out_per_ref": 2000, "in_agg": 9000, "out_agg": 2500, "n_ref": 4},
    "chat":       {"in_per_ref": 1000, "out_per_ref": 500,  "in_agg": 1500, "out_agg": 600,  "n_ref": 2},
}

# models that are NOT general assistants (classifiers/moderation/embeddings) — never use as ref or agg
BAD_ROLES = ["content-safety", "moderation", "safety", "embedding", "rerank", "classifier"]

# word-boundary keyword sets (avoid 'capital' matching 'api')
CODING_WORDS = [r"\bcode\b", r"\bapp\b", r"\bscript", r"\bbuild\b", r"\bscrape", r"\bflask\b", r"\bapi\b", r"\bfunction\b", r"\bdebug\b", r"\bgithub\b", r"\bprogram", r"\bsql\b"]
RESEARCH_WORDS = [r"\bresearch\b", r"\bcompare\b", r"\bvs\b", r"\bbenchmark\b", r"\binvestigate\b", r"\bwhat is\b", r"\bwhat are\b", r"\bwhy is\b", r"\bwhy are\b", r"\bexplain\b", r"\bhow does\b", r"\bhow do\b", r"\bcapital of\b", r"\bdifference\b", r"\bpros and cons\b"]

def load_catalog():
    with open(CATALOG) as f:
        return json.load(f)["models"]

def _nm(m):
    """Lowercased searchable name = id + name + tags (so name-based detection works)."""
    return (m["id"] + " " + (m.get("name") or "") + " " + " ".join(m.get("tags", []))).lower()

def is_usable(m):
    if m["home_provider"] == "local_ollama":
        return True
    low = _nm(m)
    return not any(b in low for b in BAD_ROLES)

def _is_coder(m):
    return "coder" in _nm(m) or "code" in _nm(m) or "codestral" in _nm(m) or "deepcoder" in _nm(m)

def _is_reason(m):
    return any(k in _nm(m) for k in ["reason", "thinking", "r1", "qwq", "nemotron", "hy3", "owl", "deepseek"])

def pick(models, predicate, limit=3, prefer_local=True, exclude_expiring=True):
    cands = [m for m in models if predicate(m) and is_usable(m)]
    if exclude_expiring:
        cands = [m for m in cands if not m.get("expiring_soon")]
    # LOCAL-FIRST: local ollama models rank above cloud, then by quality
    cands.sort(key=lambda m: (0 if (prefer_local and m["home_provider"] == "local_ollama") else 1, -m["quality"]))
    return cands[:limit]

def detect_task(text):
    t = text.lower()
    has_img = any(k in t for k in ["photo", "image", "picture", "screenshot", "look at", "workshop", "diagram", "see this"])
    if any(re.search(w, t) for w in CODING_WORDS):
        return "coding"
    if any(re.search(w, t) for w in RESEARCH_WORDS):
        return "research"
    if has_img:
        return "vision_doc"
    if any(k in t for k in ["doc", "write", "report", "summarize", "draft"]):
        # text-only doc work (no image keyword) -> research-style synthesis, not vision
        return "research"
    return "chat"
def free_mix(models, task):
    # aggregator = strong GENERAL text model (exclude coder-only, exclude expiring,
    # exclude nvidia NIM which cold-loads >90s and is unreliable as the SYNCHRONOUS
    # final step). Prefer openrouter/local (fast) then other clouds.
    def agg_pred(m):
        if m["tier"] != "free":
            return False
        if not m["modalities"]["text"]:
            return False
        if _is_coder(m):
            return False
        if m["home_provider"] == "nvidia":   # NIM cold-load too slow for aggregator
            return False
        if m["home_provider"] == "cloudflare":  # some need Workers Paid plan (403)
            return False
        # allow expiring openrouter free models as aggregator (we have runway; hy3 idx 41)
        if m.get("expiring_soon") and m["home_provider"] != "openrouter":
            return False
        return True
    def ref_pred(m):
        # references: free, usable, NOT nvidia NIM (cold-load >90s drags parallel run)
        if m["home_provider"] == "nvidia":
            return False
        return m["tier"] in ("free",) and is_usable(m)
    agg_rank = lambda m: (0 if m["home_provider"] == "openrouter" else 1 if m["home_provider"] != "local_ollama" else 2, -m["quality"])
    if task == "vision_doc":
        refs = pick(models, lambda m: ref_pred(m) and m["modalities"]["vision"], 3)
        if not refs:
            refs = pick(models, lambda m: "vision" in m["tags"] and m["home_provider"]=="local_ollama", 2)
        agg = sorted([m for m in models if agg_pred(m)], key=agg_rank)[0]
    elif task == "coding":
        refs = pick(models, lambda m: ref_pred(m) and (_is_coder(m) or _is_reason(m)), 3)
        agg = sorted([m for m in models if agg_pred(m)], key=agg_rank)[0]
    elif task == "research":
        refs = pick(models, lambda m: ref_pred(m) and (_is_reason(m) or "longctx" in m["tags"]), 4)
        agg = sorted([m for m in models if agg_pred(m)], key=agg_rank)[0]
    else:
        refs = pick(models, lambda m: ref_pred(m) and m["modalities"]["text"], 2)
        agg = sorted([m for m in models if agg_pred(m)], key=agg_rank)[0]
    return refs, agg

def paid_upgrade(models, task):
    """Swap aggregator to a cheap PAID model. Prefer deepseek-v4-pro (Tom's example)."""
    for wanted in ["deepseek/deepseek-v4-pro", "deepseek/deepseek-v4-flash"]:
        hit = [m for m in models if m["id"].lower() == wanted and m["tier"] == "cheap" and is_usable(m)]
        if hit:
            return hit[0]
    ds = pick(models, lambda m: m["tier"]=="cheap" and "deepseek" in m["id"].lower() and m["modalities"]["text"], 3, prefer_local=False)
    if ds:
        return ds[0]
    return pick(models, lambda m: m["tier"]=="cheap" and m["modalities"]["text"], 1, prefer_local=False)[0]

def premium_upgrade(models, task):
    """TOP rung: Claude / GPT (PAID, highest quality). Used only when user opts in."""
    for wanted in ["anthropic/claude-3-5-sonnet", "anthropic/claude-sonnet-4", "openai/gpt-4o", "openai/gpt-4.1"]:
        hit = [m for m in models if m["id"].lower() == wanted and is_usable(m)]
        if hit:
            return hit[0]
    cl = pick(models, lambda m: m["home_provider"]=="anthropic" and m["modalities"]["text"], 1, prefer_local=False)
    if cl: return cl[0]
    gpt = pick(models, lambda m: m["home_provider"]=="openai" and m["modalities"]["text"], 1, prefer_local=False)
    if gpt: return gpt[0]
    return None

def estimate_cost(mix_refs, agg, task):
    a = TOKEN_ASSUMPTIONS[task]
    total = 0.0
    lines = []
    for r in mix_refs:
        c = (a["in_per_ref"] * r["cost_in"]) + (a["out_per_ref"] * r["cost_out"])
        total += c
        lines.append(f"    ref {r['id']}: ${c:.6f}")
    ca = (a["in_agg"] * agg["cost_in"]) + (a["out_agg"] * agg["cost_out"])
    total += ca
    lines.append(f"    agg {agg['id']}: ${ca:.6f}")
    return total, lines

def menu(task_text, paid_ok=True):
    """Print both options (free + paid) as a choice card. Returns dict for caller."""
    models = load_catalog()
    task = detect_task(task_text)
    refs, agg = free_mix(models, task)
    free_cost, _ = estimate_cost(refs, agg, task)
    up = None
    print(f"Task type: {task.upper()}\n")
    print(f"OPTION A — ALL FREE (refs + aggregator, $0.00)")
    for r in refs:
        print(f"   ref: {r['id']}  q={r['quality']}")
    print(f"   agg: {agg['id']}  q={agg['quality']}")
    print(f"   est cost/task: ${free_cost:.6f}\n")
    if paid_ok:
        up = paid_upgrade(models, task)
        if up:
            pcost, _ = estimate_cost(refs, up, task)
            print(f"OPTION B — FREE refs + PAID aggregator ({up['id']}, q={up['quality']})")
            print(f"   est cost/task: ${pcost:.6f}  (≈ ${(pcost*1000):.2f}/1000 tasks)")
            print(f"   expected: higher factual accuracy / coherence vs free\n")
        else:
            print("OPTION B — no cheap paid model available; free only.\n")
    print("Pick A (free) or B (paid-agg)? Default A if no reply.")
    return {"task": task, "free_agg": agg["id"], "paid_agg": (up["id"] if paid_ok and up else None)}

def main():
    args = sys.argv[1:]
    text = " ".join(a for a in args if not a.startswith("--"))
    paid_ok = "--paid-ok" in args
    show_cost = "--cost" in args or paid_ok
    menu_mode = "--menu" in args
    models = load_catalog()
    task = detect_task(text)
    if menu_mode:
        menu(text, paid_ok)
        return
    refs, agg = free_mix(models, task)
    print(f"Task type: {task.upper()}")
    print(f"\nFREE/CHEAP Mixture (reference models run in parallel):")
    for r in refs:
        print(f"  • {r['id']}  [q={r['quality']} {','.join(r['tags'][:3])}]")
    print(f"  → Aggregator: {agg['id']}  [q={agg['quality']}]")
    if show_cost:
        cost, lines = estimate_cost(refs, agg, task)
        print(f"\nESTIMATED COST per task (FREE mix): ${cost:.6f}  (~$0)")
        if paid_ok:
            up = paid_upgrade(models, task)
            if up:
                pcost, plines = estimate_cost(refs, up, task)
                print(f"\nPAID-UPGRADE Mixture (aggregator -> {up['id']}):")
                for l in plines: print(l)
                print(f"  ESTIMATED COST per task (upgraded): ${pcost:.6f}")
                verdict = "WORTH IT" if pcost < 0.01 else "MARGINAL"
                print(f"\n  Tradeoff verdict: {verdict}. Upgrading aggregator to a cheap paid model")
                print(f"  typically lifts factual accuracy/coherence for <1 cent/task. Free mix may")
                print(f"  hallucinate more on complex tasks. Recommend: free for casual, paid-agg for")
                print(f"  client-facing / high-stakes docs.")
    exp = [r['id'] for r in refs+[agg] if r.get('expiring_soon')]
    if exp:
        print(f"\n  WARNING: Chosen mix contains EXPIRING models: {exp} — catalog will auto-swap.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: moa_router.py \"<task>\" [--cost] [--paid-ok] [--menu]")
        sys.exit(1)
    main()
