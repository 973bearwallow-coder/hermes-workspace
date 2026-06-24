#!/usr/bin/env python3
"""
Create symlinks in by-cuisine/, by-type/, by-method/ for all recipes.
Reads classification from each recipe file's front matter.
Run from the recipe-vault directory.
"""
import os
import re

VAULT_DIR = os.path.expanduser("~/hermes-workspace/projects/recipe-vault")
RECIPES_DIR = os.path.join(VAULT_DIR, "recipes")

def parse_recipe_metadata(filepath):
    """Extract cuisine, type, method from recipe front matter."""
    metadata = {"cuisines": [], "types": [], "methods": []}
    try:
        with open(filepath, 'r') as f:
            content = f.read(2000)  # Read first 2000 chars for front matter
        
        # Parse Cuisine
        cuisine_match = re.search(r'\*\*Cuisine:\*\*\s*(.+?)(?:\n|$)', content)
        if cuisine_match:
            metadata["cuisines"] = [c.strip() for c in cuisine_match.group(1).split(',')]
        
        # Parse Type
        type_match = re.search(r'\*\*Type:\*\*\s*(.+?)(?:\n|$)', content)
        if type_match:
            metadata["types"] = [t.strip() for t in type_match.group(1).split(',')]
        
        # Parse Method
        method_match = re.search(r'\*\*Method:\*\*\s*(.+?)(?:\n|$)', content)
        if method_match:
            metadata["methods"] = [m.strip() for m in method_match.group(1).split(',')]
    except Exception as e:
        print(f"  Error reading {filepath}: {e}")
    
    return metadata

def main():
    # Clean existing symlinks in classification dirs
    for sub in ["by-cuisine", "by-type", "by-method"]:
        sub_path = os.path.join(VAULT_DIR, sub)
        if os.path.exists(sub_path):
            for root, dirs, files in os.walk(sub_path):
                for f in files:
                    fp = os.path.join(root, f)
                    if os.path.islink(fp):
                        os.unlink(fp)
    print("Cleaned existing symlinks.")
    
    symlink_count = 0
    recipe_files = sorted([f for f in os.listdir(RECIPES_DIR) if f.endswith('.md')])
    
    for filename in recipe_files:
        recipe_path = os.path.join(RECIPES_DIR, filename)
        meta = parse_recipe_metadata(recipe_path)
        
        for cuisine in meta["cuisines"]:
            d = os.path.join(VAULT_DIR, "by-cuisine", cuisine)
            os.makedirs(d, exist_ok=True)
            link_path = os.path.join(d, filename)
            if not os.path.exists(link_path) and not os.path.islink(link_path):
                os.symlink(os.path.relpath(recipe_path, d), link_path)
                symlink_count += 1
        
        for rtype in meta["types"]:
            d = os.path.join(VAULT_DIR, "by-type", rtype)
            os.makedirs(d, exist_ok=True)
            link_path = os.path.join(d, filename)
            if not os.path.exists(link_path) and not os.path.islink(link_path):
                os.symlink(os.path.relpath(recipe_path, d), link_path)
                symlink_count += 1
        
        for method in meta["methods"]:
            d = os.path.join(VAULT_DIR, "by-method", method)
            os.makedirs(d, exist_ok=True)
            link_path = os.path.join(d, filename)
            if not os.path.exists(link_path) and not os.path.islink(link_path):
                os.symlink(os.path.relpath(recipe_path, d), link_path)
                symlink_count += 1
    
    print(f"Created {symlink_count} symlinks for {len(recipe_files)} recipes.")
    
    # Count by directory
    for sub in ["by-cuisine", "by-type", "by-method"]:
        sub_path = os.path.join(VAULT_DIR, sub)
        if os.path.exists(sub_path):
            dirs = {}
            for d in os.listdir(sub_path):
                dp = os.path.join(sub_path, d)
                if os.path.isdir(dp):
                    count = len([f for f in os.listdir(dp) if os.path.islink(os.path.join(dp, f))])
                    if count > 0:
                        dirs[d] = count
            print(f"\n{sub}:")
            for name, count in sorted(dirs.items(), key=lambda x: x[1], reverse=True):
                print(f"  {name}: {count}")

if __name__ == "__main__":
    main()
