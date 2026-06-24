#!/usr/bin/env python3
"""Verify all 43 recipes exist with content, rebuild index, ensure subdir copies."""
import json
import os
import shutil
from datetime import datetime

VAULT_DIR = os.path.expanduser("~/hermes-workspace/projects/recipe-vault")
RECIPES_DIR = os.path.join(VAULT_DIR, "recipes")
INDEX_FILE = os.path.join(VAULT_DIR, "index.json")

RECIPES = [
    {"name": "French Chicken au Poivre Sauce", "slug": "french-chicken-au-poivre-sauce", "cuisine": "french", "type": "main", "method": "stovetop"},
    {"name": "Thai Grilled Chicken (Gai Yang)", "slug": "thai-grilled-chicken-gai-yang", "cuisine": "thai", "type": "main", "method": "grilled"},
    {"name": "Chicken Chasseur", "slug": "chicken-chasseur", "cuisine": "french", "type": "main", "method": "stovetop"},
    {"name": "New Orleans Chicken Wings", "slug": "new-orleans-chicken-wings", "cuisine": "american", "type": "appetizer", "method": "baked"},
    {"name": "Chicken Cacciatore (Italian Chicken Stew)", "slug": "chicken-cacciatore", "cuisine": "italian", "type": "main", "method": "stovetop"},
    {"name": "Chicken Francese", "slug": "chicken-francese", "cuisine": "italian", "type": "main", "method": "stovetop"},
    {"name": "Vietnamese Caramel Ginger Chicken", "slug": "vietnamese-caramel-ginger-chicken", "cuisine": "vietnamese", "type": "main", "method": "stovetop"},
    {"name": "Chicken Marsala", "slug": "chicken-marsala", "cuisine": "italian", "type": "main", "method": "stovetop"},
    {"name": "One Pot Baked Greek Chicken Orzo Risoni", "slug": "one-pot-baked-greek-chicken-orzo-risoni", "cuisine": "greek", "type": "main", "method": "one-pot"},
    {"name": "Thai Red Curry Pot Roast Chicken", "slug": "thai-red-curry-pot-roast-chicken", "cuisine": "thai", "type": "main", "method": "baked"},
    {"name": "Chicken in Creamy Mustard Sauce", "slug": "chicken-in-creamy-mustard-sauce", "cuisine": "french", "type": "main", "method": "stovetop"},
    {"name": "Chicken Shawarma (Middle Eastern)", "slug": "chicken-shawarma-middle-eastern", "cuisine": "middle-eastern", "type": "main", "method": "stovetop"},
    {"name": "Coq au Vin", "slug": "coq-au-vin", "cuisine": "french", "type": "main", "method": "stovetop"},
    {"name": "Chicken Piccata", "slug": "chicken-piccata", "cuisine": "italian", "type": "main", "method": "stovetop"},
    {"name": "Creamy Chicken Mushroom Fettucine", "slug": "creamy-chicken-mushroom-fettucine", "cuisine": "italian", "type": "main", "method": "stovetop"},
    {"name": "Creamy Tuscan Chicken Pasta Bake", "slug": "creamy-tuscan-chicken-pasta-bake", "cuisine": "italian", "type": "main", "method": "baked"},
    {"name": "Chicken Broccoli Stir Fry", "slug": "chicken-broccoli-stir-fry", "cuisine": "chinese", "type": "main", "method": "stir-fry"},
    {"name": "Thai Chicken Lettuce Cups (Larb Gai / Laab Gai)", "slug": "thai-chicken-lettuce-cups-larb-gai", "cuisine": "thai", "type": "appetizer", "method": "stovetop"},
    {"name": "Chicken Pad Thai", "slug": "chicken-pad-thai", "cuisine": "thai", "type": "main", "method": "stir-fry"},
    {"name": "Chicken Chow Mein", "slug": "chicken-chow-mein", "cuisine": "chinese", "type": "main", "method": "stir-fry"},
    {"name": "Thai Basil Chicken Stir Fry", "slug": "thai-basil-chicken-stir-fry", "cuisine": "thai", "type": "main", "method": "stir-fry"},
    {"name": "Chicken with Creamy Sun Dried Tomato Sauce", "slug": "chicken-with-creamy-sun-dried-tomato-sauce", "cuisine": "italian", "type": "main", "method": "stovetop"},
    {"name": "Pad Kee Mao (Thai Drunken Noodles)", "slug": "pad-kee-mao-thai-drunken-noodles", "cuisine": "thai", "type": "main", "method": "stir-fry"},
    {"name": "Jambalaya Recipe", "slug": "jambalaya-recipe", "cuisine": "american", "type": "main", "method": "one-pot"},
    {"name": "Chicken Pasta Recipe", "slug": "chicken-pasta-recipe", "cuisine": "italian", "type": "main", "method": "stovetop"},
    {"name": "Chinese Cashew Chicken", "slug": "chinese-cashew-chicken", "cuisine": "chinese", "type": "main", "method": "stir-fry"},
    {"name": "Chicken Pot Pie", "slug": "chicken-pot-pie", "cuisine": "american", "type": "main", "method": "baked"},
    {"name": "Lemon Chicken Salad", "slug": "lemon-chicken-salad", "cuisine": "american", "type": "salad", "method": "stovetop"},
    {"name": "Mexican Chicken Avocado Salad", "slug": "mexican-chicken-avocado-salad", "cuisine": "mexican", "type": "salad", "method": "grilled"},
    {"name": "Oven Baked Chicken and Rice Pilaf (Cranberry Walnut Apple)", "slug": "oven-baked-chicken-and-rice-pilaf", "cuisine": "american", "type": "main", "method": "baked"},
    {"name": "Vietnamese Coconut Caramel Chicken", "slug": "vietnamese-coconut-caramel-chicken", "cuisine": "vietnamese", "type": "main", "method": "stovetop"},
    {"name": "Thai Coconut Chicken", "slug": "thai-coconut-chicken", "cuisine": "thai", "type": "main", "method": "grilled"},
    {"name": "Oven Baked Chicken Quesadillas", "slug": "oven-baked-chicken-quesadillas", "cuisine": "mexican", "type": "main", "method": "baked"},
    {"name": "Creamy Chicken and Bacon Pasta", "slug": "creamy-chicken-and-bacon-pasta", "cuisine": "italian", "type": "main", "method": "stovetop"},
    {"name": "Chicken and Mushroom Risotto", "slug": "chicken-and-mushroom-risotto", "cuisine": "italian", "type": "main", "method": "stovetop"},
    {"name": "Mexican Shredded Chicken", "slug": "mexican-shredded-chicken", "cuisine": "mexican", "type": "main", "method": "slow-cooker"},
    {"name": "One Pot Chicken Enchilada Rice Casserole", "slug": "one-pot-chicken-enchilada-rice-casserole", "cuisine": "mexican", "type": "main", "method": "one-pot"},
    {"name": "One Pot Creamy Parmesan Garlic Risotto with Lemon Pepper Chicken", "slug": "one-pot-creamy-parmesan-garlic-risotto", "cuisine": "italian", "type": "main", "method": "one-pot"},
    {"name": "One Pot Greek Chicken Lemon Rice", "slug": "one-pot-greek-chicken-lemon-rice", "cuisine": "greek", "type": "main", "method": "one-pot"},
    {"name": "Jamaican Jerk Chicken Drumsticks with Caribbean Rice and Beans", "slug": "jamaican-jerk-chicken-drumsticks", "cuisine": "jamaican", "type": "main", "method": "baked"},
    {"name": "One Pan Spanish Chicken Chorizo Tomato Potatoes", "slug": "one-pan-spanish-chicken-chorizo", "cuisine": "spanish", "type": "main", "method": "baked"},
    {"name": "Crispy Shredded Chicken Noodle Stir Fry", "slug": "crispy-shredded-chicken-noodle-stir-fry", "cuisine": "chinese", "type": "main", "method": "stir-fry"},
    {"name": "10 Classic Chinese Dishes + Homemade Teriyaki Sauce", "slug": "10-classic-chinese-dishes", "cuisine": "chinese", "type": "main", "method": "stir-fry"},
]

