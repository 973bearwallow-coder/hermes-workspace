# GitHub Trending Report — 2026-07-01

Top 15 repos created in the last 7 days (by stars), filtered for AI agents, LLM tools, MCP, coding agents, local models, privacy/self-hosted, agent frameworks, dev tools.

---

## Top Picks for Tom

### 1. **deepseek-ai/DeepSpec** ⭐ 5,675 | Python
**What it does:** Full-stack codebase for training and evaluating speculative decoding algorithms (draft models for faster LLM inference). Includes data prep, draft model training (Eagle3, DFlask, EAGLE3), and evaluation against benchmarks (gsm8k, math500, aime25, humaneval, livecodebench, mt-bench, alpaca-hard-v2).
**Why it matters:** Directly relevant to optimizing local LLM inference on your RTX 3090. Speculative decoding is one of the highest-leverage speedups for local models. Includes released checkpoints for Qwen/Qwen3-4B/8B/14B draft models.
**Link:** https://github.com/deepseek-ai/DeepSpec

### 2. **TianhangZhuzth/Fundamental-Ava** ⭐ 677 | Python
**What it does:** Research framework for "digital human beings" — populations of autonomous agents each with their own memory, belief system, social model, and governance. Agents run in a shared simulation with epidemic/epistemic/procedural memory, belief-weighted decision making, and emergence detection (statistical change-point detection over population metrics).
**Why it matters:** Full agent-civilization framework with memory architecture (episodic/semantic/procedural separated), governance (laws proposed/voted/ratified by agents), and emergence detection. Useful reference architecture for multi-agent systems and agent memory design.
**Link:** https://github.com/TianhangZhuzth/Fundamental-Ava

### 3. **Kulaxyz/self-learning-skills** ⭐ 487 | Markdown/CLI
**What it does:** Meta-skill for AI coding agents (Claude Code, Cursor, Codex, any AGENTS.md reader) that recognizes when a session has discovered a reusable "golden path" (hard-won procedure, workaround, project fact) and persists it as a skill/rule that auto-loads next session. Works via `npx skills` CLI or manual copy into `.claude/skills/`, `.cursor/rules/`, or `AGENTS.md`.
**Why it matters:** Directly solves the "re-discovering the same workaround every session" problem for your agent workflows. Safety-first: no secrets, only captures *where* to find secrets (env var names, MCP tools). Promotion rule: only promotes to skill after 3 verified successes (passing test, clean exit, green build, reproduced repro).
**Link:** https://github.com/Kulaxyz/self-learning-skills

### 4. **lycorp-jp/sim-use** ⭐ 379 | Swift
**What it does:** Cross-platform CLI that gives AI agents "eyes and hands" on iOS Simulator and Android emulator/devices. Uses Apple Accessibility APIs + Android AccessibilityService to emit compact token-efficient UI outlines (`ui` command) and alias-cached taps (`tap @N`). Sub-300ms observe-act-verify loop per round trip. Single binary, no Node/npm.
**Why it matters:** Mobile computer-use for agents — the missing piece for on-device agent testing. Token-efficient UI representation (~16x smaller than raw JSON accessibility tree). Works with any LLM loop. Built for agent evaluation, not human testing.
**Link:** https://github.com/lycorp-jp/sim-use

### 5. **Jia-Ethan/codex-keysmith** ⭐ 369 | Python
**What it does:** Safe installer for Codex CLI instruction files (AGENTS.md / `.md` rules). Previews changes (`--dry-run`), backs up existing config.toml and same-name `.md` files before writing, rejects unsafe paths (absolute, `..`, empty, spaces). Not a Codex fork, not a binary patcher.
**Why it matters:** Streamlines managing instruction files across Codex/Claude Code/Cursor/Zed/Gemini CLI. If you maintain a library of prompts/rules for different projects, this gives a safe, auditable install flow with automatic backups.
**Link:** https://github.com/Jia-Ethan/codex-keysmith

### 6. **tdeverx/contained-app** ⭐ 442 | Swift
**What it does:** Native macOS app (SwiftUI, Sparkle updates) wrapping Apple's Container CLI — a Docker-alternative for Apple Silicon that runs Linux containers natively without a VM.
**Why it matters:** If you run local model stacks or dev containers on Mac, this gives a GUI for Apple's native container runtime (lighter than Docker Desktop, no VM overhead).
**Link:** https://github.com/tdeverx/contained-app

---

## Honorable Mentions (skipped: crypto/gaming/unrelated)

| Repo | Stars | Lang | Why skipped |
|------|-------|------|-------------|
| baairon/torlink | 2,020 | TypeScript | Torrent client |
| Krishnagangwal/CS-Fundamentals | 1,275 | — | Interview prep |
| yynxxxxx/Codex-5.5... | 944 | Python | Model repo, no clear description |
| winsznx/theeleven | 681 | TypeScript | Crypto/AI agents on Uniswap v4 |
| Pluviobyte/video-production-skills | 489 | Python | Video generation skills |
| CopilotKit/OpenTag | 478 | TypeScript | No description |
| cclank/lanshu-animated-architecture-diagram | 392 | Python | Diagram skill |
| diinki/linux-antiquity | 385 | QML | Linux theme |
| wlzh/dji-4g-vohive-mac | 380 | — | DJI hardware hack |

---

## Quick Takeaways

1. **Speculative decoding** (DeepSpec) is the highest-impact local LLM speedup right now — worth evaluating on your 3090.
2. **Agent memory/governance frameworks** (Fundamental-Ava) are maturing beyond toy demos; good reference for Charles/Hermes architecture.
3. **Skill persistence for coding agents** (self-learning-skills) solves a real pain point you've mentioned — re-learning workarounds.
4. **Mobile agent control** (sim-use) opens on-device agent eval; could pair with your screen-capture/OMI work.
5. **Instruction-file management** (codex-keysmith) is a small but sharp tool for agent config hygiene.

---
*Generated by GitHub Trending Monitor cron job. Search: `created:>2026-06-24 sort:stars-desc per_page=15` via authenticated `gh api`.*