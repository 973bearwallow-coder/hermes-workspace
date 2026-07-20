# Lessons Learned — Corrections & Recurring Pitfalls
_Moved from MEMORY.md / USER.md during weekly consolidation (2026-07-19)._

## Verify before quoting (2026-07-18 correction)
- Tom corrected my recipe-vault count — I said 611, truth was ~217. He trusts his own estimates ('in the 300s') over stale skill notes.
- Lesson: VERIFY counts via terminal (find + grep) before quoting vault stats; skill docs drift.
- When I claimed a fact from memory/skill that was wrong, he called it out — always ground numeric claims in live tool output, not skill text.

## Memory buffer fix (2026-07-18)
- MEMORY.md hit 10k buffer limit; `memory` tool batch replace failed silently (format validation).
- Reliable fix: rewrite `/home/tom/.hermes/memories/MEMORY.md` directly via `write_file`, then confirm `memory` tool works at reduced %.
- Folded into `weekly-memory-consolidation` skill (buffer-full procedure + 10k limit).

## Honesty rule
- 'not done = don't show it.' Ground ensemble/benchmark numbers in REAL data, never guessed.
- Test MoA output BEFORE hand-writing. Test tools autonomously before Tom tries ('test away').
- When Tom finds a tool on YouTube, actually pull + install + test it.

## Diagnostic discipline
- Always diagnose WHY something failed, then determine the fix (real rule, not just patch-and-pray).
- Scrape GitHub before building. Brainstorm before executing. Prefers discussing HOW before building.

## Voice butler browser trap
- Firefox blocks getUserMedia on self-signed cert → butler buttons die. Use Chrome.
- Android background tabs hold mic 30-60s → blocks Telegram STT; mitigate with visibilitychange auto-release + manual Release Mic button.
