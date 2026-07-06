# Operational Learnings — 2026
_Consolidated from MEMORY.md during weekly memory consolidation, June 21 2026._

## Fathom Download
- `yt-dlp -f "bestaudio/best" --extract-audio --audio-format mp3` — without `-f` flag, gets full video (400MB+ instead of 50MB)

## Whisper
- `small` model for batch work (>30 min audio). `medium` is ~10x slower on CPU. Run 2 at a time.

## Skool SPA
- Kimi WebBridge clicks don't trigger route changes. User must navigate manually.
- Only reliable method: user copies Fathom share URL from video player.

## Coaching Call Workflow
- Recording cron removed. Post-call review cron (Tue/Fri 1pm) picks up tl;dv transcript → summarizes.
- Fathom + Whisper for archive.

## Sub-agents
- Don't use for CPU-bound batch work (Whisper). Use background processes in main session instead.

## Model
- Stay on openrouter/owl-alpha. Do NOT switch without asking Tom.

## GitHub API
- Always use `gh api` for GitHub calls on charles — never raw curl
- `gh` CLI authenticated as **973bearwallow-coder** (5,000/hour rate limit)

## Apify
- NOT used — zero dependency, $49/mo idle — cancel it

## Active Scraping Stack
- Crawlee, DuckDuckGo Lite, yt-dlp, web_search, CloakBrowser, Kimi WebBridge

## Email Organization — Debug Lessons
- `-w 200` (display width) ≠ `-s 500` (page size) — script only fetched 10 emails, sorted zero
- NoneType sender crash (JSON null values) — fixed
- Filter changed from 1-day → 12-hour
- When LLM cron reports counts, ALWAYS verify with filesystem

|## skill_manage write_file Blocked
|- 'email-organization' exists in both productivity/ and email/himalaya/references/
|- Use action='edit' with name='email-organization' instead
|
|## Voicebox Whisper STT Fix (2026-06-27)
|- Bug: WhisperForConditionalGeneration.from_pretrained() had weight-loading issue for output projection layer
|- Fix: Use whisper.load_model() instead, store as self._whisper_model (separate from self.model for TTS)
|- Verified: End-to-end TTS ✅ STT ✅ Health ✅
|- Always check `curl http://127.0.0.1:17493/health` if STT errors
|
|## Coaching Call Summarizer (2026-07-01 update)
|- 29 txt files >10KB in ~/Desktop/coaching_call/, 33 mp3 files
|- Key insight from June 4 call: Skills = Recipes (repeat), Workflows = Meal Plans (progression)
|- Claude.ai → Claude Code pipeline: roadmap in web → execute in terminal (mirrors Atlas/Charles split)
|
|## Model Notes (verified 2026-07-05)
|- Atlas primary: openrouter/owl-alpha (1M ctx). Do NOT switch without asking Tom.
|- Heavy reasoning: deepseek/deepseek-v4-pro. Backup: nemotron-3-nano (free)
|- Vision: Use local Ollama API directly (vision_analyze tool has 401 auth error)
|- Charles local: ollama qwen3:30b-a3b on RTX 3090
|- Always verify free model availability before recommending — OpenRouter free tier changes frequently
