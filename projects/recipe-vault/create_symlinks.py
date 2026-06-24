#!/usr/bin/env python3
"""Create symlinks for recipes in by-cuisine, by-type, and by-method directories."""

import os
import json

VAULT = os.path.expanduser('~/hermes-workspace/projects/recipe-vault')

# Read the rebuilt index
with open(os.path.join(VAULT, 'index.json'), 'r') as f:
    index = json.load(f)

# Create symlinks for each classification
for recipe in index['recipes']:
    file_path = recipe['file']  # e.g. "recipes/strawberry_spinach_salad.md"
    source = os.path.join(VAULT, file_path)
    
    if not os.path.exists(source):
        print(f"WARNING: Source not found: {source}")
        continue
    
    # By cuisine
    for cuisine in recipe['cuisines']:
        dest_dir = os.path.join(VAULT, 'by-cuisine', cuisine)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, os.path.basename(file_path))
        if not os.path.exists(dest):
            os.symlink(source, dest)
    
    # By type
    for rtype in recipe['types']:
        dest_dir = os.path.join(VAULT, 'by-type', rtype)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, os.path.basename(file_path))
        if not os.path.exists(dest):
            os.symlink(source, dest)
    
    # By method
    for method in recipe['methods']:
        dest_dir = os.path.join(VAULT, 'by-method', method)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, os.path.basename(file_path))
        if not os.path.exists(dest):
            os.symlink(source, dest)

# Count files in each directory
def count_symlinks(dir_path):
    if not os.path.exists(dir_path):
        return 0
    return len([f for f in os.listdir(dir_path) if os.path.islink(os.path.join(dir_path, f))])

print("\n=== By Cuisine ===")
for d in sorted(os.listdir(os.path.join(VAULT, 'by-cuisine'))):
    path = os.path.join(VAULT, 'by-cuisine', d)
    if os.path.isdir(path):
        count = count_symlinks(path)
        print(f"  {d}: {count} recipes")

print("\n=== By Type ===")
for d in sorted(os.listdir(os.path.join(VAULT, 'by-type'))):
    path = os.path.join(VAULT, 'by-type', d)
    if os.path.isdir(path):
        count = count_symlinks(path)
        print(f"  {d}: {count} recipes")

print("\n=== By Method ===")
for d in sorted(os.listdir(os.path.join(VAULT, 'by-method'))):
    path = os.path.join(VAULT, 'by-method', d)
    if os.path.isdir(path):
        count = count_symlinks(path)
        print(f"  {d}: {count} recipes")

print(f"\nTotal recipes in vault: {index['total_recipes']}")
print(f"All have full content: {all(r['has_full_content'] for r in index['recipes'])}")