# Build a map from slug to recipe
slug_map = {r["slug"]: r for r in RECIPES}

# Load existing index
with open(INDEX_FILE, "r") as f:
    index = json.load(f)

# Build a map from existing index: name -> entry
existing_by_name = {}
for r in index.get("recipes", []):
    existing_by_name[r["name"]] = r

# Also build map by filename
existing_by_file = {}
for r in index.get("recipes", []):
    existing_by_file[r["file"]] = r

print(f"Existing index has {len(index['recipes'])} recipes")
print(f"Checking {len(RECIPES)} target recipes...")

missing = []
has_content = []
needs_copy = []

for recipe in RECIPES:
    fname = recipe["slug"] + ".md"
    fpath = os.path.join(RECIPES_DIR, fname)
    
    if not os.path.exists(fpath):
        # Try to find by name in existing index
        if recipe["name"] in existing_by_name:
            entry = existing_by_name[recipe["name"]]
            actual_file = os.path.join(VAULT_DIR, entry["file"])
            if os.path.exists(actual_file) and os.path.getsize(actual_file) > 2000:
                has_content.append((recipe, entry))
                continue
        missing.append(recipe)
    else:
        size = os.path.getsize(fpath)
        if size > 1500:
            has_content.append((recipe, None))
        else:
            missing.append(recipe)

