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

## skill_manage write_file Blocked
- 'email-organization' exists in both productivity/ and email/himalaya/references/
- Use action='edit' with name='email-organization' instead
