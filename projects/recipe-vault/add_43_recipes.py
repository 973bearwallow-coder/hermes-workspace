#!/usr/bin/env python3
"""
Add 43 new RecipeTin Eats recipes to the recipe vault.
Handles: fetching content, writing markdown files, copying to subdirs, rebuilding index.
"""
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime

VAULT_DIR = os.path.expanduser("~/hermes-workspace/projects/recipe-vault")
RECIPES_DIR = os.path.join(VAULT_DIR, "recipes")
INDEX_FILE = os.path.join(VAULT_DIR, "index.json")

# The 43 recipes to add, organized with their metadata
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


def url_to_filename(slug):
    """Convert slug to safe filename."""
    name = slug.replace("-", " ").title()
    return f"{slug}.md"


def ensure_dirs():
    """Create necessary directories."""
    os.makedirs(RECIPES_DIR, exist_ok=True)
    for subdir in ["by-cuisine", "by-type", "by-method"]:
        os.makedirs(os.path.join(VAULT_DIR, subdir), exist_ok=True)


def load_existing_index():
    """Load existing index.json."""
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as f:
            return json.load(f)
    return {"generated": "", "total_recipes": 0, "cuisines": {}, "types": {}, "methods": {}, "recipes": []}


def save_index(index):
    """Save index.json."""
    index["generated"] = datetime.now().isoformat()
    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=2)


def safe_filename(name):
    """Create safe filename from recipe name."""
    s = name.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "_", s.strip())
    s = re.sub(r"_+", "_", s)
    return s[:60]


def recipe_exists(index, name):
    """Check if recipe already exists in index."""
    for r in index.get("recipes", []):
        if r["name"] == name:
            return True
    return False


def file_exists_in_recipes(filename):
    """Check if file exists in recipes dir."""
    return os.path.exists(os.path.join(RECIPES_DIR, filename))


def copy_to_subdirs(filepath, recipe):
    """Copy recipe file to by-cuisine, by-type, by-method subdirectories."""
    filename = os.path.basename(filepath)
    name = recipe["name"]
    cuisine = recipe["cuisine"]
    rtype = recipe["type"]
    method = recipe["method"]

    # by-cuisine
    cuisine_dir = os.path.join(VAULT_DIR, "by-cuisine", cuisine)
    os.makedirs(cuisine_dir, exist_ok=True)
    shutil.copy2(filepath, os.path.join(cuisine_dir, filename))

    # by-type
    type_dir = os.path.join(VAULT_DIR, "by-type", rtype)
    os.makedirs(type_dir, exist_ok=True)
    shutil.copy2(filepath, os.path.join(type_dir, filename))

    # by-method
    method_dir = os.path.join(VAULT_DIR, "by-method", method)
    os.makedirs(method_dir, exist_ok=True)
    shutil.copy2(filepath, os.path.join(method_dir, filename))


def rebuild_index_from_files():
    """Rebuild index by scanning all recipe files."""
    index = {
        "generated": datetime.now().isoformat(),
        "total_recipes": 0,
        "cuisines": {},
        "types": {},
        "methods": {},
        "recipes": []
    }

    # Scan recipes directory
    recipe_files = []
    for f in os.listdir(RECIPES_DIR):
        if f.endswith(".md"):
            recipe_files.append(f)

    # Also check existing index for metadata
    existing_index = load_existing_index()
    existing_meta = {}
    for r in existing_index.get("recipes", []):
        existing_meta[r["file"]] = r

    for filename in sorted(recipe_files):
        filepath = os.path.join(RECIPES_DIR, filename)
        file_size = os.path.getsize(filepath)

        # Try to get metadata from existing index
        if filename in existing_meta:
            meta = existing_meta[filename]
            name = meta["name"]
            cuisines = meta.get("cuisines", [])
            types = meta.get("types", [])
            methods = meta.get("methods", [])
            url = meta.get("url", "")
            has_full = meta.get("has_full_content", file_size > 2000)
        else:
            # Parse from file content
            with open(filepath, "r") as f:
                content = f.read()

            # Extract name from first heading
            name_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            name = name_match.group(1).strip() if name_match else filename.replace(".md", "").replace("_", " ").title()

            # Extract source URL
            url_match = re.search(r"\[RecipeTin Eats\]\((.+?)\)", content)
            url = url_match.group(1) if url_match else ""

            # Extract metadata from the header
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

        # Update category counts
        for c in cuisines:
            index["cuisines"][c] = index["cuisines"].get(c, 0) + 1
        for t in types:
            index["types"][t] = index["types"].get(t, 0) + 1
        for m in methods:
            index["methods"][m] = index["methods"].get(m, 0) + 1

    index["total_recipes"] = len(index["recipes"])
    return index


def main():
    ensure_dirs()
    existing_index = load_existing_index()

    # Check which recipes already exist
    already_exists = []
    needs_adding = []

    for recipe in RECIPES:
        if recipe_exists(existing_index, recipe["name"]):
            # Check if file actually exists
            fname = safe_filename(recipe["slug"])
            if file_exists_in_recipes(fname):
                already_exists.append(recipe)
                continue
        needs_adding.append(recipe)

    print(f"Total recipes requested: {len(RECIPES)}")
    print(f"Already in vault (skipping): {len(already_exists)}")
    print(f"Need to add: {len(needs_adding)}")

    if needs_adding:
        print("\nMissing recipes:")
        for r in needs_adding:
            print(f"  - {r['name']}")

    return len(already_exists), len(needs_adding)


if __name__ == "__main__":
    main()
