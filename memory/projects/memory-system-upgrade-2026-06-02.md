---
date: 2026-06-02
tags: [memory, system, upgrade, obsidian]
aliases: [Memory Upgrade, Obsidian Vault Setup]
---

# Memory System Upgrade (June 2 2026)

## What Changed

### Char Limits (config.yaml)
- `memory_char_limit`: 2,200 → **6,000**
- `user_char_limit`: 1,375 → **3,000**

### Obsidian Vault Structure
Created `~/hermes-workspace/memory/` as an Obsidian-compatible vault:
- **Daily/** — Daily notes (YYYY-MM-DD.md)
- **Projects/** — Active projects (standing goals, Paw Prints, etc.)
- **People/** — Contacts, community members
- **Tools/** — Tool configs, API notes, setup guides
- **Business/AI-Boardroom/** — Coaching call notes, community intel
- **Business/Paw-Prints/** — Business strategy, SEO, marketing
- **Skills-Notes/** — Lessons learned, pitfalls, patterns
- **Meeting-Notes/** — Summaries of important calls
- **GitHub-Watch/** — Interesting repos, trending projects

### Memory Organization Rules
- **Injected memory (MEMORY.md/USER.md)**: Only critical facts needed every single turn. Target: under 3,000 chars.
- **Vault files**: Everything else — details, context, history, tool APIs
- **session_search**: Use to recall past sessions and pull in context on demand
- **skill_manage**: Save reusable procedures as skills, not notes

### Cron Jobs Added
1. **Weekly model check** (Mon 9am): Scan OpenRouter for better free models
2. **Weekly memory prune** (Sun 8am): Consolidate memory, move stale entries to vault

## Guiding Principle
Julian's stack: OMI → Obsidian → Hermes. Our stack: xdotool/OCR → Obsidian vault → Hermes (with session_search). Same idea, Linux-native.

## Related
- [[standing-goals]]
- [[Tools/kimi-webbridge-api]]
