#!/usr/bin/env python3
"""Rebuild index.json from scratch by scanning all recipe files."""
import json
import os
import re
import glob
from datetime import datetime

VAULT_DIR = os.path.expanduser("~/hermes-workspace/projects/recipe-vault")
RECIPES_DIR = os.path.join(VAULT_DIR, "recipes")
INDEX_PATH = os.path.join(VAULT_DIR, "index.json")

def parse_recipe_file(filepath):
    """Parse a recipe markdown file and extract metadata."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    if not lines:
        return None
    
    name = None
    for line in lines:
        if line.startswith('# '):
            name = line[2:].strip()
            break
    
    if not name:
        return None
    
    cuisines = []
    types = []
    methods = []
    url = ""
    
    for line in lines:
        line_lower = line.lower()
        if '**cuisine:**' in line_lower:
            match = re.search(r'\*\*Cuisine:\*\*\s*(.+)', line)
            if match:
                val = match.group(1).strip()
                cuisines = [c.strip() for c in val.split(',') if c.strip()]
        elif '**type:**' in line_lower:
            match = re.search(r'\*\*Type:\*\*\s*(.+)', line)
            if match:
                val = match.group(1).strip()
                types = [t.strip() for t in val.split(',') if t.strip()]
        elif '**method:**' in line_lower:
            match = re.search(r'\*\*Method:\*\*\s*(.+)', line)
            if match:
                val = match.group(1).strip()
                methods = [m.strip() for m in val.split(',') if m.strip()]
        elif '**source:**' in line_lower:
            match = re.search(r'\[([^\]]*)\]\(([^)]+)\)', line)
            if match:
                url = match.group(2).strip()
    
    return {
        "name": name,
        "file": f"recipes/{os.path.basename(filepath)}",
        "cuisines": cuisines,
        "types": types,
        "methods": methods,
        "has_full_content": len(content) > 1000,
        "url": url,
        "size": len(content)
    }

def main():
    recipe_files = sorted(glob.glob(os.path.join(RECIPES_DIR, "*.md")))
    
    recipes = []
    for filepath in recipe_files:
        parsed = parse_recipe_file(filepath)
        if parsed:
            recipes.append(parsed)
    
    cuisine_counts = {}
    type_counts = {}
    method_counts = {}
    
    for r in recipes:
        for c in r["cuisines"]:
            cuisine_counts[c] = cuisine_counts.get(c, 0) + 1
        for t in r["types"]:
            type_counts[t] = type_counts.get(t, 0) + 1
        for m in r["methods"]:
            method_counts[m] = method_counts.get(m, 0) + 1
    
    cuisine_counts = dict(sorted(cuisine_counts.items(), key=lambda x: -x[1]))
    type_counts = dict(sorted(type_counts.items(), key=lambda x: -x[1]))
    method_counts = dict(sorted(method_counts.items(), key=lambda x: -x[1]))
    
    index = {
        "generated": datetime.now().isoformat(),
        "total_recipes": len(recipes),
        "cuisines": cuisine_counts,
        "types": type_counts,
        "methods": method_counts,
        "recipes": recipes
    }
    
    with open(INDEX_PATH, 'w') as f:
        json.dump(index, f, indent=2)
    
    print(f"Index rebuilt: {len(recipes)} recipes")
    print(f"Cuisines ({len(cuisine_counts)}): {dict(list(cuisine_counts.items())[:10])}")
    print(f"Types ({len(type_counts)}): {dict(list(type_counts.items())[:10])}")
    print(f"Methods ({len(method_counts)}): {dict(list(method_counts.items())[:10])}")
    
    # Check our 43 target recipes
    target_names = [
        "French Chicken au Poivre Sauce", "Thai Grilled Chicken (Gai Yang)",
        "Chicken Chasseur", "New Orleans Chicken Wings",
        "Chicken Cacciatore (Italian Chicken Stew)", "Chicken Francese",
        "Vietnamese Caramel Ginger Chicken", "Chicken Marsala",
        "One Pot Baked Greek Chicken Orzo Risoni", "Thai Red Curry Pot Roast Chicken",
        "Chicken in Creamy Mustard Sauce", "Chicken Shawarma (Middle Eastern)",
        "Coq au Vin", "Chicken Piccata", "Creamy Chicken Mushroom Fettucine",
        "Creamy Tuscan Chicken Pasta Bake", "Chicken Broccoli Stir Fry",
        "Thai Chicken Lettuce Cups (Larb Gai / Laab Gai)", "Chicken Pad Thai",
        "Chicken Chow Mein", "Thai Basil Chicken Stir Fry",
        "Chicken with Creamy Sun Dried Tomato Sauce", "Pad Kee Mao (Thai Drunken Noodles)",
        "Jambalaya Recipe", "Chicken Pasta Recipe", "Chinese Cashew Chicken",
        "Chicken Pot Pie", "Lemon Chicken Salad", "Mexican Chicken Avocado Salad",
        "Oven Baked Chicken and Rice Pilaf (Cranberry Walnut Apple)",
        "Vietnamese Coconut Caramel Chicken", "Thai Coconut Chicken",
        "Oven Baked Chicken Quesadillas", "Creamy Chicken and Bacon Pasta",
        "Chicken and Mushroom Risotto", "Mexican Shredded Chicken",
        "One Pot Chicken Enchilada Rice Casserole",
        "One Pot Creamy Parmesan Garlic Risotto with Lemon Pepper Chicken",
        "One Pot Greek Chicken Lemon Rice",
        "Jamaican Jerk Chicken Drumsticks with Caribbean Rice and Beans",
        "One Pan Spanish Chicken Chorizo Tomato Potatoes",
        "Crispy Shredded Chicken Noodle Stir Fry",
        "10 Classic Chinese Dishes + Homemade Teriyaki Sauce",
    ]
    
    existing_names = {r["name"] for r in recipes}
    found = [n for n in target_names if n in existing_names]
    missing = [n for n in target_names if n not in existing_names]
    
    print(f"\nTarget 43 check: {len(found)}/{len(target_names)} found")
    if missing:
        print(f"MISSING ({len(missing)}):")
        for n in missing:
            print(f"  - {n}")
    else:
        print("All 43 target recipes present!")

if __name__ == "__main__":
    main()
