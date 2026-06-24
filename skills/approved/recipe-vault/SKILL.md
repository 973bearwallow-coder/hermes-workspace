---
name: recipe-vault
category: productivity
description: "Searchable recipe vault with 90+ recipes organized by cuisine, type, method, and ingredients. Search script, automated scraping, and quality monitoring."
---

# Recipe Vault

## Quick Search
```bash
# What can I make with chicken and lemon, Thai style?
python3 ~/hermes-workspace/scripts/search_recipes.py -i chicken lemon -c thai

# One-pot meals
python3 ~/hermes-workspace/scripts/search_recipes.py -m one-pot

# Grilled chicken
python3 ~/hermes-workspace/scripts/search_recipes.py -i chicken -m grilled
```

## Categories
- **Cuisine:** american, italian, thai, mexican, french, greek, chinese, japanese, vietnamese, middle-eastern
- **Type:** main, side, salad, soup, bread, dessert, appetizer, breakfast, snack
- **Method:** grilled, baked, stovetop, one-pot, stir-fry, slow-cooker, instant-pot, overnight, no-cook, air-fryer, sheet-pan

## Adding Recipes
Paste any recipe URL to Atlas. The vault builder cron scrapes full content and indexes automatically.

## Rebuild
```bash
python3 ~/hermes-workspace/scripts/rebuild_recipe_index.py
python3 ~/hermes/workspace/scripts/build_ingredient_index.py
```
