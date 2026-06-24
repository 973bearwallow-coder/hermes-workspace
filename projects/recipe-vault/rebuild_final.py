#!/usr/bin/env python3
"""Final rebuild: verify all 43 recipes, rebuild subdirs, rebuild index."""
import json
import os
import shutil
from datetime import datetime

VAULT_DIR = os.path.expanduser("~/hermes-workspace/projects/recipe-vault")
RECIPES_DIR = os.path.join(VAULT_DIR, "recipes")
INDEX_FILE = os.path.join(VAULT_DIR, "index.json")

RECIPES_43 = [
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

# Load existing index
with open(INDEX_FILE, "r") as f:
    old_index = json.load(f)

existing_by_file = {}
for r in old_index.get("recipes", []):
    existing_by_file[os.path.basename(r["file"])] = r

# Step 1: Verify all 43 recipes exist with content
print("=== STEP 1: Verify 43 recipes ===")
ok = 0
missing = []
for recipe in RECIPES_43:
    fname = recipe["slug"] + ".md"
    fpath = os.path.join(RECIPES_DIR, fname)
    if os.path.exists(fpath) and os.path.getsize(fpath) > 1500:
        ok += 1
    else:
        missing.append(recipe["name"])
        print(f"  MISSING: {recipe['name']} ({fname})")

print(f"Present with content: {ok}/43")
if missing:
    print(f"Missing: {missing}")

# Step 2: Clean and rebuild subdirs
print("\n=== STEP 2: Rebuild subdirectories ===")
for subdir in ["by-cuisine", "by-type", "by-method"]:
    subdir_path = os.path.join(VAULT_DIR, subdir)
    if os.path.exists(subdir_path):
        shutil.rmtree(subdir_path)
    os.makedirs(subdir_path, exist_ok=True)

# Build metadata map for all recipes
meta_map = {}
for recipe in RECIPES_43:
    fname = recipe["slug"] + ".md"
    meta_map[fname] = recipe

# Add existing recipes from old index
for r in old_index.get("recipes", []):
    fname = os.path.basename(r["file"])
    if fname not in meta_map:
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
for fname, meta in meta_map.items():
    src = os.path.join(RECIPES_DIR, fname)
    if not os.path.exists(src):
        continue
    cuisine = meta.get("cuisine", "unknown")
    rtype = meta.get("type", "main")
    method = meta.get("method", "stovetop")
    for subdir, key in [("by-cuisine", cuisine), ("by-type", rtype), ("by-method", method)]:
        dest_dir = os.path.join(VAULT_DIR, subdir, key)
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy2(src, os.path.join(dest_dir, fname))
    copied += 1

print(f"Copied {copied} recipes to subdirectories")

# Step 3: Rebuild index
print("\n=== STEP 3: Rebuild index ===")
new_index = {
    "generated": datetime.now().isoformat(),
    "total_recipes": 0,
    "cuisines": {},
    "types": {},
    "methods": {},
    "recipes": []
}

all_files = sorted([f for f in os.listdir(RECIPES_DIR) if f.endswith(".md")])

for fname in all_files:
    fpath = os.path.join(RECIPES_DIR, fname)
    fsize = os.path.getsize(fpath)

    if fname in existing_by_file:
        old = existing_by_file[fname]
        name = old["name"]
        cuisines = old.get("cuisines", [])
        types = old.get("types", [])
        methods = old.get("methods", [])
        url = old.get("url", "")
        has_full = old.get("has_full_content", fsize > 2000)
    elif fname in meta_map:
        m = meta_map[fname]
        name = m["name"]
        cuisines = [m["cuisine"]] if m.get("cuisine") else []
        types = [m["type"]] if m.get("type") else []
        methods = [m["method"]] if m.get("method") else []
        url = f"https://www.recipetineats.com/{m['slug']}/"
        has_full = fsize > 2000
    else:
        # Parse from file header
        with open(fpath, "r") as f:
            content = f.read(500)
        import re
        nm = re.search(r"^# (.+)$", content, re.MULTILINE)
        name = nm.group(1).strip() if nm else fname.replace(".md", "").replace("_", " ").title()
        urlm = re.search(r"\[([^\]]*)\]\((https?://[^)]+)\)", content)
        url = urlm.group(2) if urlm else ""
        cm = re.search(r"\*\*Cuisine:\*\*\s*(.+)", content)
        cuisines = [cm.group(1).strip().lower()] if cm and cm.group(1).strip() not in ("", "n/a") else []
        tm = re.search(r"\*\*Type:\*\*\s*(.+)", content)
        types = [tm.group(1).strip().lower()] if tm and tm.group(1).strip() not in ("", "n/a") else []
        mm = re.search(r"\*\*Method:\*\*\s*(.+)", content)
        methods = [mm.group(1).strip().lower()] if mm and mm.group(1).strip() not in ("", "n/a") else []
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

print(f"Index rebuilt: {new_index['total_recipes']} recipes")
full_count = sum(1 for r in new_index['recipes'] if r['has_full_content'])
print(f"With full content: {full_count}")
print(f"Without full content: {new_index['total_recipes'] - full_count}")

# Count subdir files
for subdir in ["by-cuisine", "by-type", "by-method"]:
    subdir_path = os.path.join(VAULT_DIR, subdir)
    if os.path.exists(subdir_path):
        count = sum(1 for root, dirs, files in os.walk(subdir_path) for f2 in files if f2.endswith(".md"))
        print(f"Files in {subdir}: {count}")

print("\n=== Cuisine distribution ===")
for k, v in sorted(new_index["cuisines"].items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")
print("\n=== Type distribution ===")
for k, v in sorted(new_index["types"].items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")
print("\n=== Method distribution ===")
for k, v in sorted(new_index["methods"].items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")

print("\n=== DONE ===")
