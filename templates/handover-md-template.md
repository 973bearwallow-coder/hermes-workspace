# Autonomous Project Handover

**Date**: YYYY-MM-DD  
**Session ID**: SESSION_ID  
**Agent**: AGENT_NAME  
**Task**: TASK_DESCRIPTION  
**Status**: in_progress | blocked | ready_for_review | complete

> Write this before context compaction or agent transfer. Report observed state,
> not intent. A successful command is not proof of an external side effect.

## Objective and Acceptance Criteria
- Objective:
- [ ] Observable acceptance criterion 1
- [ ] Observable acceptance criterion 2

## Current State
- Last known-good behavior:
- Active process/job IDs (if any):
- External state read-back performed:

## Completed Work
- Item, with evidence or artifact path

## Remaining Work
- Item

## Blockers / Risks
- Blocker, consequence, and safest next attempt

## Changed Files
| Path | Purpose | Verified? |
|---|---|---|
| `/path/to/file` | What changed | test/read-back |

## Commands and Test Results
| Command/check | Actual result |
|---|---|
| `command` | exit code / pass count / relevant stderr |

## Git / Rollback Checkpoint
- Repository and branch:
- Pre-existing dirty files left untouched:
- Commit/tag/checkpoint (if one was intentionally created):
- Safe rollback instructions limited to this task's files:

## Decisions and Guardrails
- Decision and evidence:
- Explicitly rejected options and why:
- Secrets/access-bearing values: `[REDACTED]`

## Exact Next Action
1. One bounded command or edit the next agent should perform.

## Notes for Next Agent
- Context that would otherwise be lost
- Never repeat a completed side effect; verify current state first
