#!/usr/bin/env python3
"""Clean up index.json categories and rebuild counts."""
import json
import os
import re
from datetime import datetime

VAULT_DIR = os.path.expanduser("~/hermes-workspace/projects/recipe-vault")
INDEX_FILE = os.path.join(VAULT_DIR, "index.json")

with open(INDEX_FILE, "r") as f:
    old = json.load(f)

# Known non-cuisine values that ended up in cuisines arrays
NON_CUISINES = {
    "stir-fry", "grilled", "baked", "roast", "skewers", "ribs", "appetizer",
    "main | method: stovetop", "main | method: stir-fry", "main | method: baked",
    "grilled | method: grilled", "skewers | method: grilled",
}

NON_TYPES = {
    "stir-fry", "grilled", "baked", "roast", "skewers", "ribs",
}

new_index = {
    "generated": datetime.now().isoformat(),
    "total_recipes": 0,
    "cuisines": {},
    "types": {},
    "methods": {},
    "recipes": []
}

for entry in old["recipes"]:
    # Clean cuisines
    cuisines = []
    for c in entry.get("cuisines", []):
        if " | " in c:
            # Extract just the cuisine part
            parts = c.split(" | ")
            # Take the first part that's a real cuisine
            for p in parts:
                if p not in NON_CUISINES and p not in NON_TYPES:
                    cuisines.append(p)
                    break
            else:
                cuisines.append(parts[0])
        elif c not in NON_CUISINES and c not in NON_TYPES:
            cuisines.append(c)
    
    # Clean types
    types = []
    for t in entry.get("types", []):
        if " | " not in t and t not in NON_TYPES:
            types.append(t)
    
    # Clean methods
    methods = []
    for m in entry.get("methods", []):
        if " | " not in m:
            methods.append(m)
    
    new_entry = {
        "name": entry["name"],
        "file": entry["file"],
        "cuisines": cuisines,
        "types": types,
        "methods": methods,
        "has_full_content": entry.get("has_full_content", entry.get("size", 0) > 2000),
        "url": entry.get("url", ""),
        "size": entry.get("size", 0)
    }
    new_index["recipes"].append(new_entry)
    
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
print(f"\nCuisines: {dict(sorted(new_index['cuisines'].items()))}")
print(f"Types: {dict(sorted(new_index['types'].items()))}")
print(f"Methods: {dict(sorted(new_index['methods'].items()))}")
