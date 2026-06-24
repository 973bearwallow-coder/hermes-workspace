# Recipe Vault State — June 2026
_Consolidated from MEMORY.md during weekly memory consolidation, June 21 2026._

## Location
`~/hermes-workspace/projects/recipe-vault/`

## State (June 18 2026)
- **Total: ~125 recipes** (83 RTE + 47 Mel's + some Rasa Malaysia pending)
- **Index clean:** 0 missing, 0 orphaned after dedup cleanup
- **Cuisines:** 20+ distinct

## Key Rules
- No cookbook-exclusive recipes
- No exact duplicates
- Similar-named recipes with ingredient differences = DIFFERENT (keep both)
- Empty taxonomy = ask user, don't guess

## Import Workflow
`web_extract → recipe_data.json → import script → index update → dedup → taxonomy cleanup → verify`

## Sub-agent Rules
- Batch ≤10 recipes
- Check both `mels_` and `mels-kitchen-cafe_` naming for duplicates

## Verification
`len(md_files) == len(index['recipes'])`, 0 missing, 0 orphaned

## Rasa Malaysia
- 21 recipes scraped, need writing + taxonomy
- Filename: `rasa_*.md`
- Cuisines: mostly thai, some chinese/indian/greek/moroccan/french/asian
