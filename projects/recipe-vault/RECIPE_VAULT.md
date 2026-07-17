# Recipe Vault — Single Source of Truth

**Root:** `~/hermes-workspace/projects/recipe-vault/`

## Structure (CANONICAL — do not re-discover)
| Path | What | Notes |
|---|---|---|
| `recipes/*.md` | 170 recipe files | REAL source. Each has `## Ingredients` (bullet or table). |
| `index.json` | Metadata for all 170 | `cuisines`, `types`, `methods`, `url`, `file`. Enriched 2026-07-16. |
| `ingredient-index.json` | ingredient → [recipe names] | 871 keys, rebuilt 2026-07-16 from `recipes/`. |
| `recipe_query.py` | **Atlas calls this** | Conversational query interface. See usage below. |
| `rebuild_ingredient_index.py` | Rebuilds the two JSONs | Run if recipes added/changed. |
| `recipe_dashboard_test.py` | MoA-generated Flask app | Test artifact ONLY. Not the production path. |
| `prices.csv` | Store prices (Phase 2) | Manual + scraped. Not yet created. |

## How Atlas queries (THE ONLY WAY)
```bash
# Fridge raid
python3 recipe_query.py "asian chicken broccoli dinner 3 people"
# Sale-driven plan
python3 recipe_query.py --sale pork --count 5
```
Output: JSON → Atlas reads, replies to Tom in natural language.

## Cuisine notes
- Vault has specific cuisines (chinese, thai, vietnamese, italian, mexican, etc.)
- NO "asian" / "european" tags — `recipe_query.py` maps these via REGION_MAP.
- `clean_cuisine()` strips `| type:` suffixes (e.g. "chinese | type: beef" → "chinese").

## Known data quirks
- `index.json` `file` paths use `recipes/` prefix (correct, files exist there).
- `by-type/` folder is a PARTIAL duplicate export — ignore it, use `recipes/`.
- 47 recipes still missing cuisines (content didn't contain keyword) — acceptable.

## Phase 2 (store prices) — pending
Stores: Aldi, Lidl, Great Wall, H Mart, Harris Teeter, Safeway, Giant, Grocery Outlet.
Scrapeable flyers: Aldi, Lidl, HT, Safeway, Giant. Manual: Great Wall, H Mart, Grocery Outlet.
Optimizer rule: least-stops, within ~10-15% of absolute lowest.
