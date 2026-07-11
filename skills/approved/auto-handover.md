SKILL: Auto-Handover on Context Limit

## Trigger
When context window reaches 70% capacity OR every 15-20 agent interactions.

## What to Do
1. Read `/home/tom/hermes-workspace/templates/handover-md-template.md`
2. Populate all sections from current session:
   - Context Summary: Summarize what was worked on
   - What Was Done: List completed items from todo list
   - What's Remaining: List pending items
   - Blockers/Issues: Any errors or blockers encountered
   - Next Steps: What the next agent/session should do first
   - Files Modified: List all files changed in this session
   - Key Decisions Made: Any strategic decisions
   - Notes for Next Agent: Context that would be lost

3. Save to `/home/tom/hermes-workspace/memory/handovers/YYYY-MM-DD_HHMM-session-handover.md`
4. If Kanban integration is set up, also create a ticket referencing this handover.

## Verification
- Handover file exists with all sections populated
- Next agent can start from "Next Steps" without re-reading full conversation

## Notes
- Run this BEFORE context window fills (at 70%, not 90%)
- If `/compact` is used, include the handover in the summary
- For delegation subagents, create handover when they complete (in their final summary)
