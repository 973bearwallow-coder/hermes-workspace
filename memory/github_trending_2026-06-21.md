# GitHub Trending Report — 2026-06-21

## Top Repositories (Last 7 Days, by Stars)

| # | Repo | Stars | Language | Description |
|---|------|-------|----------|-------------|
| 1 | vercel/eve | 1,937 | TypeScript | Filesystem-first framework for durable AI agents |
| 2 | zhongerxin/cowart | 731 | JavaScript | (No description) |
| 3 | alchaincyf/loop-engineering-orange-book | 721 | — | Guide to loop engineering (橙皮书系列) |
| 4 | rebel0789/codexpro | 594 | JavaScript | ChatGPT Developer Mode as local coding agent via MCP |
| 5 | Forsy-AI/agent-apprenticeship | 566 | — | Ecosystem where AI agents learn from real-world work through iterative loops |
| 6 | Plaer1/junction | 516 | TypeScript | VS Code chat sidebar for local AI coding agents |
| 7 | ngrok/webernetes | 418 | TypeScript | Kubernetes in the browser |
| 8 | dongshuyan/compass-skills | 400 | Python | Personal alignment skills OS for AI agents (COMPASS) |
| 9 | boogu-project/Boogu-Image | 378 | Python | Apache-2.0 open-source image generation/editing model family |
| 10 | MstKail/polymarket-trading-bot-services-polyedge365 | 370 | — | Polymarket trading bot services |
| 11 | ReulgeApmpetty0O/Back-End-Developer-Interview-Questions | 355 | — | Backend interview questions |
| 12 | nnecrkvenuOX/formcms | 353 | C# | AI Agent headless CMS with ASP.NET Core + React |
| 13 | MstKail/wc2026-crypto-sportsbook | 329 | TypeScript | 2026 FIFA World Cup crypto sportsbook |
| 14 | aidenybai/cnfast | 304 | TypeScript | Fast drop-in replacement for `cn` (Tailwind class utility) |
| 15 | anthropics/launch-your-agent | 295 | HTML | Claude Code skill for building on Claude Managed Agents |

---

## Curated Picks for Tom

### 1. vercel/eve ⭐ 1,937 — TypeScript
**What:** Filesystem-first framework for durable AI agents. Agent capabilities (instructions, tools, skills, channels, schedules) live in conventional file locations — the filesystem IS the authoring interface.
**Why it matters:** Directly relevant to how Atlas/Hermes operates. The "filesystem as agent config" philosophy mirrors our own approach with skills, cron, and memory. Worth studying for ideas on structuring agent projects.
**Link:** https://github.com/vercel/eve

### 2. Forsy-AI/agent-apprenticeship ⭐ 566 — (no language)
**What:** An ecosystem where AI agents learn from real-world work through iterative workflow loops, reusable experience, and collective training signal exchange. Ships with 500+ seed tasks, 495 reusable agent lessons, 1000+ execution traces. Supports Codex, Cursor, Claude Code, OpenClaw, OpenCode, and Hermes Agent.
**Why it matters:** This is directly in our wheelhouse — agent self-improvement through experience loops. The explicit support for Hermes Agent and OpenClaw makes it immediately experimentable. The "apprentice/mentor" model for agent training signals is a fascinating approach to compounding agent capability.
**Link:** https://github.com/Forsy-AI/agent-apprenticeship

### 3. dongshuyan/compass-skills ⭐ 400 — Python
**What:** COMPASS — a personal alignment skills OS for AI agents. Ships four SKILL.md skills: task-clarifier, task-forest (DAG-based task memory), session-handoff-prompt, and user-profile-keeper. Installs via `npx skills add` for Claude Code and Codex.
**Why it matters:** This is essentially a skills ecosystem for coding agents — highly relevant to how we use skills in Hermes. The task-forest DAG concept and session-handoff-prompt are directly useful patterns. Could inspire better skill authoring or even be adapted for Hermes skills.
**Link:** https://github.com/dongshuyan/compass-skills

### 4. Plaer1/junction ⭐ 516 — TypeScript
**What:** VS Code chat sidebar that connects to 7 local AI coding agent backends: OpenClaw, Hermes, Souveraine, MiMoCode, Goose, OpenCode, and OpenHands. Features workspace context via drag-and-drop, model/reasoning picker, and auto-reconnection.
**Why it matters:** A unified multi-agent frontend that explicitly supports both OpenClaw and Hermes. Great reference for how to build a unified agent UI, and the multi-backend switching pattern is interesting for anyone running multiple agent runtimes.
**Link:** https://github.com/Plaer1/junction

### 5. rebel0789/codexpro ⭐ 594 — JavaScript
**What:** Turns ChatGPT Developer Mode into a local coding agent via MCP. Gives ChatGPT bounded tools for file reads, code search, exact edits, git inspection, and safe verification commands — all tunneled through ngrok/Cloudflare.
**Why it matters:** Clever use of MCP to bridge a cloud model to local repos. The architecture (MCP server ↔ ChatGPT Developer Mode) is a useful pattern to understand, even if we prefer fully local agents. Shows how far MCP has become the standard agent-tool bridge.
**Link:** https://github.com/rebel0789/codexpro

### 6. anthropics/launch-your-agent ⭐ 295 — HTML
**What:** Official Anthropic reference: a Claude Code skill that interviews you about what you want to build, scopes a v0, launches it as a Claude Managed Agent in your own account, grades it, iterates, and optionally schedules it.
**Why it matters:** This is Anthropic's playbook for going from idea → managed agent in production. The 4-phase flow (interview → launch → grade → iterate) is a solid methodology. Useful to understand the CMA primitives and how Anthropic thinks about agent deployment.
**Link:** https://github.com/anthropics/launch-your-agent

### 7. boogu-project/Boogu-Image ⭐ 378 — Python
**What:** Apache-2.0 open-source unified image generation and editing model family (Base, Turbo, Edit variants). Achieves near-closed-source performance with ~10x less training data. Includes inference code and checkpoints.
**Why it matters:** For the local model / self-hosting angle — this is a high-quality open image generation model that could run locally. The "order of magnitude less data" finding is interesting for efficient training. Relevant if Tom explores local image generation.
**Link:** https://github.com/boogu-project/Boogu-Image
