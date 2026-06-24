# GitHub Trending Report — 2026-06-23

## Top Repositories (Last 7 Days, by Stars)

| # | Repository | Stars | Language | Description |
|---|-----------|-------|----------|-------------|
| 1 | zhongerxin/Cowart | 2,283 | JavaScript | (No description) |
| 2 | baidu/Unlimited-OCR | 1,896 | Python | Unlimited OCR: One-shot long-horizon parsing |
| 3 | lyra81604/zhengxi-views | 841 | Python | Fund manager research agent skill (Chinese funds) |
| 4 | Forsy-AI/agent-apprenticeship | 791 | — | AI agent ecosystem for learning from real-world work |
| 5 | aidenybai/cnfast | 731 | TypeScript | Fast drop-in replacement for `cn` (Tailwind) |
| 6 | Plaer1/junction | 528 | TypeScript | VS Code chat sidebar for local AI coding agents |
| 7 | sums001/Windows-Copilot-API | 455 | Python | Reverse-engineered Windows Copilot → OpenAI-compatible API |
| 8 | cloudflare/security-audit-skill | 438 | JavaScript | Multi-phase security audit skill for coding agents |
| 9 | MstKail/polymarket-trading-bot* | 411 | — | Polymarket trading bots (skipped — crypto) |
| 10 | nnecrkvenuOX/formcms | 393 | C# | Open-source headless CMS with AI agent |
| 11 | yo-WASSUP/Good-Badminton | 389 | Python | AI Badminton Hawk-Eye System |
| 12 | raiyanyahya/recall | 367 | Python | Offline memory for Claude Code |
| 13 | overflowy/make-look-scanned | 364 | Go | Make PDFs look scanned (CLI/WASM) |

## Detailed Analysis — Most Relevant to Tom

### 1. Forsy-AI/agent-apprenticeship ⭐ 791
**What:** A living ecosystem where AI agents learn from real-world work through iterative workflow loops, reusable experience, and collective training signal exchange.
**Why it matters:** Directly relevant to Tom's agent work — mentions Hermes, OpenClaw, Claude Code, Codex, and OpenCode in its topics. The concept of "agent apprenticeship" (agents learning from traces of real work) is a hot research direction that could inform how Atlas/Charles improve over time.
**Language:** Multi-language (no primary) | [github.com/Forsy-AI/agent-apprenticeship](https://github.com/Forsy-AI/agent-apprenticeship)

### 2. raiyanyahya/recall ⭐ 367
**What:** Gives Claude Code durable memory — entirely offline. Stops wasting tokens re-explaining projects every session.
**Why it matters:** Solves a real pain point Tom likely experiences with agent sessions. Local-first, privacy-focused, uses TextRank for summarization. Actively developed (v0.3.5 just released with privacy policy, benchmarks, deterministic summaries).
**Language:** Python | [github.com/raiyanyahya/recall](https://github.com/raiyanyahya/recall)

### 3. Plaer1/junction ⭐ 528
**What:** VS Code chat sidebar for local AI coding agents with multi-bridge support (OpenCode, OpenHands, Hermes, Souveraine).
**Why it matters:** Directly supports Hermes as a bridge. Auto-detects Hermes config and port. This could be a great local UI for working with Atlas/Charles agents from VS Code.
**Language:** TypeScript | [github.com/Plaer1/junction](https://github.com/Plaer1/junction)

### 4. cloudflare/security-audit-skill ⭐ 438
**What:** A coding-agent skill for multi-phase security audits with independently verified, machine-readable findings.
**Why it matters:** From Cloudflare, so production-grade. The pattern of "security audit as an agent skill" is directly applicable to Tom's agent-skill architecture. Could be adapted for auditing Charles/OpenClaw configs.
**Language:** JavaScript | [github.com/cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill)

### 5. baidu/Unlimited-OCR ⭐ 1,896
**What:** "Unlimited OCR" — one-shot long-horizon parsing of documents. Baidu research project.
**Why it matters:** If Tom ever needs to process scanned documents, PDFs, or screenshots at scale, this is a powerful new tool. The "one-shot long-horizon" approach suggests it handles complex multi-page layouts better than traditional OCR.
**Language:** Python | [github.com/baidu/Unlimited-OCR](https://github.com/baidu/Unlimited-OCR)

### 6. sums001/Windows-Copilot-API ⭐ 455
**What:** Reverse-engineered Windows Copilot into an OpenAI-compatible REST API. Access GPT-4/GPT-5 without API keys.
**Why it matters:** Clever hack for getting free LLM access on Windows machines. Could be useful for any Windows boxes on Tom's LAN. Note: legally gray area.
**Language:** Python | [github.com/sums001/Windows-Copilot-API](https://github.com/sums001/Windows-Copilot-API)

## Skipped
- **polymarket-trading-bot** — pure crypto/trading
- **Cowart, birds.cafe** — no description, unclear purpose
- **Good-Badminton** — sports/vision, not relevant
- **Back-End-Developer-Interview-Questions** — fork of existing repo
- **formcms** — CMS, not AI/agent related
- **make-look-scanned** — niche utility
- **zhengxi-views** — Chinese fund investing agent, niche use case
- **cnfast** — Tailwind CSS utility, not AI-related
