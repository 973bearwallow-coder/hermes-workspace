# MoA Model Stack & Routing — Detailed Notes
_Moved from MEMORY.md during weekly consolidation (2026-07-19). Supersedes Tools/model-stack-notes.md (June) for current state._

## Model Policy (as of 2026-07-19)
- PAID RELAXED since 2026-07-15 (OpenRouter funded, auto-refresh ON).
- Default Atlas brain: `tencent/hy3:free` (expires 2026-07-21).
- Daily driver (MoA): `deepseek/deepseek-v4-flash` (free, 1M ctx).
- `deepseek-v4-pro` = $0.000001/MTok, `deepseek-r1` = $0.000003/MTok (hard builds).
- AGNES RULE: bare slug `agnes-2.0-flash` home_provider='agnes'. NEVER `agnes/agnes-2.0-flash` (503). Diagnose slug/key BEFORE dropping a 503ing model. Added as multimodal fallback (256K ctx, vision=True), NOT default.

## MoA LADDER (Jul18)
DeepSeek V4 Flash = daily driver (free). `gpt-5.6-sol` (openai-codex OAuth, ChatGPT Plus) RESERVED for high-value via `should_escalate()`. Fallback: Gemini 2.5 Flash > qwen2:72b local > Groq llama-3.3-70b.
`codex_usage_gate.py` throttles on 429 + 30min cooldown. `moa_catalog.py` PRESERVES openai-codex entries on refresh (cron `a0bb763127fa` daily OpenRouter refresh).

## OPENAI CODEX OAUTH (Jul18)
- LIVE via `hermes auth add openai-codex --type oauth --no-browser` (device flow, `~/.hermes/auth.json` cred `openai-codex-oauth-1`).
- Codex route exposes ONLY `gpt-5.6-sol` (272K, streaming + store:false, endpoint `chatgpt.com/backend-api/codex/responses`).
- gpt-4o/o1/mini BLOCKED. Plus != API billing (sk-proj key insufficient_quota).

## ATLAS BRAIN (Jul18)
- default = `tencent/hy3:free` (expires 2026-07-21).
- Jul21 cron `eebf2f75fbb8` auto-switches to `deepseek-v4-flash` via `hermes config set`.
- `atlas_reason.py` escalates Atlas's own reasoning to `gpt-5.6-sol` when `should_escalate_brain()`=True; soft cap 15/day; fallback DeepSeek on 429.
- Daily 8PM status cron `9b9195006ae3` → Telegram.

## Rejected experiments (Jul18)
- NaraRouter (router.bynara.id): redundant — OpenRouter gives V4 Flash free + codex OAuth gives GPT 5.6 Sol free. User said 'don't bother'.
- Agent OS (Julian Golding, YouTube): prompt-pack to build Next.js dashboard, NOT pre-written software. ~80% redundant with our stack. User accepted: adapt parts / don't adopt as-is.
