#!/usr/bin/env python3
"""Create symlinks for by-cuisine, by-type, by-method directories."""

import os
import json

VAULT = os.path.expanduser('~/hermes-workspace/projects/recipe-vault')

with open(os.path.join(VAULT, 'index.json'), 'r') as f:
    index = json.load(f)

# Clear and recreate symlinks
import shutil
for category in ['by-cuisine', 'by-type', 'by-method']:
    path = os.path.join(VAULT, category)
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

# Create symlinks
for recipe in index['recipes']:
    source = os.path.join(VAULT, recipe['file'])
    if not os.path.exists(source):
        continue
    
    for cuisine in recipe['cuisines']:
        dest_dir = os.path.join(VAULT, 'by-cuisine', cuisine)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, os.path.basename(recipe['file']))
        if not os.path.exists(dest):
            os.symlink(source, dest)
    
    for rtype in recipe['types']:
        dest_dir = os.path.join(VAULT, 'by-type', rtype)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, os.path.basename(recipe['file']))
        if not os.path.exists(dest):
            os.symlink(source, dest)
    
    for method in recipe['methods']:
        dest_dir = os.path.join(VAULT, 'by-method', method)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, os.path.basename(recipe['file']))
        if not os.path.exists(dest):
            os.symlink(source, dest)

# Report
print("=== Vault Structure ===")
for category in ['by-cuisine', 'by-type', 'by-method']:
    base = os.path.join(VAULT, category)
    if os.path.exists(base):
        dirs = sorted(os.listdir(base))
        print(f"\n{category}:")
        for d in dirs:
            path = os.path.join(base, d)
            if os.path.isdir(path):
                count = len(os.listdir(path))
                print(f"  {d}: {count} recipes")

print(f"\nTotal recipes in vault: {index['total_recipes']}")
print(f"All have full content: {all(r['has_full_content'] for r in index['recipes'])}")
print(f"Vault location: {VAULT}")
