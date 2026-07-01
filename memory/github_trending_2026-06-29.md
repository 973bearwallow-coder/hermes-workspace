# GitHub Trending Report — 2026-06-29

Generated from GitHub API search for repos created in the last 7 days, filtered for relevance to AI agents, LLM tools, MCP, coding agents, local models, privacy/self-hosted, and dev tools.

---

## Top Picks for Tom

### 1. deepseek-ai/DeepSpec ⭐ 2,880 | Python
**What:** Full-stack codebase for training and evaluating speculative decoding algorithms.
**Why it matters:** From DeepSeek — directly relevant to local LLM inference optimization. Speculative decoding is how you squeeze more tokens/sec out of your RTX 3090.
**Link:** https://github.com/deepseek-ai/DeepSpec

### 2. benchflow-ai/awesome-evals ⭐ 577
**What:** Curated, non-BS library of the best resources for building and evaluating AI agents — papers, blogs, tools, benchmarks.
**Why it matters:** High-quality evals are the bottleneck for agent reliability. This is a goldmine for anyone building production agent systems.
**Link:** https://github.com/benchflow-ai/awesome-evals

### 3. eli-labz/Godcoder ⭐ 249 | Rust
**What:** Local-first, open-source desktop coding agent. Bring your own LLM key; your code stays on your machine.
**Why it matters:** Privacy-focused coding agent built with Tauri + MCP. Local-first is the right model — Charles would approve.
**Link:** https://github.com/eli-labz/Godcoder

### 4. lightbearco/tupper ⭐ 138 | TypeScript
**What:** Open-source sandboxes for AI agents — run untrusted, AI-generated code safely on your own machine.
**Why it matters:** Self-hosted alternative to E2b. Uses Apple Container on macOS, Firecracker on Linux. Critical infra for safe agent execution.
**Link:** https://github.com/lightbearco/tupper

### 5. Ezeafk/awesome-agent-skills ⭐ 81
**What:** Curated reusable skills, workflows, and tool-backed capabilities for AI agents (Claude Code, Codex, Cursor).
**Why it matters:** Growing library of production skills. Good reference for what's emerging in the agent skills ecosystem — directly applicable to Hermes's own skill architecture.
**Link:** https://github.com/Ezeafk/awesome-agent-skills

### 6. Oxbshw/Agent-Span ⭐ 25 | Rust
**What:** Web Access Gateway for AI Agents — 52 channels, 92 MCP tools, 9 SDKs, self-healing backends, async Rust.
**Why it matters:** Self-hosted web scraping/API gateway purpose-built for agents. Could replace fragile custom scraping in agent pipelines.
**Link:** https://github.com/oxbshw/Agent-Span

### 7. lambda-alpha-labs/Graphenium ⭐ 13 | Rust
**What:** Trust-aware codebase memory for AI coding agents. Query repo structure, trace change impact, choose the right files before editing.
**Why it matters:** Code graph + blast radius analysis for agents. Solves the "agent edits the wrong file" problem with provenance tracking.
**Link:** https://github.com/lambda-alpha-labs/Graphenium

### 8. Menfre01/waveloom ⭐ 12 | Go
**What:** Terminal coding agent optimized for DeepSeek prefix caching — 95-99% cache hit, 1/50th the input cost.
**Why it matters:** If you're using DeepSeek APIs, this is a massive cost optimization. Pure Go TUI with Bubble Tea.
**Link:** https://github.com/Menfre01/waveloom

### 9. SparkyWen/qcue ⭐ 80 | Rust
**What:** Self-hosted "second brain" — knowledge management with LLM integration, offline-first, BYOK.
**Why it matters:** Privacy-focused personal knowledge base. Rust + Flutter + PostgreSQL. Good reference for self-hosted AI-augmented tools.
**Link:** https://github.com/SparkyWen/qcue

### 10. GraeLefix/GITVERSE ⭐ 131 | TypeScript
**What:** Reverse engineer any codebase into a build prompt — architecture breakdown, ASCII blueprint, AI-ready reconstruction prompt.
**Why it matters:** Feed it a repo, get back a structured prompt for reconstruction or documentation. Useful for codebase migration and onboarding agents.
**Link:** https://github.com/GraeLefix/GITVERSE

---

## Honorable Mentions
- **CopilotKit/OpenTag** (⭐ 360) — Open @agent mentions for Slack/GitHub, routes to Codex/Claude Code
- **Reyzowter/Hello-Agents** (⭐ 137) — Comprehensive AI agent tutorial from fundamentals to production
- **YurunChen/repo-docs-skills** (⭐ 235) — Living project docs for coding agents
- **pmady/gpu-mcp-server** (⭐ 9) — MCP server for NVIDIA GPU metrics (relevant for Charles monitoring)
- **lazhenyi/behest** (⭐ 10) — Rust-native building blocks for production AI agent runtimes

---

## Trends Observed
1. **Coding agents are exploding** — dozens of new local/self-hosted coding agent projects this week
2. **MCP everywhere** — nearly every agent tool now ships with MCP server support
3. **Privacy-first / local-first** is a major theme — Godcoder, tupper, qcue all emphasize data staying on your machine
4. **Agent skills/workflows** as a category is maturing — curated libraries emerging
5. **Rust for agent infra** — tupper, Agent-Span, Graphenium, behest all choose Rust for performance-critical agent infrastructure