print(f"\nAlready present with content: {len(has_content)}")
print(f"Missing or stub: {len(missing)}")

if missing:
    print("\nMissing recipes:")
    for r in missing:
        print(f"  - {r['name']}")

# Now ensure all existing recipe files are in proper subdirs
# First, clean up old subdirs
for subdir in ["by-cuisine", "by-type", "by-method"]:
    subdir_path = os.path.join(VAULT_DIR, subdir)
    if os.path.exists(subdir_path):
        shutil.rmtree(subdir_path)
    os.makedirs(subdir_path, exist_ok=True)

# Now copy all recipe files to subdirs based on their metadata
# Build metadata map from existing index + our 43 recipes
meta_map = {}  # filename -> recipe metadata

# From our 43 recipes
for recipe in RECIPES:
    fname = recipe["slug"] + ".md"
    meta_map[fname] = recipe

# From existing index, for recipes not in our 43 list
for r in index.get("recipes", []):
    fname = os.path.basename(r["file"])
    if fname not in meta_map:
        # Build a recipe-like entry from index data
        cuisines = r.get("cuisines", [])
        types = r.get("types", [])
        methods = r.get("methods", [])
        meta_map[fname] = {
            "name": r["name"],
            "slug": fname.replace(".md", ""),
            "cuisine": cuisines[0] if cuisines else "unknown",
            "type": types[0] if types else "main",
            "method": methods[0] if methods else "stovetop",
        }

copied = 0
errors = []
for fname, meta in meta_map.items():
    src = os.path.join(RECIPES_DIR, fname)
    if not os.path.exists(src):
        continue
    
    cuisine = meta.get("cuisine", "unknown")
    rtype = meta.get("type", "main")
    method = meta.get("method", "stovetop")
    
    # by-cuisine
    cuisine_dir = os.path.join(VAULT_DIR, "by-cuisine", cuisine)
    os.makedirs(cuisine_dir, exist_ok=True)
    try:
        shutil.copy2(src, os.path.join(cuisine_dir, fname))
    except Exception as e:
        errors.append(f"cuisine copy failed for {fname}: {e}")
    
    # by-type
    type_dir = os.path.join(VAULT_DIR, "by-type", rtype)
    os.makedirs(type_dir, exist_ok=True)
    try:
        shutil.copy2(src, os.path.join(type_dir, fname))
    except Exception as e:
        errors.append(f"type copy failed for {fname}: {e}")
    
    # by-method
    method_dir = os.path.join(VAULT_DIR, "by-method", method)
    os.makedirs(method_dir, exist_ok=True)
    try:
        shutil.copy2(src, os.path.join(method_dir, fname))
    except Exception as e:
        errors.append(f"method copy failed for {fname}: {e}")
    
    copied += 1

print(f"\nCopied {copied} recipes to subdirectories")
if errors:
    print(f"Errors: {len(errors)}")
    for e in errors:
        print(f"  {e}")

# Now rebuild the index completely from the recipe files + existing metadata
print("\nRebuilding index.json...")
new_index = {
    "generated": datetime.now().isoformat(),
    "total_recipes": 0,
    "cuisines": {},
    "types": {},
    "methods": {},
    "recipes": []
}

