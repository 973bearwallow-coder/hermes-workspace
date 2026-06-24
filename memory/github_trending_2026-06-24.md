# GitHub Trending Report — 2026-06-24

## Top Repos Relevant to Tom's Interests (AI Agents, LLM Tools, MCP, Coding Agents, Local Models, Privacy)

---

### 1. [Forsy-AI/agent-apprenticeship](https://github.com/Forsy-AI/agent-apprenticeship) ⭐ 887
**What:** A living ecosystem where AI agents learn from real-world work through iterative workflow loops, reusable experience, and collective training signal exchange.
**Why it matters:** This is directly relevant to our agent stack. It supports Hermes Agent, OpenClaw, Claude Code, Codex, and OpenCode out of the box. The idea: agents produce training signals from real tasks, and those signals improve future agent performance across the ecosystem. 500+ seed tasks, 495 reusable lessons, 1000+ execution traces — all open.
**Language:** TypeScript/JS (npm package) | **Topics:** ai-agents, hermes-agent, openclaw, claude-code, codex, opencode, reinforcement-learning

---

### 2. [raiyanyahya/recall](https://github.com/raiyanyahya/recall) ⭐ 440
**What:** Fully-local project memory for Claude Code — entirely offline, no API keys, no external model. Keeps a session log and condenses it into a resume-ready summary using classical Python summarization (zero LLM tokens).
**Why it matters:** Solves the "cold start" problem for coding agents. This is a privacy-first, local-first memory system that could be a great complement to Hermes — it works offline, costs nothing beyond Claude Code's own subscription, and never sends transcripts anywhere. MIT licensed.
**Language:** Python | **Topics:** claude-code-plugin, local-first, offline, privacy, memory, developer-tools

---

### 3. [lightbearco/tupper](https://github.com/lightbearco/tupper) ⭐ 121
**What:** Open-source sandboxes for AI agents — run untrusted, AI-generated code safely on your own machine. E2B-style SDK, self-hosted via Apple Containers (macOS) / Firecracker (Linux). Has an MCP server built in.
**Why it matters:** If we want agents to execute code safely on charles/vision without relying on hosted sandboxes (E2B, Modal), Tupper gives us that locally. Framework-ready for deepagents and Mastra, with a TypeScript SDK. MIT licensed.
**Language:** TypeScript | **Topics:** ai-agents, sandbox, mcp, e2b-alternative, containers, self-hosted

---

### 4. [Johell1NS/browser-search](https://github.com/Johell1NS/browser-search) ⭐ 153
**What:** A skill for AI agents that orchestrates SearXNG (metasearch), Camofox (browsing), and CloakBrowser (stealth) into one self-hosted, free, unlimited search+browse system. Anti-hallucination by design.
**Why it matters:** This is a drop-in skill for OpenClaw/Claude Code/Cursor that gives agents real web capability without API costs. Self-hosted, no rate limits, works with the tools we already care about. Great for our research and daily briefing workflows.
**Language:** JavaScript (skill/instructions) | **Topics:** ai-agent, searxng, camoufox, cloakbrowser, web-search, self-hosted

---

### 5. [tsouth89/conduit](https://github.com/tsouth89/conduit) ⭐ 24
**What:** A local MCP gateway that collapses all your MCP servers' tools from hundreds of definitions down to 3 meta-tools the agent searches on demand. Measured 97% less tool-definition overhead per request.
**Why it matters:** As we add more MCP servers to our stack, token overhead becomes a real problem. Conduit solves this elegantly — one gateway, lazy discovery, works with Claude Code, Cursor, Codex, etc. Keys in OS keychain, no cloud. Rust + Tauri UI.
**Language:** Rust | **Topics:** mcp, gateway, llm, developer-tools, rust, tauri

---

### 6. [jaredrhod/ai-memory-vault](https://github.com/jaredrhod/ai-memory-vault) ⭐ 31
**What:** Open-source system + templates that turn an Obsidian vault into an AI's working memory. No vector database, just markdown. MCP-compatible.
**Why it matters:** If we want our agents to have persistent, structured memory using Obsidian (which Tom already uses), this provides the templates and MCP integration to make that work. Local-first, privacy-preserving.
**Language:** Markdown/templates | **Topics:** agent-memory, obsidian, mcp, local-first, privacy, second-brain

---

### 7. [Sachin7456/ollama-local-coding-agent](https://github.com/Sachin7456/ollama-local-coding-agent) ⭐ 12
**What:** Private, offline AI coding agent for local Qwen models via Ollama — zero dependencies, real tools, multi-agent. Code never leaves your machine.
**Why it matters:** A proof-of-concept for fully-local coding agents using Ollama + Qwen. Relevant to our interest in local models and privacy. Could be a reference for building local agent workflows on the RTX 3090.
**Language:** TypeScript | **Topics:** ollama, local-llm, offline-ai, qwen, self-hosted-ai, coding-assistant

---

### 8. [smixs/iva](https://github.com/smixs/iva) ⭐ 18
**What:** Open-source personal AI agent with long-term memory. Best tools hand-picked and assembled — one command and it works. Supports Ollama, DeepSeek, Obsidian, Telegram, voice.
**Why it matters:** A privacy-focused, self-hosted personal agent that integrates many of the tools we care about (Ollama, DeepSeek, Obsidian, MCP). Good reference for what a full local-first agent stack looks like.
**Language:** Python | **Topics:** personal-ai, self-hosted, privacy, ollama, deepseek, mcp, obsidian, local-first

---

## Notable Mentions (less directly relevant but interesting)
- **cloudflare/security-audit-skill** (⭐ 581) — Coding-agent skill for multi-phase security audits with machine-readable findings. Could be useful for infrastructure work.
- **ObsidianOwl123/AgentLens** (⭐ 83) — Lightweight AI context compressor for LLM agents. Relevant to managing context windows.
- **Karovia/fullstack-ai-agent-roadmap** (⭐ 165) — 110-tutorial Chinese roadmap for AI agent development. Good reference material.

## Skipped (crypto/gaming/unrelated)
- baidu/Unlimited-OCR (OCR, not agent-related)
- zhongerxin/Cowart (no description, likely unrelated)
- sums001/Windows-Copilot-API (reverse engineering, legally gray)
- Valorant-AI/valorant-ai-aimbot-undetected (gaming cheat)
- eooce/transfer-api (API relay, unclear)
