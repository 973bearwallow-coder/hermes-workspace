# Operational Learnings — 2026

## 2026-09-13 — Evidence retrieval evaluation
- Funes is a promising local-first Hermes history index, but its published benchmark is too small for adoption.
- Retrieval tests must include irrelevant queries and superseded facts, not just known-positive queries; measure false positives and obsolete-fact ranking as well as Hit@1.
- External binaries remain quarantined and sanitized before execution; optional publishing/synchronization stays disabled during local evaluation.

## 2026-09-20 — Voice bridge acceptance discipline
- Completion-first microphone rearm must wait for matching terminal completion, drained playback, and an echo-tail guard; Stop/New Question must invalidate pending rearm.
- Browser/unit acceptance is not physical acceptance. Keep production unchanged until the Samsung proves one audible answer per turn and automatic listening after playback.
- For the real-time bridge, prove gateway-to-outbound-media delivery with grounded, non-silent audio before asking for another phone/OpenRun test.
- Prefer one general memory-aware Atlas reasoning bridge with deterministic read-only tools over brittle domain-specific patches.
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

## Model routing
- Use GPT-6 Astra for consequential reasoning; use Sol, Terra, Luna, or local models for routine/high-volume work.
- Do not buy credits or use separately API-billed capacity without Tom's explicit approval.

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

## skill_manage write_file Blocked
- `email-organization` exists in both productivity/ and email/himalaya/references/.
- Use `action='edit'` with `name='email-organization'` instead.

## Voicebox Whisper STT Fix (2026-06-27)
- Bug: WhisperForConditionalGeneration.from_pretrained() had a weight-loading issue for the output projection layer.
- Fix: Use `whisper.load_model()` instead, stored as `self._whisper_model` (separate from `self.model` for TTS).
- Verified: end-to-end TTS, STT, and health passed.
- Check `curl http://127.0.0.1:17493/health` if STT errors recur.

## Coaching Call Summarizer (2026-07-01 update)
- 29 txt files >10KB in `~/Desktop/coaching_call/`, 33 mp3 files.
- Key insight from June 4 call: Skills = Recipes (repeat), Workflows = Meal Plans (progression).
- Claude.ai → Claude Code pipeline: roadmap in web → execute in terminal (mirrors Atlas/Charles split).

## Model Notes
- Current routing policy is recorded above; older fixed Owl/DeepSeek routing was retired.
- Vision uses the local Ollama API directly.
- Charles local model note: Ollama qwen3:30b-a3b on RTX 3090.
- Verify free-model availability before recommending; OpenRouter free tiers change frequently.
