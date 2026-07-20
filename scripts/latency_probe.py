#!/usr/bin/env python3
"""
latency_probe.py — Measure real wall-clock latency for each usable MoA model.

Pings every free/cheap/premium model in the catalog with a tiny prompt, records
the time-to-first-token (or full completion for non-streaming), and writes the
result back into model_catalog.json as `latency_ms`.

This replaces the hardcoded ETA formula in moa_dashboard.py with MEASURED data.

Usage:
    python3 latency_probe.py            # probe all usable models (slow, ~1 call each)
    python3 latency_probe.py --quick    # only probe models used by free_mix for common tasks
    python3 latency_probe.py --id deepseek/deepseek-v4-flash   # probe one model

Note: respects rate limits loosely (small sleep between calls). Premium (openai-codex)
is probed but throttled via codex_usage_gate if present.
"""
import sys, os, json, time, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moa_providers as MP
import moa_router as MR

CATALOG = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "memory", "model_catalog.json")
CATALOG = os.path.abspath(CATALOG)

PING_PROMPT = "Reply with exactly: pong"
SYS = "You are a latency test. Reply with exactly one word: pong"

def probe_one(model_entry):
    mid = model_entry["id"]
    t0 = time.perf_counter()
    try:
        text, usage = MP.call_model(model_entry, PING_PROMPT, SYS, max_tokens=8, timeout=60)
        dt = (time.perf_counter() - t0) * 1000
        ok = bool(text and "pong" in text.lower())
        return int(dt), ok
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:80]}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="only probe free_mix models for chat/research/vision")
    ap.add_argument("--id", help="probe a single model id")
    ap.add_argument("--sleep", type=float, default=0.5, help="sleep between probes (s)")
    args = ap.parse_args()

    catalog = json.load(open(CATALOG))
    models = catalog["models"]

    if args.id:
        targets = [m for m in models if m["id"] == args.id]
    elif args.quick:
        # get the models the router would actually pick for common tasks
        seen = set()
        targets = []
        for task in ("chat", "research", "vision_doc", "coding"):
            refs, agg = MR.free_mix(models, task)
            for m in list(refs) + [agg]:
                if m["id"] not in seen and m.get("tier") in ("free", "cheap", "premium"):
                    seen.add(m["id"]); targets.append(m)
    else:
        targets = [m for m in models if m.get("tier") in ("free", "cheap", "premium")]

    print(f"Probing {len(targets)} models...")
    results = {}
    for m in targets:
        mid = m["id"]
        print(f"  {mid}...", end="", flush=True)
        ms, ok = probe_one(m)
        if ms is None:
            print(f" FAIL ({ok})")
            m["latency_ms"] = None
            m["latency_ok"] = False
            m["latency_err"] = ok
        else:
            print(f" {ms}ms {'OK' if ok else 'BAD-REPLY'}")
            m["latency_ms"] = ms
            m["latency_ok"] = ok
            m.pop("latency_err", None)
        results[mid] = ms
        time.sleep(args.sleep)

    # write back
    json.dump(catalog, open(CATALOG, "w"), indent=1)
    print(f"\nWrote latency_ms for {len(targets)} models to {CATALOG}")

    # summary table
    good = [(k, v) for k, v in results.items() if v]
    good.sort(key=lambda x: x[1])
    print("\n=== Fastest ===")
    for k, v in good[:8]:
        print(f"  {v:6d}ms  {k}")
    print("\n=== Slowest ===")
    for k, v in good[-5:]:
        print(f"  {v:6d}ms  {k}")

if __name__ == "__main__":
    main()
