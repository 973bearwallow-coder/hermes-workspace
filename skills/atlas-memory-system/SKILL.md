---
name: atlas-memory-system
description: How Atlas searches and organizes memory — vault files, session search, semantic index, and quick reference. Use this skill when you need to find past information or decide where to store new information.
---

# Atlas Memory System v2

## Architecture

Three layers:
1. **Injected memory** (MEMORY.md/USER.md) — 6K + 3K char limits. Only critical facts every session.
2. **Obsidian vault** (`~/hermes-workspace/memory/`) — Detailed notes in 9 folders. Searchable via hybrid semantic+keyword engine.
3. **Session transcripts** — Indexed into search DB (last 20 sessions, 390+ exchanges). Also searchable via FTS5.

## How to Find Something

### 🥇 Best: Hybrid Search (vault + sessions)
```bash
python3 ~/hermes-workspace/scripts/memory_search.py "query here"
```
- Searches vault files AND session transcripts simultaneously
- Combines semantic (conceptual) + keyword (exact match) scoring
- Recency-weighted: newer results rank higher
- Old daily noise automatically depriorized
- Modes: `--semantic` (conceptual only), `--keyword` (exact only)

### 🥈 Session Search (keyword, full transcripts)
Use the `session_search` tool:
- `session_search("keyword")` — discovery across all sessions
- `session_search(session_id="...", around_message_id=N)` — scroll within a session

### 🥉 Vault File Search
```bash
# Find files by name
search_files(pattern="keyword", target="files", path="~/hermes-workspace/memory/")

# Search inside files
search_files(pattern="keyword", path="~/hermes-workspace/memory/")

# Read specific file directly
cat ~/hermes-workspace/memory/Tools/kimi-webbridge-api.md
```

## Index Management

```bash
# Rebuild vault index (after adding new files)
python3 ~/hermes-workspace/scripts/memory_search.py --rebuild

# Re-index session transcripts (adds last 20 sessions)
python3 ~/hermes-workspace/scripts/index_sessions.py

# Rebuild everything + search
python3 ~/hermes-workspace/scripts/memory_search.py --rebuild "query"

# Check what's indexed
python3 ~/hermes-workspace/scripts/memory_search.py --stats
```

## How to Store Something

| Type of Info | Where |
|---|---|
| Needed every session | Injected memory (`memory` tool) |
| Details/context/history | Vault file |
| Tool API reference | `Tools/` in vault |
| Repeatable procedure | Skill (`skill_manage`) |
| Daily activity log | `Daily/YYYY-MM-DD.md` |

## Vault Folder Convention
- `Daily/` — YYYY-MM-DD.md logs (auto-depriorized after 7 days in search)
- `Projects/` — Active project notes
- `People/` — Contacts
- `Tools/` — API refs, configs
- `Business/AI-Boardroom/` — Julian's coaching, Skool
- `Business/Paw-Prints/` — Business strategy
- `Skills-Notes/` — Lessons learned
- `Meeting-Notes/` — Call summaries
- `GitHub-Watch/` — Trending repos

## Quick Reference
`cat ~/hermes-workspace/memory/QUICK_REFERENCE.md` — one-page map of everything.

## Current Stats (as of June 2 2026)
- 439 searchable chunks from 26 sources
- 7.7 MB search index
- Covers vault files + last 20 sessions
- Spans May 17 – June 2, 2026
