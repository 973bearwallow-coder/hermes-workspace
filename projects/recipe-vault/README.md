# 🍳 Recipe Vault

**Location:** `~/hermes-workspace/projects/recipe-vault/`
**Search script:** `~/hermes-workspace/scripts/search_recipes.py`

## Search Commands

```bash
# By ingredients
python3 scripts/search_recipes.py -i chicken thai
python3 scripts/search_recipes.py -i lemon chicken

# By cuisine
python3 scripts/search_recipes.py -c italian
python3 scripts/search_recipes.py -c mexican

# By type
python3 scripts/search_recipes.py -t dessert
python3 scripts/search_recipes.py -t salad

# By method
python3 scripts/search_recipes.py -m grilled
python3 scripts/search_recipes.py -m one-pot

# Combined
python3 scripts/search_recipes.py -i chicken -c thai
python3 scripts/search_recipes.py -i chicken -m one-pot
python3 scripts/search_recipes.py -c italian -t main
```

## Vault Structure

```
recipe-vault/
├── recipes/          ← All recipes as individual markdown files
├── by-cuisine/       ← Recipes organized by cuisine
│   ├── american/
│   ├── thai/
│   ├── italian/
│   └── ...
├── by-type/          ← Recipes organized by dish type
│   ├── main/
│   ├── salad/
│   ├── dessert/
│   └── ...
├── by-method/        ← Recipes organized by cooking method
│   ├── grilled/
│   ├── baked/
│   ├── one-pot/
│   └── ...
├── index.json        ← Master index with all metadata
└── ingredient-index.json ← Ingredient-to-recipe mapping
```

## Sources

- **Mel's Kitchen Cafe** (48 recipes) — melskitchencafe.com
- **RecipeTin Eats** (43 recipes) — recipetineats.com
- **Total:** 91 recipes (and growing)

## How to Add Recipes

Just paste a URL or recipe name to Atlas. The vault builder cron will:
1. Scrape full content (ingredients, instructions, tips, nutrition)
2. Classify by cuisine, type, and method
3. Add to all search indexes
4. Copy to appropriate category directories

## Rebuild Indexes

```bash
python3 scripts/rebuild_recipe_index.py     # Rebuild master index
python3 scripts/build_ingredient_index.py  # Rebuild ingredient search
```
