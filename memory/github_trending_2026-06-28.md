# GitHub Trending Report — 2026-06-28

## AI Agents / LLM Tools / Dev Tools — Weekly Top Picks

### 1. [deepseek-ai/DeepSpec](https://github.com/deepseek-ai/DeepSpec) ⭐ 1,774
- **What**: Full-stack codebase for training and evaluating speculative decoding algorithms
- **Why it matters**: Speculative decoding is the key to fast local inference on your RTX 3090. DeepSeek open-training the full pipeline means the community can replicate 2-3× speedups without relying on proprietary stacks. Directly relevant to your local-model roadmap.
- **Language**: Python | Created: 2026-06-26

### 2. [QwenLM/Qwen-AgentWorld](https://github.com/QwenLM/Qwen-AgentWorld) ⭐ 608
- **What**: "Language World Models for General Agents" — a new paradigm for agent architectures
- **Why it matters**: Alibaba's Qwen team is pushing world models (not just LLMs) as the agent backbone. This could shape how the next generation of autonomous agents plans and reasons. Relevant if you're evaluating agent architectures for Charles.
- **Language**: Python | Created: 2026-06-22

### 3. [benchflow-ai/awesome-evals](https://github.com/benchflow-ai/awesome-evals) ⭐ 544
- **What**: Curated, non-BS library of resources for building and evaluating AI agents — papers, talks, tools, benchmarks, RL envs
- **Why it matters**: The definitive "what to read/watch/use" list for agent evals. Instead of Googling, start here. Useful for picking the right benchmarking approach for your own agents.
- **Topics**: agent-evaluation, ai-agents, benchmarks, llm-evaluation, rl-environments | Created: 2026-06-24

### 4. [HKUDS/AgentSpace](https://github.com/HKUDS/AgentSpace) ⭐ 494
- **What**: "Human + Agents. One Team. One Workspace." — a collaborative multi-agent workspace framework
- **Why it matters**: Focuses on human-in-the-loop multi-agent collaboration rather than fully autonomous swarms. Interesting pattern for how Tom and Atlas could orchestrate Charles and other agents more naturally.
- **Language**: TypeScript | Created: 2026-06-22

### 5. [Negai-98/AgentClaw](https://github.com/Negai-98/AgentClaw) ⭐ 34
- **What**: Harness-based declarative Agent framework — generate an agent from a single sentence, turn your builds into reusable "Claw" capabilities
- **Why it matters**: The "describe your agent in plain text, get a running agent" approach could simplify how you define new agent personalities for Hermes without deep coding. Low traction but conceptually aligned with Claw-based orchestration.
- **Language**: Python | Created: 2026-06-23

### 6. [rxdt/py_ralph_frame](https://github.com/rxdt/py_ralph_frame) ⭐ 5
- **What**: Lightweight spec-driven loop harness for Claude Code, Codex, and Gemini CLI — fresh-context runs, specs, commits, gates
- **Why it matters**: Solves the "agent context drift" problem by giving each run a fresh context window with explicit specs. Could wrap Codex/Claude Code sessions in your pipeline to keep them on-rails.
- **Topics**: agent-loop, agentic-ai, coding-agents, harness, claude-code, codex-cli | Created: 2026-06-23

### 7. [RedHillsMediaFL/caix](https://github.com/RedHillsMediaFL/caix) ⭐ 1 (fresh, just published 2026-06-27)
- **What**: Native Apple Core AI inference server for Apple silicon — OpenAI/Anthropic API compat, streaming chat, tools/skills/MCP, MTP speculative decoding
- **Why it matters**: If you ever move inference to a Mac Mini or want on-device AI with a familiar API, this is a native Swift/CoreML alternative to Ollama. Still brand new but technically ambitious.
- **Language**: Swift | Topics: local-llm, llm-inference, mcp, speculative-decoding | Created: 2026-06-27

### 8. [r5rana/agentware](https://github.com/r5rana/agentware) ⭐ 14
- **What**: Framework that makes your LLM self-aware, with loops for self-learning and persistent private memory
- **Why it matters**: The "persistent private memory" angle is interesting — agents that learn across sessions without cloud dependency. Worth watching if memory is a key concern.
- **Language**: Python | Created: 2026-06-23

---

## Notable Mentions (High Stars, Lower Relevance to Tom)
- **bozhouDev/codex-orange-book** (⭐2,246) — Comprehensive Codex usage guide in Chinese, good reference but derivative
- **krea-ai/krea-2** (⭐350) — Official inference code for Krea 2 generative model, media-focused
- **Pluviobyte/video-production-skills** (⭐354) — AI video production skills library, creative/media use case
- **NVIDIA-BioNeMo/bionemo-agent-toolkit** (⭐170) — BioNeMo agent skills, domain-specific

## Trend Observations
1. **Speculative decoding is going mainstream** — DeepSpec + multiple from-scratch inference engines dropped this week
2. **Agent evals are maturing** — awesome-evals at 544 stars in 4 days shows the community urgently needs this
3. **Multi-agent collaboration > pure autonomy** — AgentSpace and similar projects emphasize human+agent teams
4. **Streaming inference on consumer hardware** remains hot, with alternatives to Ollama emerging

---

*Generated: 2026-06-28T12:00:00Z via gh API authenticated search*
