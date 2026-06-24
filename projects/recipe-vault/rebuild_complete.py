#!/usr/bin/env python3
"""Verify all 43 recipes, rebuild subdirs, rebuild index."""
import json, os, re, shutil
from datetime import datetime

VAULT = os.path.expanduser("~/hermes-workspace/projects/recipe-vault")
RECIPES = os.path.join(VAULT, "recipes")
INDEX = os.path.join(VAULT, "index.json")

TARGET = [
    ("French Chicken au Poivre Sauce", "french-chicken-au-poivre-sauce", "french", "main", "stovetop"),
    ("Thai Grilled Chicken (Gai Yang)", "thai-grilled-chicken-gai-yang", "thai", "main", "grilled"),
    ("Chicken Chasseur", "chicken-chasseur", "french", "main", "stovetop"),
    ("New Orleans Chicken Wings", "new-orleans-chicken-wings", "american", "appetizer", "baked"),
    ("Chicken Cacciatore (Italian Chicken Stew)", "chicken-cacciatore", "italian", "main", "stovetop"),
    ("Chicken Francese", "chicken-francese", "italian", "main", "stovetop"),
    ("Vietnamese Caramel Ginger Chicken", "vietnamese-caramel-ginger-chicken", "vietnamese", "main", "stovetop"),
    ("Chicken Marsala", "chicken-marsala", "italian", "main", "stovetop"),
    ("One Pot Baked Greek Chicken Orzo Risoni", "one-pot-baked-greek-chicken-orzo-risoni", "greek", "main", "one-pot"),
    ("Thai Red Curry Pot Roast Chicken", "thai-red-curry-pot-roast-chicken", "thai", "main", "baked"),
    ("Chicken in Creamy Mustard Sauce", "chicken-in-creamy-mustard-sauce", "french", "main", "stovetop"),
    ("Chicken Shawarma (Middle Eastern)", "chicken-shawarma-middle-eastern", "middle-eastern", "main", "stovetop"),
    ("Coq au Vin", "coq-au-vin", "french", "main", "stovetop"),
    ("Chicken Piccata", "chicken-piccata", "italian", "main", "stovetop"),
    ("Creamy Chicken Mushroom Fettucine", "creamy-chicken-mushroom-fettucine", "italian", "main", "stovetop"),
    ("Creamy Tuscan Chicken Pasta Bake", "creamy-tuscan-chicken-pasta-bake", "italian", "main", "baked"),
    ("Chicken Broccoli Stir Fry", "chicken-broccoli-stir-fry", "chinese", "main", "stir-fry"),
    ("Thai Chicken Lettuce Cups (Larb Gai / Laab Gai)", "thai-chicken-lettuce-cups-larb-gai", "thai", "appetizer", "stovetop"),
    ("Chicken Pad Thai", "chicken-pad-thai", "thai", "main", "stir-fry"),
    ("Chicken Chow Mein", "chicken-chow-mein", "chinese", "main", "stir-fry"),
    ("Thai Basil Chicken Stir Fry", "thai-basil-chicken-stir-fry", "thai", "main", "stir-fry"),
    ("Chicken with Creamy Sun Dried Tomato Sauce", "chicken-with-creamy-sun-dried-tomato-sauce", "italian", "main", "stovetop"),
    ("Pad Kee Mao (Thai Drunken Noodles)", "pad-kee-mao-thai-drunken-noodles", "thai", "main", "stir-fry"),
    ("Jambalaya Recipe", "jambalaya-recipe", "american", "main", "one-pot"),
    ("Chicken Pasta Recipe", "chicken-pasta-recipe", "italian", "main", "stovetop"),
    ("Chinese Cashew Chicken", "chinese-cashew-chicken", "chinese", "main", "stir-fry"),
    ("Chicken Pot Pie", "chicken-pot-pie", "american", "main", "baked"),
    ("Lemon Chicken Salad", "lemon-chicken-salad", "american", "salad", "stovetop"),
    ("Mexican Chicken Avocado Salad", "mexican-chicken-avocado-salad", "mexican", "salad", "grilled"),
    ("Oven Baked Chicken and Rice Pilaf (Cranberry Walnut Apple)", "oven-baked-chicken-and-rice-pilaf", "american", "main", "baked"),
    ("Vietnamese Coconut Caramel Chicken", "vietnamese-coconut-caramel-chicken", "vietnamese", "main", "stovetop"),
    ("Thai Coconut Chicken", "thai-coconut-chicken", "thai", "main", "grilled"),
    ("Oven Baked Chicken Quesadillas", "oven-baked-chicken-quesadillas", "mexican", "main", "baked"),
    ("Creamy Chicken and Bacon Pasta", "creamy-chicken-and-bacon-pasta", "italian", "main", "stovetop"),
    ("Chicken and Mushroom Risotto", "chicken-and-mushroom-risotto", "italian", "main", "stovetop"),
    ("Mexican Shredded Chicken", "mexican-shredded-chicken", "mexican", "main", "slow-cooker"),
    ("One Pot Chicken Enchilada Rice Casserole", "one-pot-chicken-enchilada-rice-casserole", "mexican", "main", "one-pot"),
    ("One Pot Creamy Parmesan Garlic Risotto with Lemon Pepper Chicken", "one-pot-creamy-parmesan-garlic-risotto", "italian", "main", "one-pot"),
    ("One Pot Greek Chicken Lemon Rice", "one-pot-greek-chicken-lemon-rice", "greek", "main", "one-pot"),
    ("Jamaican Jerk Chicken Drumsticks with Caribbean Rice and Beans", "jamaican-jerk-chicken-drumsticks", "jamaican", "main", "baked"),
    ("One Pan Spanish Chicken Chorizo Tomato Potatoes", "one-pan-spanish-chicken-chorizo", "spanish", "main", "baked"),
    ("Crispy Shredded Chicken Noodle Stir Fry", "crispy-shredded-chicken-noodle-stir-fry", "chinese", "main", "stir-fry"),
    ("10 Classic Chinese Dishes + Homemade Teriyaki Sauce", "10-classic-chinese-dishes", "chinese", "main", "stir-fry"),
]

