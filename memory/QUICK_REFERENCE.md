# Atlas Quick Memory Reference

## Vault Structure
```
~/hermes-workspace/memory/
  YYYY-MM-DD.md  — Daily auto-captured notes (screen/OCR snapshots)
  github_trending_YYYY-MM-DD.md  — GitHub trending reports
  model_scout_YYYY-MM-DD.md  — Free model scouting reports
  MEMORY.md  — Compact injected-memory source of truth (target: <3K chars)
  QUICK_REFERENCE.md  — This file
  business/
    email-organization.md  — Email folder/retention rules
    paw-prints-brand-brain.md  — Full brand brain (16K, master ref)
    paw-prints-divi-checklist.md  — Divi website rebuild checklist
  Meeting-Notes/
    coaching-calls-2026.md  — AI Profit Boardroom call notes
  people/
    carson-status.md  — Carson's Hermes setup plan & status
  projects/
    standing-goals.md  — Active long-running objectives
    memory-system-upgrade-2026-06-02.md
    dukes-shot-clock.md  — Shot clock project notes
    recipe-vault-state-2026-06.md
  Skills-notes/
    operational-learnings-2026.md  — Lessons learned, pitfalls, patterns
  Tools/
    google-oauth-notes.md  — Google OAuth detailed notes
    hermes-desktop-launch.md  — Desktop app launch/troubleshooting
    hermes-desktop-vs-mission-control.md  — Comparison
    kimi-webbridge-api.md  — Kimi WebBridge API reference
    model-stack-notes.md  — Model stack & fallbacks
    voicebox-local-ai-voice.md  — Voicebox TTS/STT setup & fix
```

## Search Tools (ordered by preference)
1. `session_search(query="keyword")` — FTS5 across past conversations (always reach for this first)
2. `search_files(pattern="keyword", path="~/hermes-workspace/memory/")` — Grep vault files
3. `python3 ~/hermes-workspace/scripts/atlas_unified_search.py "query"` — Hybrid semantic + keyword + FTS5
4. Read specific vault file with `read_file`

## Rules
- Don't store credentials in memory files or vault
- Move detailed notes OUT of injected memory INTO vault
- Use `skill_manage` for repeatable procedures
- When stuck → switch to deepseek-v4-pro, solve it, switch back
- MEMORY.md target under 3,000 chars (currently 2,897 ✅)
