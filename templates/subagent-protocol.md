# Sub-Agent Dispatch Protocol

## When to spawn a sub-agent
- Task will take > 5 minutes (transcription, research, builds, scraping)
- Task is independent (doesn't need my conversation context)
- Task has a clear, verifiable output (file path, URL, data)

## When to do it myself
- Quick file creation, config changes, lookups (< 2 min)
- Tasks needing conversation context or user interaction
- Multi-step reasoning that benefits from the full conversation

## Dispatch pattern
```
delegate_task(
  goal="...",
  context="...",
  role="leaf",
  toolsets=["terminal", "file", "web"]
)
```

## Delivery
- Sub-agent reports back using `templates/handover-md-template.md`
- Validate a filled handover with `python3 scripts/validate_handover.py PATH`; do not accept unresolved placeholders or missing evidence sections
- Required evidence: completed work, current state, blockers, changed files, actual test results, exact next action, acceptance criteria, and rollback/checkpoint state
- I verify the artifact path and any external side effect by reading back the exact target; do not trust a self-reported success
- Check repository status before and after work so pre-existing dirty files are not claimed or overwritten
- Never repeat a completed side effect after context compaction or handoff
- Then deliver to Tom

## Active sub-agent budget
- Max 3 concurrent sub-agents
- Always verify external side-effects (file writes, API calls) before reporting success
