
## MoA Trip-Up Test (2026-07-16, while Tom at gym)
- Empty desc -> "No task description" (graceful) ✅
- Gibberish "florp/bleep" -> silent nothing (should say "can't") ⚠️
- "asian chicken" fuzzy -> chinese/thai ✅
- "dessert steak" -> no conflict detection ⚠️ minor
- 15-ingredient query -> 100% match (permissive) ✅ no crash
- Recipe app edge cases (gibberish/nonsense) -> no crash ✅
- Contradictory "website no HTML" -> unclear (possible hang/refuse) ⚠️
- Huge 5k-char prompt -> ran (cost logged), output capture timing issue

VERDICT: MoA robust on runtime; needs (1) graceful refuse on nonsense,
(2) contradiction guard. Recipe app itself is solid.
