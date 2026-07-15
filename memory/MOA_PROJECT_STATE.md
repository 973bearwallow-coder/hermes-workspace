# Atlas MoA Router — Project State (DISASTER-RECOVERY SNAPSHOT)

**Last updated:** 2026-07-14 (Tuesday), session with Tom (Telegram).
**Purpose:** Single source of truth so a power outage / session loss cannot erase where we are, what we've built, and what we're shooting for. If you wake up blank, read this top-to-bottom.

---

## 🎯 WHAT WE'RE SHOOTING FOR (North Star)
A **fully data-driven, local-first Mixture-of-Agents (MoA) router** that:
1. Takes any task → analyzes required model strengths (vision/coding/research/chat).
2. Pulls **free + local** model options from a live GitHub-curated list (`free-model-scout` → `awesome-freellm-apis` / `cheahjs`).
3. Flags **caps** (rate limits, expirations) that would break the run.
4. Ranks candidates by **real third-party benchmarks** (Artificial Analysis Intelligence Index) — NOT just a heuristic.
5. If a paid model is genuinely better, estimates the **cheapest paid option + token cost** and presents it.
6. **Reports options to Tom** → Tom decides → only then does the MoA actually execute.
7. Long-term: package this so it benefits **us AND others** (reusable, shareable). Not scoped yet — north star only.

Tom's standing mandate: **stay free/cheap/local-first**; only go paid when clearly worth it (cheap-paid = deepseek-v4-pro / -flash). Human is the validator, not a bottleneck — but the *decision to run* stays with Tom.

---

## ✅ WHERE WE ARE (built & verified, 2026-07-14)

### Voice Butler (Atlas Voice Butler)
- Build A (desk GUI) + Build B (Android web client over Tailscale) done.
- Latency optimized; `atlas-butler.service` (user systemd) **active**, listening :8765.
- TTS = local Voicebox (chatterbox), STT = Parakeet-TDT CPU (zero VRAM).
- **Brain = local-first 6-tier fallback ladder** via `moa_providers.call_model()`:
  1. `tencent/hy3:free` (OpenRouter, primary persona) — **expires ~2026-07-21**
  2. `local_ollama/qwen2.5:7b` (local free)
  3. `groq/llama-3.3-70b-versatile`
  4. `cloudflare/@cf/meta/llama-3.3-70b-instruct-fp8-fast`
  5. `agnes/agnes-2.0-flash` (tool-calling + 256K ctx + vision) — **wired THIS session**
  6. `github/llama-3.3-70b-instruct`
- **hy3 expiry pre-wired**: `HY3_EXPIRY = 2026-07-21` + `_active_brain_ladder()` auto-drops hy3 after that date, promotes free tiers. No manual switch needed.

### MoA Router (the "agent brain selector")
- `moa_catalog.py` — pulls 611 models (OpenRouter keyless + local Ollama), tags tier/modalities/tags/rate_limit/expiration. Writes `model_catalog.json`.
- `moa_router.py` — `detect_task()` (vision_doc/coding/research/chat), `free_mix()`, `paid_upgrade()`, `estimate_cost()`. **Quality field is a HEURISTIC (1-10), not a benchmark** (the Phase-2 gap).
- `moa_exec.py` — runs a REAL mixture via OpenRouter API (parallel refs + 1 aggregator), logs real cost to `moa_cost_log.jsonl`. **Proven live**: $0.00 free / $0.000869 paid-agg.
- `moa_providers.py` — unified `call_model()` routing by `home_provider`. Keys via `get_provider_key.py` (never printed), secrets in `provider_keys.json` (chmod 600).
- `moa_report.py` — daily 8AM Telegram "model newspaper" (cron, no-agent mode).
- `free-model-scout` skill — `free_model_scout.sh` (cron Mon 9AM) scrapes GitHub free-LLM lists + OpenRouter live API.

