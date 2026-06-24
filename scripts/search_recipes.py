#!/usr/bin/env python3
"""Search the recipe vault by ingredients, cuisine, type, or method."""
import json
import sys
import re
from pathlib import Path

VAULT_DIR = Path.home() / "hermes-workspace" / "projects" / "recipe-vault"
INDEX_FILE = VAULT_DIR / "index.json"
INGREDIENT_FILE = VAULT_DIR / "ingredient-index.json"

def search(ingredients=None, cuisine=None, recipe_type=None, method=None, limit=10):
    """Search recipes by multiple criteria."""
    
    # Load data
    try:
        recipe_index = json.load(open(INDEX_FILE))
    except:
        print("❌ Index not found. Run rebuild_recipe_index.py first.")
        return
    
    try:
        ingredient_index = json.load(open(INGREDIENT_FILE))
    except:
        ingredient_index = {}
    
    # Get all recipe names
    all_recipes = {r['name'] for r in recipe_index['recipes']}
    matches = all_recipes.copy()
    
    # Filter by ingredients (AND logic — recipe must contain ALL specified ingredients)
    if ingredients:
        for ing in ingredients:
            ing_lower = ing.lower().strip()
            found = set()
            for key, recipes in ingredient_index.items():
                if ing_lower in key:
                    found.update(recipes)
            matches = matches & found
    
    # Filter by cuisine
    if cuisine:
        cuisine_lower = cuisine.lower()
        cuisine_matches = set()
        for r in recipe_index['recipes']:
            if any(cuisine_lower in c.lower() for c in r.get('cuisines', [])):
                cuisine_matches.add(r['name'])
        matches = matches & cuisine_matches
    
    # Filter by type
    if recipe_type:
        type_lower = recipe_type.lower()
        type_matches = set()
        for r in recipe_index['recipes']:
            if any(type_lower in t.lower() for t in r.get('types', [])):
                type_matches.add(r['name'])
        matches = matches & type_matches
    
    # Filter by method
    if method:
        method_lower = method.lower()
        method_matches = set()
        for r in recipe_index['recipes']:
            if any(method_lower in m.lower() for m in r.get('methods', [])):
                method_matches.add(r['name'])
        matches = matches & method_matches
    
    # Output results
    results = sorted(matches)[:limit]
    
    if not results:
        print(f"❌ No recipes found")
        return
    
    # Build search description
    parts = []
    if ingredients:
        parts.append(f"with {', '.join(ingredients)}")
    if cuisine:
        parts.append(f"{cuisine} cuisine")
    if recipe_type:
        parts.append(f"{recipe_type} type")
    if method:
        parts.append(f"{method} method")
    
    desc = " ".join(parts) if parts else "all recipes"
    print(f"🍳 Found {len(matches)} recipes {desc}:\n")
    
    for i, name in enumerate(results, 1):
        # Get recipe details
        recipe_info = None
        for r in recipe_index['recipes']:
            if r['name'] == name:
                recipe_info = r
                break
        
        if recipe_info:
            cuisines = ', '.join(recipe_info.get('cuisines', []))
            types = ', '.join(recipe_info.get('types', []))
            has_content = '✅' if recipe_info.get('has_full_content') else '⚠️'
            print(f"  {i}. {has_content} {name}")
            print(f"     Cuisine: {cuisines} | Type: {types}")
        else:
            print(f"  {i}. {name}")
    
    if len(matches) > limit:
        print(f"\n  ... and {len(matches) - limit} more")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Search recipe vault')
    parser.add_argument('--ingredients', '-i', nargs='+', help='Ingredients to search for')
    parser.add_argument('--cuisine', '-c', help='Cuisine type')
    parser.add_argument('--type', '-t', help='Dish type (main, side, dessert, etc.)')
    parser.add_argument('--method', '-m', help='Cooking method (grilled, baked, etc.)')
    parser.add_argument('--limit', '-l', type=int, default=10, help='Max results')
    args = parser.parse_args()
    
    search(args.ingredients, args.cuisine, args.type, args.method, args.limit)