# Load existing index
with open(INDEX) as f:
    old_index = json.load(f)

# Build metadata lookup from existing index
meta_by_file = {}
for r in old_index.get("recipes", []):
    meta_by_file[r["file"]] = r

# Also build from TARGET list
target_meta = {}
for name, slug, cuisine, rtype, method in TARGET:
    fname = slug + ".md"
    target_meta[fname] = {"name": name, "cuisine": cuisine, "type": rtype, "method": method, "slug": slug}

# STEP 1: Verify all 43 target recipes exist with content
print("=== STEP 1: Verify 43 target recipes ===")
ok = 0
missing = []
for name, slug, cuisine, rtype, method in TARGET:
    fpath = os.path.join(RECIPES, slug + ".md")
    if os.path.exists(fpath):
        sz = os.path.getsize(fpath)
        if sz > 1500:
            ok += 1
        else:
            print(f"  STUB: {name} ({sz} bytes)")
            missing.append((name, slug, cuisine, rtype, method))
    else:
        print(f"  MISSING: {name}")
        missing.append((name, slug, cuisine, rtype, method))

print(f"OK: {ok}/43, Missing/stub: {len(missing)}/43")

# STEP 2: Clean and rebuild subdirs
print("\n=== STEP 2: Rebuild subdirectories ===")
for sub in ["by-cuisine", "by-type", "by-method"]:
    p = os.path.join(VAULT, sub)
    if os.path.exists(p):
        shutil.rmtree(p)
    os.makedirs(p, exist_ok=True)

# Build complete meta map for ALL recipe files
all_meta = {}
# From target list (highest priority)
for fname, m in target_meta.items():
    all_meta[fname] = m
# From existing index (for non-target recipes)
for r in old_index.get("recipes", []):
    fname = os.path.basename(r["file"])
    if fname not in all_meta:
        cuisines = r.get("cuisines", [])
        types = r.get("types", [])
        methods = r.get("methods", [])
        all_meta[fname] = {
            "name": r["name"],
            "cuisine": cuisines[0] if cuisines else "unknown",
            "type": types[0] if types else "main",
            "method": methods[0] if methods else "stovetop",
        }

copied = 0
for fname, m in all_meta.items():
    src = os.path.join(RECIPES, fname)
    if not os.path.exists(src):
        continue
    cuisine = m.get("cuisine", "unknown")
    rtype = m.get("type", "main")
    method = m.get("method", "stovetop")
    
    for sub, key in [("by-cuisine", cuisine), ("by-type", rtype), ("by-method", method)]:
        d = os.path.join(VAULT, sub, key)
        os.makedirs(d, exist_ok=True)
        shutil.copy2(src, os.path.join(d, fname))
    copied += 1

print(f"Copied {copied} recipes to subdirs")

# Count files in subdirs
for sub in ["by-cuisine", "by-type", "by-method"]:
    p = os.path.join(VAULT, sub)
    n = sum(1 for _, _, files in os.walk(p) for f in files if f.endswith(".md"))
    print(f"  {sub}: {n} files")

