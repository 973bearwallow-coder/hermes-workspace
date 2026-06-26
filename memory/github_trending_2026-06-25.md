# GitHub Trending Report — 2026-06-25

## Top Picks Relevant to Tom's Work

### 1. [Forsy-AI/agent-apprenticeship](https://github.com/Forsy-AI/agent-apprenticeship) ⭐ 924
AI agents learn from real-world work through iterative workflow loops, reusable experience, and collective training signal exchange. Includes 500+ seed tasks, 495 lessons, 1000+ execution traces. Works with Claude Code, Codex, OpenClaw, OpenCode, Hermes Agent.
**Why it matters:** Directly relevant to agent infrastructure — this is about agents learning from each other's work loops, a meta-agent pattern. Could inform how we structure agent memory/training for Hermes workflows.

### 2. [HKUDS/AgentSpace](https://github.com/HKUDS/AgentSpace) ⭐ 393
Human + Agents. One Team. One Workspace. An agent-native collaborative workspace where agents have defined roles, owners, permissions, and audit trails. Feishu-backed collaboration with role-based agent management.
**Why it matters:** Addresses multi-agent coordination and accountability at team/organization scale — useful context if we're thinking about multi-agent orchestration patterns.

### 3. [raiyanyahya/recall](https://github.com/raiyanyahya/recall) ⭐ 514
Fully-local project memory for Claude Code. Keeps a condensed session summary (context.md) across sessions using a local Python summarizer — no API calls, nothing leaves the machine. MIT licensed.
**Why it matters:** Solves the "cold session" problem for coding agents with a privacy-first approach. Relevant pattern for how we might handle persistent context across Hermes sessions without external APIs.

### 4. [Johell1NS/browser-search](https://github.com/Johell1NS/browser-search) ⭐ 165
Agent skill that orchestrates SearXNG (search) + Camofox (browse) + CloakBrowser (stealth) into a self-hosted, free, unlimited web research system for AI agents. Anti-hallucination by design.
**Why it matters:** We already have a browser-search skill, but this three-tool escalation pattern (search → browse → stealth browse) is a great reference for improving our own web-search capabilities.

### 5. [lightbearco/tupper](https://github.com/lightbearco/tupper) ⭐ 124
Open-source sandboxes for AI agents — runs untrusted, AI-generated code safely on your own machine. Apple Containers (macOS), Firecracker (Linux), E2B-style TypeScript SDK, with MCP server support and agent-framework integrations (Mastra, deepagents).
**Why it matters:** Self-hosted code execution sandbox for agents — directly relevant for safely running AI-generated code locally.

### 6. [QwenLM/Qwen-AgentWorld](https://github.com/QwenLM/Qwen-AgentWorld) ⭐ 407
A native "language world model" that simulates agentic environments (MCP, Search, Terminal, SWE, Android, Web, OS) through chain-of-thought reasoning. MoE model at 35B total/3B active, trained on 10M+ real interaction trajectories. Releases weights + evaluation benchmark.
**Why it matters:** This is agent simulation as a model capability — the agent environment is encoded directly into the model weights. Could be useful for understanding agent stateMachines or as a local evaluation approach.

### 7. [NotASithLord/peerd](https://github.com/NotASithLord/peerd) ⭐ 86
First AI agent harness native to the browser — a Chrome/Firefox extension that runs a full agent loop inside your existing browser. BYOK, no backend, no telemetry, WebRTC P2P for agent-to-agent comms.
**Why it matters:** Browser-as-agent-runtime is an interesting pattern. Good reference for how far browser-based agents can go without server infrastructure.

### 8. [Sachin7456/ollama-local-coding-agent](https://github.com/Sachin7456/ollama-local-coding-agent) ⭐ 12
Private, offline AI coding agent for local Qwen models via Ollama — zero dependencies, real tools, multi-agent. Code never leaves the machine.
**Why it matters:** Local-first multi-agent coding with Ollama. Good reference for how to build air-gapped agent workflows with Qwen on the 3090.

## Other Notable Mentions
- [benchflow-ai/awesome-evals](https://github.com/benchflow-ai/awesome-evals) ⭐ 232 — Curated resource list for building and evaluating AI agents (benchmarks, tools, papers)
- [Karovia/fullstack-ai-agent-roadmap](https://github.com/Karovia/fullstack-ai-agent-roadmap) ⭐ 191 — Chinese-language comprehensive AI agent learning roadmap (110 tutorials, 400+ projects)
- [joeseesun/qiaomu-llm-mcp](https://github.com/joeseesun/qiaomu-llm-mcp) ⭐ 44 — Local MCP gateway for multi-provider LLM routing
- [tsouth89/conduit](https://github.com/tsouth89/conduit) ⭐ 33 — Local MCP gateway that collapses servers to 3 meta-tools for ~90% token reduction
- [SlavaSexton/ComfyUI-Agent-Kit](https://github.com/SlavaSexton/ComfyUI-Agent-Kit) ⭐ 11 — ComfyUI skill for AI coding agents (Claude Code, Codex, etc.)

## Skipped (not relevant)
- Crypto/web3 proxy repos
- Gaming projects (Arma source code, badminton AI)
- PDF styling tools
- Investment tracking agents
