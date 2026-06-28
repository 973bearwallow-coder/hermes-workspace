# GitHub Trending Report — 2026-06-27

## Top Repos Relevant to Tom's Work (AI Agents, LLMs, MCP, Dev Tools)

### 1. deepseek-ai/DeepSpec ⭐ 589
- **What:** Full-stack codebase for training and evaluating speculative decoding algorithms
- **Language:** Python
- **Why it matters:** Speculative decoding is key to faster local inference — directly relevant to Charles/RTX 3090 setup. DeepSeek continues shipping high-quality inference infra.
- **Link:** https://github.com/deepseek-ai/DeepSpec

### 2. QwenLM/Qwen-AgentWorld ⭐ 582
- **What:** Language World Models for General Agents — Qwen's agent environment/research framework
- **Language:** Python
- **Why it matters:** Alibaba's Qwen team releasing agent infrastructure signals the agent race is heating up. Could provide useful patterns for Atlas/Hermes agent workflows.
- **Link:** https://github.com/QwenLM/Qwen-AgentWorld

### 3. HKUDS/AgentSpace ⭐ 461
- **What:** "Human + Agents. One Team. One Workspace" — collaborative multi-agent workspace
- **Language:** TypeScript
- **Why it matters:** Research-focused multi-agent coordination from HKU's data science lab. Concepts applicable to orchestrating multiple Atlas/OpenClaw workers.
- **Link:** https://github.com/HKUDS/AgentSpace

### 4. lightbearco/tupper ⭐ 125
- **What:** Open-source sandboxes for AI agents — run untrusted AI-generated code safely on your own machine
- **Language:** TypeScript (Bun)
- **Why it matters:** Self-hosted sandbox for agent code execution. MCP-compatible. Direct alternative to e2b but fully local — pairs well with Charles.
- **Link:** https://github.com/lightbearco/tupper

### 5. nikhilkagita04/continuum ⭐ 21
- **What:** Your whole desktop context as a single MCP — local-first, on-device, privacy-preserving agent memory
- **Language:** JavaScript
- **Why it matters:** Captures screen, reading, typing history into a structured memory layer for agents. The "dreaming" consolidation pass is novel. Directly relevant to Atlas's long-term memory work.
- **Link:** https://github.com/nikhilkagita04/continuum

### 6. benchflow-ai/awesome-evals ⭐ 513
- **What:** Curated library of the best resources for building and evaluating AI agents — papers, tools, benchmarks
- **Language:** (curated list)
- **Why it matters:** High-quality, actively-maintained eval resource. Useful for benchmarking local models on Charles and understanding agent quality metrics.
- **Link:** https://github.com/benchflow-ai/awesome-evals

### 7. neuronaline/ai-memory-context-management ⭐ 7
- **What:** Cache-optimized architecture and Shadow VFS framework for token-efficient LLM agents
- **Language:** (framework)
- **Why it matters:** Solves context window bloat in long-running agents with tiered memory + VFS. Directly applicable to keeping Atlas/Hermes sessions efficient.
- **Link:** https://github.com/neuronaline/ai-memory-context-management

### 8. pexni/smails ⭐ 28
- **What:** Agent-native disposable email — Cloudflare Workers + Durable Objects, with CLI & MCP
- **Language:** TypeScript
- **Why it matters:** MCP-native disposable email for agents. Useful pattern for agent-to-outside-world communication without polluting real inboxes.
- **Link:** https://github.com/pexni/smails

---

## Notable Mentions (less directly relevant but interesting)
- **m1ckc3s/claude-status-bar** ⭐ 365 — macOS menu bar indicator for Claude Code (Swift)
- **HiyuCat/deepseek-v4-pro-flash-desktop-app** ⭐ 41 — Desktop app for DeepSeek V4 Flash (TypeScript)
- **Kaos599/Deep-Ass-Research** ⭐ 2 — IDE-agnostic deep research framework outputting to Obsidian vaults

## Skipped (crypto/web3/gaming/unrelated)
- winsznx/theeleven (web3/football betting)
- kanavtwtgg/birds.cafe (no description)
- BohemiaInteractive/CWR (game source code)
- Yu9191/wloc (location spoofing)
- bikini/exploitarium (security exploits)