# STEP 3: Rebuild index
print("\n=== STEP 3: Rebuild index.json ===")
new_index = {
    "generated": datetime.now().isoformat(),
    "total_recipes": 0,
    "cuisines": {},
    "types": {},
    "methods": {},
    "recipes": []
}

all_files = sorted(f for f in os.listdir(RECIPES) if f.endswith(".md"))

for fname in all_files:
    fpath = os.path.join(RECIPES, fname)
    fsize = os.path.getsize(fpath)
    rf = f"recipes/{fname}"
    
    # Get metadata: priority > existing index > target list > parse from file
    if rf in meta_by_file:
        old = meta_by_file[rf]
        name = old["name"]
        cuisines = old.get("cuisines", [])
        types = old.get("types", [])
        methods = old.get("methods", [])
        url = old.get("url", "")
        has_full = old.get("has_full_content", fsize > 2000)
    elif fname in target_meta:
        m = target_meta[fname]
        name = m["name"]
        cuisines = [m["cuisine"]]
        types = [m["type"]]
        methods = [m["method"]]
        url = f"https://www.recipetineats.com/{m['slug']}/"
        has_full = fsize > 2000
    else:
        # Parse from file header
        with open(fpath) as f:
            content = f.read(800)
        nm = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        name = nm.group(1).strip() if nm else fname.replace(".md", "").replace("_", " ").title()
        
        # URL
        um = re.search(r"\[RecipeTin Eats\]\((.+?)\)", content)
        if not um: um = re.search(r"\[Mel's Kitchen Cafe\]\((.+?)\)", content)
        if not um: um = re.search(r"\[Preppy Kitchen\]\((.+?)\)", content)
        if not um: um = re.search(r"\[Rasa Malaysia\]\((.+?)\)", content)
        url = um.group(1) if um else ""
        
        # Cuisine/Type/Method
        cuisines, types, methods = [], [], []
        cm = re.search(r"\*\*Cuisine:\*\*\s*(.+)", content)
        if cm and cm.group(1).strip().lower() not in ("", "n/a"): cuisines = [cm.group(1).strip().lower()]
        tm = re.search(r"\*\*Type:\*\*\s*(.+)", content)
        if tm and tm.group(1).strip().lower() not in ("", "n/a"): types = [tm.group(1).strip().lower()]
        mm = re.search(r"\*\*Method:\*\*\s*(.+)", content)
        if mm and mm.group(1).strip().lower() not in ("", "n/a"): methods = [mm.group(1).strip().lower()]
        has_full = fsize > 2000
    
    entry = {
        "name": name, "file": rf,
        "cuisines": cuisines, "types": types, "methods": methods,
        "has_full_content": has_full, "url": url, "size": fsize
    }
    new_index["recipes"].append(entry)
    for c in cuisines: new_index["cuisines"][c] = new_index["cuisines"].get(c, 0) + 1
    for t in types: new_index["types"][t] = new_index["types"].get(t, 0) + 1
    for m in methods: new_index["methods"][m] = new_index["methods"].get(m, 0) + 1

new_index["total_recipes"] = len(new_index["recipes"])

with open(INDEX, "w") as f:
    json.dump(new_index, f, indent=2)

print(f"Index rebuilt: {new_index['total_recipes']} recipes")
full = sum(1 for r in new_index['recipes'] if r['has_full_content'])
print(f"Full content: {full}, Stubs: {new_index['total_recipes'] - full}")
print(f"\nCuisines: {json.dumps(dict(sorted(new_index['cuisines'].items())), indent=2)}")
print(f"Types: {json.dumps(dict(sorted(new_index['types'].items())), indent=2)}")
print(f"Methods: {json.dumps(dict(sorted(new_index['methods'].items())), indent=2)}")

# Verify all 43 are in the new index
print("\n=== FINAL: Verify 43 target recipes in new index ===")
idx_names = {r["name"] for r in new_index["recipes"]}
all_found = True
for name, slug, _, _, _ in TARGET:
    if name not in idx_names:
        print(f"  NOT IN INDEX: {name}")
        all_found = False
if all_found:
    print("All 43 target recipes found in index!")

# Check full content for target recipes
print("\nFull content check for 43 targets:")
for r in new_index["recipes"]:
    target_names = {t[0] for t in TARGET}
    if r["name"] in target_names:
        status = "FULL" if r["has_full_content"] else "STUB"
        print(f"  {status} ({r['size']}b): {r['name']}")
