#!/usr/bin/env python3
"""Build ingredient index for the recipe vault.
Scans all recipe files and creates an ingredient-to-recipe mapping.
"""
import json
import os
import re
from pathlib import Path

VAULT_DIR = Path.home() / "hermes-workspace" / "projects" / "recipe-vault"
RECIPES_DIR = VAULT_DIR / "recipes"
INDEX_FILE = VAULT_DIR / "ingredient-index.json"

def extract_ingredients(filepath):
    """Extract ingredient list from a recipe markdown file."""
    try:
        with open(filepath) as f:
            content = f.read()
    except:
        return []
    
    ingredients = []
    in_ingredients = False
    
    for line in content.split('\n'):
        line = line.strip()
        if line.lower() == '## ingredients':
            in_ingredients = True
            continue
        if in_ingredients:
            if line.startswith('## ') or line.startswith('# '):
                break
            if line.startswith('- '):
                ing = line[2:].strip()
                # Clean up measurements for matching
                ing_clean = re.sub(r'^\d+[\d\s./-]*\s*(cups?|tbsp|tsp|oz|lbs?|pounds?|cloves?|slices?|pieces?|cans?|packages?)\s*', '', ing, flags=re.IGNORECASE).strip()
                ing_clean = re.sub(r'\(.*?\)', '', ing_clean).strip()
                if ing_clean:
                    ingredients.append(ing_clean.lower())
    
    return ingredients

def main():
    index = {}  # ingredient -> list of recipe names
    
    for filename in sorted(os.listdir(RECIPES_DIR)):
        if not filename.endswith('.md'):
            continue
        
        filepath = RECIPES_DIR / filename
        name = filename.replace('.md', '').replace('_', ' ').title()
        ingredients = extract_ingredients(filepath)
        
        for ing in ingredients:
            # Normalize: remove plurals, trim
            ing_key = ing.rstrip('s')  # simple de-plural
            if ing_key not in index:
                index[ing_key] = []
            if name not in index[ing_key]:
                index[ing_key].append(name)
    
    # Sort by number of recipes per ingredient (most common first)
    sorted_index = dict(sorted(index.items(), key=lambda x: -len(x[1])))
    
    INDEX_FILE.write_text(json.dumps(sorted_index, indent=2))
    
    print(f"✅ Ingredient index built: {len(index)} unique ingredients")
    print(f"   Saved to {INDEX_FILE}")
    
    # Show top 20 most common ingredients
    print(f"\n   Top 20 ingredients:")
    for ing, recipes in list(sorted_index.items())[:20]:
        print(f"     {ing}: {len(recipes)} recipes")

if __name__ == "__main__":
    main()
