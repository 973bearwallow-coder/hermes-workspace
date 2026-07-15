# Phase 2 — Benchmark-Driven MoA + Coaching-Call Test (2026-07-14)

## What was built
`moa_benchmarks.py` — scrapes the Artificial Analysis LLM leaderboard (HTTP 200,
239 rows) and attaches REAL benchmark data to `model_catalog.json`:
- `aa_intelligence_index` (replaces heuristic `quality` where matched)
- `aa_blended_usd_1m`, `aa_median_tok_s`, `aa_latency`
- `quality_source`: "aa" (real) or "heuristic" (fallback)

239 AA rows scraped → 24 catalog entries matched initially, +`:free`-suffix variants
backfilled → hy3 (idx 41), deepseek-v4-pro (idx 44) now carry real AA indices.
Robust: if scrape yields 0 rows, keeps heuristic + logs warning (no crash).

## Router hardening done this session (bugs found by REAL execution)
1. **`detect_task` misclassified text-summary as vision_doc** — fixed: text-only
   doc work (summarize/report/write, no image keyword) → `research`, not vision_doc.
2. **Aggregator picked NVIDIA NIM (cold-load >90s, timed out 212s)** — fixed:
   `agg_pred` excludes `nvidia`; `agg_rank` prefers openrouter > other cloud > local.
3. **Aggregator picked Cloudflare model needing Workers Paid (HTTP 403)** — fixed:
   `agg_pred` excludes `cloudflare`.
4. **Aggregator picked local `qwen2:72b` (41GB > 38.9GB free RAM, HTTP 500)** — fixed:
   aggregator prefers openrouter cloud (always loads) over local for final synthesis.
5. **References included slow NVIDIA (dragged parallel run)** — fixed: `ref_pred`
   excludes `nvidia` from reference pool too.
6. **BROKEN_LOCAL exclusion was WRONG** — qwen3 models aren't broken, they're
   reasoning models (answer in `reasoning` field, `call_model` falls back correctly).
   Removed the exclusion; all 15 local models usable. Diagnosed, not guessed.
7. **`moa_exec` passed file PATH not CONTENT** — advisors couldn't read transcript.
   Fixed: `_load_transcript()` inlines transcript text into the prompt (truncated 24k).

## Coaching-call test — REAL execution
- Source: `/home/tom/meet-record/transcripts/coaching_call_20260709.txt` (66KB, clean).
  (20260710.txt is a bad Whisper run — do NOT use.)
- Task: "Extract 3 actionable determinations + summarize key topics" (research).
- Mix: refs = qwen2:72b + qwen3:30b-a3b + qwen3:4b + qwen3-64k (local, free);
  agg = tencent/hy3:free (openrouter, AA idx 41).
- **Result: ran successfully, $0.00, 123s.** Output: 3 real determinations
  (ionic balance / validator-not-bottleneck / AI session hygiene) + topic summary.
- Logged to `moa_cost_log.jsonl`.

## MoA vs Flagship comparison (benchmark ESTIMATE — no GPT/Claude keys to execute)
| Model | AA Idx | $/1M | tok/s |
|---|---|---|---|
| OUR Free MoA (hy3 agg) | 41 | $0.00 | — |
| OUR Cheap-Paid (deepseek-v4-pro) | ~44 | $0.18 | — |
| Claude Fable 5 | 60 | $7.70 | 60 |
| GPT-5.6 Sol (high) | 56 | $4.35 | 58 |
| GPT-5.6 Terra (max) | 55 | $2.17 | 141 |
| Claude Sonnet 5 (max) | 53 | $1.54 | 71 |

**Verdict:** Free MoA ≈ 68% of Claude Fable quality at $0 (vs $7.70/1M) → ~40x cost
advantage. Cheap-Paid ≈ 73% at $0.18/1M (~$6/1000 tasks). Quality gap real but cost
gap is 40-4000x. For coaching-call intel, free MoA is sufficient; cheap-paid reserved
for client-facing/high-stakes.

## Files changed
- NEW: `moa_benchmarks.py` (+ workspace copy)
- `moa_router.py`: detect_task fix, agg_pred/ref_pred/agg_rank, BROKEN_LOCAL removed (+ workspace)
- `moa_exec.py`: _load_transcript() inlines file content (+ workspace)
- `model_catalog.json`: 611 models, now with aa_* fields on matched entries
- `aa_scores.json`: 239 raw AA rows

## How to re-run
```
python3 moa_benchmarks.py              # refresh benchmarks
python3 moa_router.py "task" --cost --paid-ok   # show mix + cost
python3 moa_exec.py "task. Transcript: /path/to.txt" --max-tokens 1000   # RUN
```
Cron: free-model-scout Mon 9AM; moa_report daily 8AM (should call moa_benchmarks
inside refresh — TODO: wire moa_benchmarks into moa_report.py / moa_catalog.py).
