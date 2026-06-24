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
- Sub-agent reports back with: what it did, where the output is, any issues
- I verify the output (spot-check, don't trust blindly)
- Then deliver to Tom

## Active sub-agent budget
- Max 3 concurrent sub-agents
- Always verify external side-effects (file writes, API calls) before reporting success
