#!/usr/bin/env python3
"""Rebuild by-cuisine/, by-type/, by-method/ symlink directories and index.json"""

import json
import os
import shutil

VAULT_DIR = os.path.dirname(os.path.abspath(__file__))
RECIPES_DIR = os.path.join(VAULT_DIR, "recipes")
INDEX_FILE = os.path.join(VAULT_DIR, "index.json")

# Classification directories
SUBDIRS = ["by-cuisine", "by-type", "by-method"]

def clean_symlinks():
    """Remove all existing symlink directories"""
    for sub in SUBDIRS:
        sub_path = os.path.join(VAULT_DIR, sub)
        if os.path.exists(sub_path):
            shutil.rmtree(sub_path)
        os.makedirs(sub_path, exist_ok=True)

def create_symlinks(recipes):
    """Create symlink directories for all recipes"""
    for recipe in recipes:
        fname = recipe["file"]
        cuisines = recipe.get("cuisines", [])
        types = recipe.get("types", [])
        methods = recipe.get("methods", [])
        
        recipe_path = os.path.join(RECIPES_DIR, fname)
        if not os.path.exists(recipe_path):
            print(f"  WARNING: Recipe file not found: {fname}")
            continue
        
        for cuisine in cuisines:
            dir_path = os.path.join(VAULT_DIR, "by-cuisine", cuisine)
            os.makedirs(dir_path, exist_ok=True)
            link_path = os.path.join(dir_path, fname)
            if not os.path.exists(link_path):
                os.symlink(os.path.relpath(recipe_path, dir_path), link_path)
        
        for rtype in types:
            dir_path = os.path.join(VAULT_DIR, "by-type", rtype)
            os.makedirs(dir_path, exist_ok=True)
            link_path = os.path.join(dir_path, fname)
            if not os.path.exists(link_path):
                os.symlink(os.path.relpath(recipe_path, dir_path), link_path)
        
        for method in methods:
            dir_path = os.path.join(VAULT_DIR, "by-method", method)
            os.makedirs(dir_path, exist_ok=True)
            link_path = os.path.join(dir_path, fname)
            if not os.path.exists(link_path):
                os.symlink(os.path.relpath(recipe_path, dir_path), link_path)

def rebuild_index(recipes):
    """Rebuild index.json with current recipe data"""
    # Count categories
    cuisines_count = {}
    types_count = {}
    methods_count = {}
    
    for recipe in recipes:
        for c in recipe.get("cuisines", []):
            cuisines_count[c] = cuisines_count.get(c, 0) + 1
        for t in recipe.get("types", []):
            types_count[t] = types_count.get(t, 0) + 1
        for m in recipe.get("methods", []):
            methods_count[m] = methods_count.get(m, 0) + 1
    
    # Sort by count descending
    cuisines_sorted = dict(sorted(cuisines_count.items(), key=lambda x: -x[1]))
    types_sorted = dict(sorted(types_count.items(), key=lambda x: -x[1]))
    methods_sorted = dict(sorted(methods_count.items(), key=lambda x: -x[1]))
    
    index = {
        "generated": "2026-06-17T02:00:00",
        "total_recipes": len(recipes),
        "cuisines": cuisines_sorted,
        "types": types_sorted,
        "methods": methods_sorted,
        "recipes": recipes
    }
    
    with open(INDEX_FILE, 'w') as f:
        json.dump(index, f, indent=2)
    
    return index

def main():
    # Read existing index
    with open(INDEX_FILE, 'r') as f:
        old_index = json.load(f)
    
    recipes = old_index["recipes"]
    
    print(f"Total recipes in index: {len(recipes)}")
    
    # Check for recipe files that exist on disk but aren't in index
    indexed_files = {r["file"] for r in recipes}
    disk_files = set(os.listdir(RECIPES_DIR))
    missing_from_index = disk_files - indexed_files
    if missing_from_index:
        print(f"\nFiles on disk but not in index ({len(missing_from_index)}):")
        for f in sorted(missing_from_index):
            print(f"  - {f}")
    
    # Check for recipes in index but not on disk
    missing_from_disk = indexed_files - disk_files
    if missing_from_disk:
        print(f"\nFiles in index but not on disk ({len(missing_from_disk)}):")
        for f in sorted(missing_from_disk):
            print(f"  - {f}")
    
    # Clean and rebuild symlinks
    print("\nCleaning old symlink directories...")
    clean_symlinks()
    print("Creating new symlinks...")
    create_symlinks(recipes)
    
    # Rebuild index
    print("Rebuilding index.json...")
    new_index = rebuild_index(recipes)
    
    # Report
    print(f"\n{'='*50}")
    print(f"VAULT REBUILD COMPLETE")
    print(f"{'='*50}")
    print(f"Total recipes: {new_index['total_recipes']}")
    print(f"\nCuisines ({len(new_index['cuisines'])}):")
    for c, n in new_index['cuisines'].items():
        print(f"  {c}: {n}")
    print(f"\nTypes ({len(new_index['types'])}):")
    for t, n in new_index['types'].items():
        print(f"  {t}: {n}")
    print(f"\nMethods ({len(new_index['methods'])}):")
    for m, n in new_index['methods'].items():
        print(f"  {m}: {n}")
    
    # Count symlinks
    for sub in SUBDIRS:
        sub_path = os.path.join(VAULT_DIR, sub)
        if os.path.exists(sub_path):
            link_count = sum(1 for root, dirs, files in os.walk(sub_path) 
                           for f in files if os.path.islink(os.path.join(root, f)))
            dir_count = sum(1 for _, dirs, _ in os.walk(sub_path) for _ in dirs)
            print(f"\n{sub}/: {dir_count} categories, {link_count} symlinks")

if __name__ == "__main__":
    main()
