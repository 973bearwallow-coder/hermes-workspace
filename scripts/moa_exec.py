#!/usr/bin/env python3
"""
moa_exec.py — Actually RUN a Mixture-of-Agents task via OpenRouter
Part of Atlas MoA Router (2026-07-14). Phase 3 (execution, not just recommendation).

WHY NOT hermes config set moa.presets?
  Proven: `hermes config set` does NOT write real YAML lists for MoA arrays
  (Hermes's own normalize_moa_config fell back to defaults). And per-turn preset
  swaps break the sacred prompt cache. So we execute the mixture DIRECTLY via the
  OpenRouter chat API: parallel reference calls (advisors) + 1 aggregator call.
  This (a) actually works, (b) measures REAL token cost, (c) costs $0 config risk.

USAGE
  python3 moa_exec.py "task description" [--paid-ok] [--max-tokens 1200]
  Reads model_catalog.json to pick the mix (same logic as moa_router.py).

OUTPUT
  - prints the chosen mix + estimated cost
  - runs references in parallel, feeds their outputs to the aggregator
  - prints FINAL answer + REAL cost (prompt/completion tokens used)
  - records actual cost to moa_cost_log.jsonl for the feedback/ROI loop

COST: real tokens billed by OpenRouter; free models = $0; cheap-paid aggregator = cents.
"""
import json, os, sys, time, concurrent.futures, urllib.request, urllib.error, re
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, "/home/tom/hermes-workspace/memory")
from moa_router import load_catalog, detect_task, free_mix, paid_upgrade, premium_upgrade, estimate_cost
from moa_providers import call_model
from get_openrouter_key import get_key

OR_URL = "https://openrouter.ai/api/v1/chat/completions"
MEMORY = "/home/tom/hermes-workspace/memory"
COST_LOG = os.path.join(MEMORY, "moa_cost_log.jsonl")

def _load_transcript(task_text, max_chars=24000):
    """If task_text references a local .txt/.md/.json file path, read + truncate it
    and return (file_text, used_path). Advisors can't access the filesystem, so we
    must inline the content. Returns ('', None) if no readable path found."""
    paths = re.findall(r"(/\S+\.(?:txt|md|json|srt|vtt|tsv))", task_text)
    for p in paths:
        if os.path.isfile(p):
            try:
                txt = open(p, encoding="utf-8", errors="ignore").read()
                if len(txt) > max_chars:
                    txt = txt[:max_chars] + f"\n...[truncated {len(txt)-max_chars} chars]"
                return txt, p
            except Exception:
                continue
    return "", None

def call_or(model_entry, prompt, sys_prompt="You are a specialist advisor. Give a concise, expert take.", max_tokens=500):
    """One model call via provider router. Returns (text, usage_dict)."""
    text, usage = call_model(model_entry, prompt, sys_prompt, max_tokens)
    return text, usage

def run(task_text, paid_ok=False, premium=False, max_tokens=1200):
    models = load_catalog()
    task = detect_task(task_text)
    refs, agg = free_mix(models, task)
    # inline any referenced transcript file so advisors can actually see it
    transcript, tpath = _load_transcript(task_text)
    if transcript:
        task_text = f"{task_text}\n\n--- TRANSCRIPT CONTENT (from {tpath}) ---\n{transcript}"
    print(f"Task: {task.upper()}")
    print(f"References (parallel):")
    for r in refs:
        print(f"  • {r['id']}  [{','.join(r['tags'][:3])}]")
    print(f"Aggregator: {agg['id']}")
    est, est_lines = estimate_cost(refs, agg, task)
    print(f"Est cost: ${est:.6f}")

    # Run references in parallel (each may hit a DIFFERENT provider — local-first)
    t0 = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(refs)) as ex:
        futs = {ex.submit(call_or, r, task_text, max_tokens=500): r for r in refs}
        ref_outputs = {}
        for f in concurrent.futures.as_completed(futs):
            r = futs[f]
            txt, _ = f.result()
            ref_outputs[r["id"]] = txt
    ref_block = "\n\n".join(f"[ADVISOR {mid}]\n{out}" for mid, out in ref_outputs.items())

    # Aggregator synthesizes
    agg_prompt = f"TASK: {task_text}\n\nADVISOR OUTPUTS:\n{ref_block}\n\nSynthesize the best final answer from the advisors above."
    final, usage = call_or(agg, agg_prompt,
                           sys_prompt="You are the lead synthesizer. Combine advisor inputs into one clear, correct final answer.",
                           max_tokens=max_tokens)
    dt = time.time() - t0

    # cost accounting (refs may be local $0; aggregator cost from its pricing)
    real_cost = (usage.get("prompt_tokens", 0) * agg["cost_in"]) + (usage.get("completion_tokens", 0) * agg["cost_out"])
    print(f"\n=== FINAL ANSWER (agg {agg['id']}) ===\n{final}")
    print(f"\nTime: {dt:.1f}s | Aggregator real cost: ${real_cost:.6f} | usage={usage}")

    # Cheap-paid upgrade comparison (optional)
    if paid_ok:
        up = paid_upgrade(models, task)
        if up:
            print(f"\n--- CHEAP-PAID UPGRADE: aggregator -> {up['id']} (refs stay free) ---")
            final_p, usage_p = call_or(up, agg_prompt,
                                      sys_prompt="You are the lead synthesizer.", max_tokens=max_tokens)
            pcost = (usage_p.get("prompt_tokens",0)*up["cost_in"]) + (usage_p.get("completion_tokens",0)*up["cost_out"])
            print(f"Paid final (first 400c): {final_p[:400]}...")
            print(f"Cheap-paid real cost: ${pcost:.6f} vs free agg ${real_cost:.6f}")

    # Premium rung (Claude/GPT) — only if --premium passed
    if premium:
        prem = premium_upgrade(models, task)
        if prem:
            print(f"\n--- PREMIUM UPGRADE: aggregator -> {prem['id']} ---")
            final_pr, usage_pr = call_or(prem, agg_prompt,
                                        sys_prompt="You are the lead synthesizer.", max_tokens=max_tokens)
            prcost = (usage_pr.get("prompt_tokens",0)*prem["cost_in"]) + (usage_pr.get("completion_tokens",0)*prem["cost_out"])
            print(f"Premium final (first 400c): {final_pr[:400]}...")
            print(f"Premium real cost: ${prcost:.6f}")

    # log actual cost for ROI feedback loop
    with open(COST_LOG, "a") as f:
        f.write(json.dumps({
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "task": task, "agg": agg["id"], "refs": [r["id"] for r in refs],
            "real_cost_agg": real_cost, "paid_ok": paid_ok, "premium": premium,
            "usage": usage,
        }) + "\n")
    print(f"\n[logged to {COST_LOG}]")
    return final

if __name__ == "__main__":
    args = sys.argv[1:]
    text = " ".join(a for a in args if not a.startswith("--"))
    paid = "--paid-ok" in args
    premium = "--premium" in args
    if len(args) < 1 or not text:
        print('usage: moa_exec.py "task" [--paid-ok] [--premium]')
        sys.exit(1)
    run(text, paid_ok=paid, premium=premium)
