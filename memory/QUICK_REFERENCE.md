# Atlas Quick Memory Reference

## Vault Structure
```
~/hermes-workspace/memory/
  2026-06-07.md .. 2026-06-13.md  — Daily activity logs (last 7 days)
  github_trending_2026-06-12/13/14.md — GitHub trending (last 3 days)
  QUICK_REFERENCE.md  — This file
  STANDING_PROTOCOLS.md  — Operational protocols
  ai-profit-boardroom-scrape.md  — AI Profit Boardroom research
  auto-capture-system.md  — Auto-capture architecture
  boardroom-findings-june9.md  — Boardroom key findings
  github_audit_claude-hermes-mcp.md  — GitHub audit results
  business/
    email-organization.md  — Email folder/retention rules
    paw-prints-strategy.md  — Paw Prints biz strategy
  people/
    carson-hermes-setup-plan.md  — Carson setup plan
    carson-status.md  — Carson current status
  projects/
    standing-goals.md  — Standing goals
    memory-system-upgrade-2026-06-02.md
    tndc-invitation.md  — TNDC invitation project
  Tools/
    google-oauth-notes.md  — Google OAuth detailed notes
    hermes-desktop-launch.md  — Desktop app launch/troubleshooting
    hermes-desktop-vs-mission-control.md  — Comparison
    kimi-webbridge-api.md  — Kimi WebBridge API reference
    model-stack-notes.md  — Model stack & fallbacks
```

## Search Tools
1. `python3 ~/hermes-workspace/scripts/atlas_unified_search.py "query"` — Hybrid semantic + keyword + FTS5 (BEST)
2. `session_search(query="keyword")` — FTS5 across past conversations
3. `search_files(pattern="keyword", path="~/hermes-workspace/memory/")` — Grep vault files
4. `cat ~/hermes-workspace/memory/...` — Read specific file

## Rules
- Don't store credentials in memory files or vault
- Move detailed notes OUT of injected memory INTO vault
- Use `skill_manage` for repeatable procedures
- When stuck → switch to deepseek-v4-pro, solve it, switch back