# Get all .md files in recipes dir
all_files = sorted([f for f in os.listdir(RECIPES_DIR) if f.endswith(".md")])

for fname in all_files:
    fpath = os.path.join(RECIPES_DIR, fname)
    fsize = os.path.getsize(fpath)
    
    # Try to get metadata from existing index
    if fname in existing_by_file:
        old = existing_by_file[fname]
        name = old["name"]
        cuisines = old.get("cuisines", [])
        types = old.get("types", [])
        methods = old.get("methods", [])
        url = old.get("url", "")
        has_full = old.get("has_full_content", fsize > 2000)
    elif fname in meta_map:
        meta = meta_map[fname]
        name = meta["name"]
        cuisines = [meta.get("cuisine", "")] if meta.get("cuisine") else []
        types = [meta.get("type", "")] if meta.get("type") else []
        methods = [meta.get("method", "")] if meta.get("method") else []
        url = f"https://www.recipetineats.com/{meta.get('slug', fname.replace('.md', ''))}/"
        has_full = fsize > 2000
    else:
        # Parse from file
        with open(fpath, "r") as f:
            content = f.read(500)
        import re
        name_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        name = name_match.group(1).strip() if name_match else fname.replace(".md", "").replace("_", " ").title()
        url_match = re.search(r"\[RecipeTin Eats\]\((.+?)\)", content)
        if not url_match:
            url_match = re.search(r"\[Mel's Kitchen Cafe\]\((.+?)\)", content)
        if not url_match:
            url_match = re.search(r"\[Preppy Kitchen\]\((.+?)\)", content)
        if not url_match:
            url_match = re.search(r"\[Rasa Malaysia\]\((.+?)\)", content)
        url = url_match.group(1) if url_match else ""
        
        cuisines = []
        types = []
        methods = []
        cm = re.search(r"\*\*Cuisine:\*\*\s*(.+)", content)
        if cm and cm.group(1).strip().lower() not in ("", "n/a"):
            cuisines = [cm.group(1).strip().lower()]
        tm = re.search(r"\*\*Type:\*\*\s*(.+)", content)
        if tm and tm.group(1).strip().lower() not in ("", "n/a"):
            types = [tm.group(1).strip().lower()]
        mm = re.search(r"\*\*Method:\*\*\s*(.+)", content)
        if mm and mm.group(1).strip().lower() not in ("", "n/a"):
            methods = [mm.group(1).strip().lower()]
        has_full = fsize > 2000
    
    entry = {
        "name": name,
        "file": f"recipes/{fname}",
        "cuisines": cuisines,
        "types": types,
        "methods": methods,
        "has_full_content": has_full,
        "url": url,
        "size": fsize
    }
    new_index["recipes"].append(entry)
    
    for c in cuisines:
        new_index["cuisines"][c] = new_index["cuisines"].get(c, 0) + 1
    for t in types:
        new_index["types"][t] = new_index["types"].get(t, 0) + 1
    for m in methods:
        new_index["methods"][m] = new_index["methods"].get(m, 0) + 1

new_index["total_recipes"] = len(new_index["recipes"])

with open(INDEX_FILE, "w") as f:
    json.dump(new_index, f, indent=2)

print(f"\nIndex rebuilt: {new_index['total_recipes']} recipes")
print(f"Cuisines: {dict(sorted(new_index['cuisines'].items()))}")
print(f"Types: {dict(sorted(new_index['types'].items()))}")
print(f"Methods: {dict(sorted(new_index['methods'].items()))}")

# Final verification
print("\n--- VERIFICATION ---")
print(f"Total recipes in index: {new_index['total_recipes']}")
full_count = sum(1 for r in new_index['recipes'] if r['has_full_content'])
print(f"With full content: {full_count}")
print(f"Without full content: {new_index['total_recipes'] - full_count}")

# Count files in subdirs
for subdir in ["by-cuisine", "by-type", "by-method"]:
    subdir_path = os.path.join(VAULT_DIR, subdir)
    if os.path.exists(subdir_path):
        count = sum(1 for root, dirs, files in os.walk(subdir_path) for f in files if f.endswith(".md"))
        print(f"Files in {subdir}: {count}")
