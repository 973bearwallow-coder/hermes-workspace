#!/usr/bin/env python3
"""Rebuild index.json from existing recipe files and old index metadata."""
import json
import os
import re
from datetime import datetime

VAULT_DIR = os.path.expanduser("~/hermes-workspace/projects/recipe-vault")
RECIPES_DIR = os.path.join(VAULT_DIR, "recipes")
INDEX_FILE = os.path.join(VAULT_DIR, "index.json")

# Load old index for metadata
with open(INDEX_FILE, "r") as f:
    old_index = json.load(f)

# Build lookup by filename
old_by_file = {}
for r in old_index.get("recipes", []):
    old_by_file[os.path.basename(r["file"])] = r

# Get all recipe files
all_files = sorted([f for f in os.listdir(RECIPES_DIR) if f.endswith(".md")])

new_index = {
    "generated": datetime.now().isoformat(),
    "total_recipes": 0,
    "cuisines": {},
    "types": {},
    "methods": {},
    "recipes": []
}

for fname in all_files:
    fpath = os.path.join(RECIPES_DIR, fname)
    fsize = os.path.getsize(fpath)

    # Try old index first
    if fname in old_by_file:
        old = old_by_file[fname]
        name = old["name"]
        url = old.get("url", "")
        has_full = old.get("has_full_content", fsize > 2000)
        # Clean up combined-category artifacts
        raw_cuisines = old.get("cuisines", [])
        raw_types = old.get("types", [])
        raw_methods = old.get("methods", [])
        
        # Extract real cuisines (filter out combined keys)
        cuisines = []
        for c in raw_cuisines:
            if " | " not in c and c not in ("stir-fry", "grilled", "baked", "roast", "skewers", "ribs", "appetizer"):
                cuisines.append(c)
        # If no cuisines found, try to parse from file
        if not cuisines:
            with open(fpath, "r") as f:
                content = f.read(500)
            cm = re.search(r"\*\*Cuisine:\*\*\s*(.+)", content)
            if cm and cm.group(1).strip().lower() not in ("", "n/a"):
                cuisines = [cm.group(1).strip().lower()]
        
        types = []
        for t in raw_types:
            if " | " not in t and t not in ("stir-fry", "grilled", "baked"):
                types.append(t)
        if not types:
            with open(fpath, "r") as f:
                content = f.read(500)
            tm = re.search(r"\*\*Type:\*\*\s*(.+)", content)
            if tm and tm.group(1).strip().lower() not in ("", "n/a"):
                types = [tm.group(1).strip().lower()]
        
        methods = []
        for m in raw_methods:
            if " | " not in m:
                methods.append(m)
        if not methods:
            with open(fpath, "r") as f:
                content = f.read(500)
            mm = re.search(r"\*\*Method:\*\*\s*(.+)", content)
            if mm and mm.group(1).strip().lower() not in ("", "n/a"):
                methods = [mm.group(1).strip().lower()]
    else:
        # Parse from file
        with open(fpath, "r") as f:
            content = f.read(500)
        nm = re.search(r"^# (.+)$", content, re.MULTILINE)
        name = nm.group(1).strip() if nm else fname.replace(".md", "").replace("_", " ").title()
        urlm = re.search(r"\[([^\]]*)\]\((https?://[^)]+)\)", content)
        url = urlm.group(2) if urlm else ""
        cm = re.search(r"\*\*Cuisine:\*\*\s*(.+)", content)
        cuisines = [cm.group(1).strip().lower()] if cm and cm.group(1).strip().lower() not in ("", "n/a") else []
        tm = re.search(r"\*\*Type:\*\*\s*(.+)", content)
        types = [tm.group(1).strip().lower()] if tm and tm.group(1).strip().lower() not in ("", "n/a") else []
        mm = re.search(r"\*\*Method:\*\*\s*(.+)", content)
        methods = [mm.group(1).strip().lower()] if mm and mm.group(1).strip().lower() not in ("", "n/a") else []
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
print(f"\nCuisines: {dict(sorted(new_index['cuisines'].items()))}")
print(f"Types: {dict(sorted(new_index['types'].items()))}")
print(f"Methods: {dict(sorted(new_index['methods'].items()))}")