### Live-certified providers (through `call_model()`)
local_ollama ✅ · openrouter ✅ · groq ✅ (browser UA) · cloudflare ✅ (acct_id in URL) · github ✅ (bare lowercase id) · **agnes ✅ (this session, tool-call tested)**.
NOT working: OpenAI (429), NVIDIA NIM (cold-load >90s), HF (DNS dead), Anthropic (401 — Tom skipped), Nous (DNS dead), Replicate (curated only).

---

## ✅ NIGHT SESSION (2026-07-14, pre-coffee-hour)
1. **Butler hermes_reply fix (ROOT CAUSE).** Local Qwen3 leaves `content` empty
   (answer only in `reasoning` field). `call_model` now passes `think:false` for
   local Ollama qwen3 → clean `content` ("2+2 equals 4."). Added `clean_reply()`
   in atlas_desk.py (no more first-line-of-thinking-trace garbage). qwen3:4b
   RE-ADDED to BRAIN_LADDER. Butler restarted, verified live.
2. **Cron benchmark refresh wired in.** `moa_report.py` now calls
   `moa_benchmarks.refresh()` at top of daily run (08:00 job `moa-daily-report`,
   delivers to Telegram). Cheap (~2s), robust (keeps prior aa_* on scrape fail).
   RECOMMENDATION WAS YES — done. No new cron needed.
3. **Dashboard built + LIVE.** `moa_dashboard.py` (Flask, :8770, Tailscale-only,
   Charles 100.115.214.128). Shows: live catalog stats, task planner (proposed
   advisers + WHY each + est time + est cost), MoA-vs-Claude/GPT comparison
   (AA benchmark estimate), past MoA tasks from moa_cost_log.jsonl. systemd
   `moa-dashboard.service` active. Verified HTTP 200, real router data rendered.

### How to view
- Local: http://127.0.0.1:8770  (Charles)
- Phone (Tailscale): http://100.115.214.128:8770
- Plan a task: http://100.115.214.128:8770/?task=research  (or ?task=coding)

### Files changed this session
- `atlas_butler/atlas_desk.py`: clean_reply() + qwen3 re-added to ladder
- `moa_providers.py`: think:false for local qwen3
- `moa_benchmarks.py`: refresh() wrapper
- `moa_report.py`: calls refresh() at top
- NEW `moa_dashboard.py` + `moa-dashboard.service`
- All synced to hermes-workspace/scripts/

### Resume after power loss
```
systemctl --user restart moa-dashboard.service   # dashboard
systemctl --user restart atlas-butler.service     # voice butler
python3 moa_benchmarks.py   # manual benchmark refresh
```
1. **Benchmark scraping built + verified.** `moa_benchmarks.py` scrapes Artificial
   Analysis leaderboard (239 rows, HTTP 200), attaches `aa_intelligence_index`,
   `aa_blended_usd_1m`, `aa_median_tok_s`, `aa_latency` to catalog. 24+ entries
   matched (hy3 idx 41, deepseek-v4-pro idx 44). Robust fallback to heuristic.
2. **Coaching-call test RAN FOR REAL.** Source: `coaching_call_20260709.txt` (clean;
   20260710.txt is a bad Whisper run, DO NOT USE). Mix: 4 local refs + hy3 aggregator.
   Result: 3 real determinations extracted, $0.00, 123s. Logged to moa_cost_log.jsonl.
3. **MoA vs Flagship comparison table produced** (benchmark ESTIMATE — no GPT/Claude
   keys): Free MoA ≈68% of Claude Fable quality at $0 (vs $7.70/1M) → ~40x cost edge.
   Full results: `hermes-workspace/memory/PHASE2_RESULTS.md`.

### Router bugs found + FIXED during real execution (this session)
- detect_task: text-summary misclassified as vision_doc → fixed to research.
- Aggregator picked NVIDIA NIM (212s timeout) → excluded nvidia from agg + refs.
- Aggregator picked Cloudflare paid-only model (HTTP 403) → excluded cloudflare.
- Aggregator picked local qwen2:72b (41GB > 38.9GB RAM, HTTP 500) → agg prefers
  openrouter cloud over local.
