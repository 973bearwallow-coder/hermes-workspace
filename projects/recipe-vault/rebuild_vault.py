#!/usr/bin/env python3
"""Rebuild recipe vault: create by-cuisine, by-type, by-method subdirectories and rebuild index.json"""

import json
import os
import shutil
from collections import defaultdict

VAULT_DIR = os.path.dirname(os.path.abspath(__file__))
RECIPES_DIR = os.path.join(VAULT_DIR, "recipes")
INDEX_FILE = os.path.join(VAULT_DIR, "index.json")

# Load existing index
with open(INDEX_FILE, "r") as f:
    index = json.load(f)

# Create subdirectories
by_cuisine_dir = os.path.join(VAULT_DIR, "by-cuisine")
by_type_dir = os.path.join(VAULT_DIR, "by-type")
by_method_dir = os.path.join(VAULT_DIR, "by-method")

os.makedirs(by_cuisine_dir, exist_ok=True)
os.makedirs(by_type_dir, exist_ok=True)
os.makedirs(by_method_dir, exist_ok=True)

# Track counts
cuisine_counts = defaultdict(int)
type_counts = defaultdict(int)
method_counts = defaultdict(int)

# Process each recipe in the index
for recipe in index["recipes"]:
    src = os.path.join(RECIPES_DIR, recipe["file"])
    if not os.path.exists(src):
        print(f"WARNING: {recipe['file']} not found, skipping")
        continue

    # Copy to by-cuisine subdirectories
    for cuisine in recipe.get("cuisines", []):
        cuisine_dir = os.path.join(by_cuisine_dir, cuisine)
        os.makedirs(cuisine_dir, exist_ok=True)
        dst = os.path.join(cuisine_dir, recipe["file"])
        shutil.copy2(src, dst)
        cuisine_counts[cuisine] += 1

    # Copy to by-type subdirectories
    for rtype in recipe.get("types", []):
        type_dir = os.path.join(by_type_dir, rtype)
        os.makedirs(type_dir, exist_ok=True)
        dst = os.path.join(type_dir, recipe["file"])
        shutil.copy2(src, dst)
        type_counts[rtype] += 1

    # Copy to by-method subdirectories
    for method in recipe.get("methods", []):
        method_dir = os.path.join(by_method_dir, method)
        os.makedirs(method_dir, exist_ok=True)
        dst = os.path.join(method_dir, recipe["file"])
        shutil.copy2(src, dst)
        method_counts[method] += 1

# Rebuild index with updated counts
new_index = {
    "generated": "2026-06-19T23:00:00.000000",
    "total_recipes": index["total_recipes"],
    "cuisines": dict(sorted(cuisine_counts.items())),
    "types": dict(sorted(type_counts.items())),
    "methods": dict(sorted(method_counts.items())),
    "recipes": index["recipes"]
}

with open(INDEX_FILE, "w") as f:
    json.dump(new_index, f, indent=2)

print(f"Total recipes: {index['total_recipes']}")
print(f"Cuisines: {len(cuisine_counts)} - {dict(sorted(cuisine_counts.items()))}")
print(f"Types: {len(type_counts)} - {dict(sorted(type_counts.items()))}")
print(f"Methods: {len(method_counts)} - {dict(sorted(method_counts.items()))}")
print("Done!")

