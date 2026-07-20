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
        # ALLOW: free, cheap, AND premium (ChatGPT Plus OAuth — already paid, $0 marginal).
        # Premium (openai-codex/gpt-5.6-sol) is preferred when credits are available.
        if m["home_provider"] == "local_ollama":  # slow on this box (~20-50s) — never the sync aggregator
            return False
        if m["tier"] not in ("free", "cheap", "premium"):
            return False
        if not m["modalities"]["text"]:
            return False
        # openai-codex/gpt-5.6-sol is a GENERAL model (not code-only) despite "codex" in name
        if _is_coder(m) and m["home_provider"] != "openai-codex":
            return False
        if m["home_provider"] == "nvidia":   # NIM cold-load too slow for aggregator
            return False
        if m["home_provider"] == "cloudflare":  # some need Workers Paid plan (403)
            return False
        # hy3 promo expires ~2026-07-21; after that DeepSeek V4 Flash is the daily default.
        if m.get("expiring_soon") and m["home_provider"] != "openrouter":
            return False
        return True
    def ref_pred(m):
        # references: free, usable, NOT nvidia NIM (cold-load >90s drags parallel run),
        # NOT local_ollama (slow ~20-50s on this box — only useful as offline fallback)
        if m["home_provider"] in ("nvidia", "local_ollama"):
            return False
        return m["tier"] in ("free", "cheap") and is_usable(m)
    # Daily-driver: DeepSeek V4 Flash is the stable FREE default (fast, 1M ctx).
    # ChatGPT Plus OAuth (gpt-5.6-sol) is RESERVED for high-value / complex tasks
    # (client docs, hard builds, research synthesis) — invoked via premium_upgrade()
    # or auto-escalation, NOT as the default. This maximizes the $20/mo sub's value
    # without burning the codex credit limit on trivial chatter.
    DAILY_DRIVER = "deepseek/deepseek-v4-flash"
    FALLBACK_DRIVER = "gemini/gemini-2.5-flash"   # free, 1M ctx, different provider (redundancy)
    PRIVACY_DRIVER = "local_ollama/qwen2:72b"     # 100% local, free, private, no API cost
    SPEED_DRIVER = "groq/llama-3.3-70b-versatile" # free, very fast (0.1s), 128K ctx
    PREMIUM_DRIVER = "openai-codex/gpt-5.6-sol"  # ChatGPT Plus OAuth, $0 marginal, frontier quality
    def agg_rank(m):
        if m["id"] == DAILY_DRIVER:
            return (-1, 0)   # always top for regular chats
        if m["id"] == FALLBACK_DRIVER:
            return (0, 0)    # second choice
        if m["id"] == PRIVACY_DRIVER:
            return (1, 0)    # third choice (privacy/local)
        if m["id"] == SPEED_DRIVER:
            return (2, 0)    # fourth choice (fast free)
        if m["id"] == PREMIUM_DRIVER:
            return (3, 0)    # reserved — only used when explicitly escalated
        return (4 if m["home_provider"] == "openrouter" else 5 if m["home_provider"] != "local_ollama" else 2, -m["quality"])
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

# Keywords that signal a task deserves GPT "horsepower" (client-facing, complex,
# high-stakes). Regular chatter / casual Qs stay on free DeepSeek.
HORSEPOWER_KEYWORDS = [
    "client", "proposal", "contract", "report", "publish", "final", "important",
    "critical", "perfect", "best quality", "boardroom", "coaching call", "strategy",
    "analysis", "research", "build", "deploy", "architecture", "security doc",
    "paw prints", "business", "investment", "legal", "presentation", "email to",
    "send to", "hard", "complex", "reasoning", "synthesize", "comparison",
]

def should_escalate(task_text):
    """Return True if task warrants GPT-5.6-sol horsepower over free default."""
    t = task_text.lower()
    return any(k in t for k in HORSEPOWER_KEYWORDS)

def premium_upgrade(models, task):
    """TOP rung: highest-quality models. Used only when user opts in (--premium).

    Priority order:
      1. openai-codex/gpt-5.6-sol  — ChatGPT Plus OAuth (ALREADY PAID $20/mo, $0 marginal)
      2. openai/gpt-5.6-sol        — OpenRouter cheap (funded balance)
      3. anthropic/claude-*         — OpenRouter cheap
    The codex route is preferred because it costs nothing extra vs the Plus sub
    we already pay for. API key (openai/gpt-4o) is intentionally NOT used — the
    sk-proj key has insufficient_quota (no API billing).
    """
    # 1. ChatGPT Plus OAuth — zero marginal cost, top quality
    codex_hit = [m for m in models if m["id"].lower() == "openai-codex/gpt-5.6-sol" and is_usable(m)]
    if codex_hit:
        return codex_hit[0]
    # 2. OpenRouter gpt-5.6-sol (funded cheap tier)
    or_hit = [m for m in models if m["id"].lower() == "openai/gpt-5.6-sol" and is_usable(m)]
    if or_hit:
        return or_hit[0]
    # 3. Anthropic fallback
    cl = pick(models, lambda m: m["home_provider"]=="anthropic" and m["modalities"]["text"], 1, prefer_local=False)
    if cl: return cl[0]
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