- BROKEN_LOCAL exclusion was WRONG — qwen3 models aren't broken, they're reasoning
  models (answer in `reasoning` field; call_model falls back correctly). Removed it;
  all 15 local models usable. Diagnosed, not guessed.
- moa_exec passed file PATH not CONTENT → advisors couldn't read transcript. Fixed
  with _load_transcript() inlining transcript text (truncated 24k).

### Files changed this session
- NEW `moa_benchmarks.py` (+ workspace copy)
- `moa_router.py`: detect_task fix, agg_pred/ref_pred/agg_rank, BROKEN_LOCAL removed
- `moa_exec.py`: _load_transcript() inlines file content
- `model_catalog.json`: aa_* fields on matched entries
- `aa_scores.json`: 239 raw AA rows
- Docs: `PHASE2_RESULTS.md`, this state file (MOA_PROJECT_STATE.md)

### To re-run after power loss
```
python3 moa_benchmarks.py
python3 moa_router.py "task" --cost --paid-ok
python3 moa_exec.py "task. Transcript: /path/to.txt" --max-tokens 1000
```

---

## 📁 FILE MAP (truth on disk)
- `/home/tom/atlas_butler/atlas_desk.py` — butler + BRAIN_LADDER + `_active_brain_ladder()`
- `/home/tom/.hermes/scripts/` AND `/home/tom/hermes-workspace/scripts/` — `moa_catalog.py`, `moa_router.py`, `moa_exec.py`, `moa_providers.py`, `moa_report.py`, `get_provider_key.py`, `free_model_scout.sh`
- `/home/tom/hermes-workspace/memory/model_catalog.json` — 611 models (authoritative)
- `/home/tom/hermes-workspace/memory/moa_cost_log.jsonl` — real cost accrual
- `/home/tom/.hermes/secrets/provider_keys.json` — chmod 600 (github, hf, nous, nvidia, replicate, openai, cloudflare+acct_id, **agnes**; anthropic skipped)
- `/home/tom/.hermes/skills/mlops/atlas-moa-router/SKILL.md` — router docs
- `/home/tom/.hermes/skills/free-model-scout/SKILL.md` — GitHub free-model notifier
- Coaching: `/home/tom/meet-record/transcripts/coaching_call_20260710.txt`, `/home/tom/hermes-workspace/memory/coaching-calls/coaching-call-intelligence.md`

---

## ⚠️ OPEN ITEMS (non-blocking)
- Phase 2 benchmark scraping (IN PROGRESS).
- Per-call latency/tier logging into daily report.
- NVIDIA NIM slow (cold-load) — leave out of ladder.
- Broken local `qwen3:4b`/`30b-a3b` (empty content) — excluded; use `qwen2.5:7b`.
- Agnes image/video free endpoints unwired (no need yet).
- Google token-refresh cron liveliness (Gmail read worked 2026-07-14).
- Long-term: package/sharable MoA (north star only).

---

## 🔌 HOW TO RESUME AFTER POWER LOSS
1. `systemctl --user status atlas-butler.service` — should be active. If dead: `systemctl --user restart atlas-butler.service`.
2. Read this file + `SKILL.md` (atlas-moa-router).
3. If Phase 2 was mid-build: check `moa_catalog.py` / `moa_benchmarks.py` for the AA scrape function; re-run `python3 moa_catalog.py --quiet` to confirm catalog still 611 + AA fields present.
4. If coaching test was mid-run: re-run `python3 moa_router.py "summarize coaching transcript, 3 determinations" --cost --paid-ok` then `moa_exec.py` once Tom approves.
5. Cron jobs: `hermes cron list` (moa daily report 08:00; free-model-scout Mon 09:00).

**Key facts that survive sessions:** Tom = Falls Church VA, co-owns Paw Prints w/ Jane. Voice app = Atlas (me), not a sub-bot. Free/local-first mandate. hy3 expires ~2026-07-21 (pre-wired). Agnes key in secrets (alias MUST be in get_provider_key.py or 401).
