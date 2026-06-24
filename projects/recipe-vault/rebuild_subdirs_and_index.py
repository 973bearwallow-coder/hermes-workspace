#!/usr/bin/env python3
"""
Create by-cuisine, by-type, by-method subdirectories and copy recipes into them.
Then rebuild index.json with accurate counts.
"""
import json
import os
import re
import shutil
from datetime import datetime

VAULT_DIR = os.path.expanduser("~/hermes-workspace/projects/recipe-vault")
RECIPES_DIR = os.path.join(VAULT_DIR, "recipes")
INDEX_FILE = os.path.join(VAULT_DIR, "index.json")

def ensure_subdirs():
    """Create all subdirectory structures."""
    for cat in ["by-cuisine", "by-type", "by-method"]:
        os.makedirs(os.path.join(VAULT_DIR, cat), exist_ok=True)

def copy_to_subdirs():
    """Copy each recipe file into appropriate by-cuisine, by-type, by-method dirs."""
    # Load index to get metadata
    with open(INDEX_FILE, "r") as f:
        index = json.load(f)
    
    # Build a map from filename -> recipe metadata
    meta_map = {}
    for r in index.get("recipes", []):
        meta_map[r["file"]] = r
    
    copied = 0
    errors = []
    
    for filename in os.listdir(RECIPES_DIR):
        if not filename.endswith(".md"):
            continue
        
        filepath = os.path.join(RECIPES_DIR, filename)
        rel_path = f"recipes/{filename}"
        
        # Get metadata
        meta = meta_map.get(rel_path, {})
        cuisines = meta.get("cuisines", [])
        types = meta.get("types", [])
        methods = meta.get("methods", [])
        
        # If no metadata, try to parse from file
        if not cuisines or not types or not methods:
            with open(filepath, "r") as f:
                content = f.read()
            
            if not cuisines:
                m = re.search(r"\*\*Cuisine:\*\*\s*(.+)", content)
                if m:
                    cuisines = [m.group(1).strip().lower()]
            if not types:
                m = re.search(r"\*\*Type:\*\*\s*(.+)", content)
                if m:
                    types = [m.group(1).strip().lower()]
            if not methods:
                m = re.search(r"\*\*Method:\*\*\s*(.+)", content)
                if m:
                    methods = [m.group(1).strip().lower()]
        
        # Copy to each category
        for cuisine in cuisines:
            dest_dir = os.path.join(VAULT_DIR, "by-cuisine", cuisine)
            os.makedirs(dest_dir, exist_ok=True)
            shutil.copy2(filepath, os.path.join(dest_dir, filename))
            copied += 1
        
        for rtype in types:
            dest_dir = os.path.join(VAULT_DIR, "by-type", rtype)
            os.makedirs(dest_dir, exist_ok=True)
            shutil.copy2(filepath, os.path.join(dest_dir, filename))
            copied += 1
        
        for method in methods:
            dest_dir = os.path.join(VAULT_DIR, "by-method", method)
            os.makedirs(dest_dir, exist_ok=True)
            shutil.copy2(filepath, os.path.join(dest_dir, filename))
            copied += 1
    
    return copied, errors

def rebuild_index():
    """Rebuild index.json from scratch by scanning recipe files."""
    import re
    
    index = {
        "generated": datetime.now().isoformat(),
        "total_recipes": 0,
        "cuisines": {},
        "types": {},
        "methods": {},
        "recipes": []
    }
    
    recipe_files = sorted([f for f in os.listdir(RECIPES_DIR) if f.endswith(".md")])
    
    for filename in recipe_files:
        filepath = os.path.join(RECIPES_DIR, filename)
        file_size = os.path.getsize(filepath)
        
        with open(filepath, "r") as f:
            content = f.read()
        
        # Extract name from first heading
        name_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        name = name_match.group(1).strip() if name_match else filename.replace(".md", "").replace("_", " ").title()
        
        # Extract source URL
        url_match = re.search(r"\[RecipeTin Eats\]\((.+?)\)", content)
        if not url_match:
            url_match = re.search(r"\[Mel's Kitchen Cafe\]\((.+?)\)", content)
        if not url_match:
            url_match = re.search(r"\[Preppy Kitchen\]\((.+?)\)", content)
        if not url_match:
            url_match = re.search(r"\[Rasa Malaysia\]\((.+?)\)", content)
        if not url_match:
            url_match = re.search(r"\[Dad Cooks Dinner\]\((.+?)\)", content)
        url = url_match.group(1) if url_match else ""
        
        # Extract metadata
        cuisines = []
        types = []
        methods = []
        
        cuisine_match = re.search(r"\*\*Cuisine:\*\*\s*(.+)", content)
        if cuisine_match:
            c = cuisine_match.group(1).strip().lower()
            if c:
                cuisines = [c]
        
        type_match = re.search(r"\*\*Type:\*\*\s*(.+)", content)
        if type_match:
            t = type_match.group(1).strip().lower()
            if t:
                types = [t]
        
        method_match = re.search(r"\*\*Method:\*\*\s*(.+)", content)
        if method_match:
            m = method_match.group(1).strip().lower()
            if m:
                methods = [m]
        
        has_full = file_size > 2000
        
        recipe_entry = {
            "name": name,
            "file": f"recipes/{filename}",
            "cuisines": cuisines,
            "types": types,
            "methods": methods,
            "has_full_content": has_full,
            "url": url,
            "size": file_size
        }
        
        index["recipes"].append(recipe_entry)
        
        for c in cuisines:
            index["cuisines"][c] = index["cuisines"].get(c, 0) + 1
        for t in types:
            index["types"][t] = index["types"].get(t, 0) + 1
        for m in methods:
            index["methods"][m] = index["methods"].get(m, 0) + 1
    
    index["total_recipes"] = len(index["recipes"])
    
    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=2)
    
    return index

def main():
    print("=== Recipe Vault: Rebuild Subdirectories & Index ===\n")
    
    # Step 1: Create subdirs
    ensure_subdirs()
    print("✓ Subdirectories created (by-cuisine, by-type, by-method)")
    
    # Step 2: Copy recipes to subdirs
    copied, errors = copy_to_subdirs()
    print(f"✓ Copied {copied} recipe entries to subdirectories")
    if errors:
        print(f"  Errors: {errors}")
    
    # Step 3: Rebuild index
    index = rebuild_index()
    print(f"\n✓ Index rebuilt: {index['total_recipes']} recipes")
    print(f"  Cuisines: {len(index['cuisines'])} categories")
    print(f"  Types: {len(index['types'])} categories")
    print(f"  Methods: {len(index['methods'])} categories")
    
    # Show top categories
    print(f"\n  Top cuisines: {dict(sorted(index['cuisines'].items(), key=lambda x: -x[1])[:5])}")
    print(f"  Top types: {dict(sorted(index['types'].items(), key=lambda x: -x[1])[:5])}")
    print(f"  Top methods: {dict(sorted(index['methods'].items(), key=lambda x: -x[1])[:5])}")
    
    # Verify subdir counts
    for cat in ["by-cuisine", "by-type", "by-method"]:
        base = os.path.join(VAULT_DIR, cat)
        if os.path.exists(base):
            subdirs = os.listdir(base)
            total_files = sum(len(os.listdir(os.path.join(base, d))) for d in subdirs if os.path.isdir(os.path.join(base, d)))
            print(f"  {cat}: {len(subdirs)} categories, {total_files} files")

if __name__ == "__main__":
    main()
