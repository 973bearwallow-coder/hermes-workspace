# Atlas Brain & Routing Project State
_Moved from MEMORY.md during weekly consolidation (2026-07-19)._

## Current state (2026-07-26)
- Atlas brain: `deepseek/deepseek-v4-flash` primary.
- Fallback: `tencent/hy3`.
- Stay off Gemini 2.5 Flash unless Tom explicitly overrides.
- Tom prefers conservative model adoption: validate with real use before promoting a new/expensive model.
- Daily 8PM status cron `9b9195006ae3` → Telegram.
- `atlas_reason.py` still escalates only when `should_escalate_brain()`=True; keep production changes evidence-based.

## Open items (carried from Jul18)
1. Resend 4 Italy al Dente cookbook photos → vault.
2. Clean stale recording crons + repoint `f7640f8d2c51` to `coaching_call_poll.py`.
3. Optional Lidl/GW/H Mart price comparison.
4. Patch `moa_providers.call_model` system-prompt bug (low pri).

## Hardware
- 2TB SSD arrives Thu 2026-07-23. Confirm use (storage/models/backup?) when it lands.

## Recipe vault (food-efficiency)
- 238 recipes as of 2026-07-19 (was 217 → 232 → 238; earlier '611' was stale skill text).
- Ingest: web-scrape free sources (author site/Food.com/tfrecipes) preferred over photo OCR.
- Cookbooks: Nick Stellino, Commander's Palace, D'Artagnan Glorious Game, ATK 2008, Biba Caggiano Italy al Dente (photo-demand only, borrow-only on Archive.org).
- Skills: food-efficiency-system, recipe-vault, recipe-fridge-raid, recipe-optimizer, recipe-web-ingest, atlas-voice-butler.
