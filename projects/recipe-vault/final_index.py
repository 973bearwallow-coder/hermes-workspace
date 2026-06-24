#!/usr/bin/env python3
"""Final index rebuild - includes all recipe files."""

import os
import json
from datetime import datetime
from collections import Counter

VAULT = os.path.expanduser('~/hermes-workspace/projects/recipe-vault')
RECIPES_DIR = os.path.join(VAULT, 'recipes')
INDEX_FILE = os.path.join(VAULT, 'index.json')

# Read existing index to get URL data for known recipes
with open(INDEX_FILE, 'r') as f:
    old_index = json.load(f)

# Build URL lookup from old index
url_lookup = {}
for r in old_index['recipes']:
    url_lookup[r['file'].split('/')[-1]] = r['url']

# Find all recipe files
recipe_files = []
for f in sorted(os.listdir(RECIPES_DIR)):
    if f.endswith('.md') and os.path.getsize(os.path.join(RECIPES_DIR, f)) > 500:
        recipe_files.append(f)

print(f"Found {len(recipe_files)} recipe files with content")

# Build recipe entries
recipes = []
for filename in recipe_files:
    filepath = os.path.join(RECIPES_DIR, filename)
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Extract name from first line
    first_line = content.strip().split('\n')[0]
    if first_line.startswith('# '):
        name = first_line[2:].strip()
    else:
        name = filename.replace('.md', '').replace('_', ' ').title()
    
    # Get URL from lookup or construct
    url = url_lookup.get(filename, f"https://www.melskitchencafe.com/")
    
    # Extract cuisine/type/method from content
    cuisines = []
    types = []
    methods = []
    
    content_lower = content.lower()
    
    # Simple classification based on content
    if 'greek' in content_lower or 'tzatziki' in content_lower:
        cuisines.append('greek')
    if 'mexican' in content_lower or 'elote' in content_lower or 'esquites' in content_lower:
        cuisines.append('mexican')
    if 'french' in content_lower:
        cuisines.append('french')
    if 'italian' in content_lower or 'alfredo' in content_lower or 'pasta' in content_lower:
        cuisines.append('italian')
    if 'thai' in content_lower:
        cuisines.append('thai')
    if 'vietnamese' in content_lower:
        cuisines.append('asian')
    if not cuisines:
        cuisines = ['american']
    
    # Type classification
    if 'salad' in content_lower:
        types.append('salad')
    if 'soup' in content_lower or 'stew' in content_lower:
        types.append('soup')
    if any(kw in content_lower for kw in ['cake', 'cheesecake', 'pie', 'brownie', 'bar', 'bliss', 'caramel', 'bark', 'cupcake', 'truffle', 'pudding', 'candy', 'fudge', 'cookie']):
        types.append('dessert')
    if any(kw in content_lower for kw in ['bread', 'biscuit', 'roll', 'bun', 'loaf', 'pull-apart', 'monkey bread', 'sweet roll', 'sticky bun']):
        types.append('bread')
    if any(kw in content_lower for kw in ['dip', 'caviar', 'shrapnel', 'spread', 'appetizer']):
        types.append('appetizer')
    if 'oatmeal' in content_lower or 'breakfast' in content_lower:
        types.append('breakfast')
    if 'popcorn' in content_lower:
        types.append('snack')
    if 'side' in content_lower or 'potato' in content_lower:
        types.append('side')
    if not types:
        types = ['main']
    
    # Method classification
    if 'grill' in content_lower:
        methods.append('grilled')
    if 'bake' in content_lower or 'oven' in content_lower:
        methods.append('baked')
    if 'slow cooker' in content_lower or 'crockpot' in content_lower:
        methods.append('slow-cooker')
    if 'stovetop' in content_lower or 'skillet' in content_lower:
        methods.append('stovetop')
    if 'overnight' in content_lower:
        methods.append('overnight')
    if 'no-cook' in content_lower or 'no cook' in content_lower:
        methods.append('no-cook')
    if 'instant pot' in content_lower:
        methods.append('instant-pot')
    if not methods:
        methods = ['stovetop']
    
    recipes.append({
        'name': name,
        'file': f'recipes/{filename}',
        'cuisines': cuisines,
        'types': types,
        'methods': methods,
        'has_full_content': True,
        'url': url
    })

# Count stats
cuisine_counts = {}
type_counts = {}
method_counts = []
for r in recipes:
    for c in r['cuisines']:
        cuisine_counts[c] = cuisine_counts.get(c, 0) + 1
    for t in r['types']:
        type_counts[t] = type_counts.get(t, 0) + 1
    for m in r['methods']:
        method_counts.append(m)

method_counts = dict(Counter(method_counts))

# Rebuild index
new_index = {
    'generated': datetime.now().isoformat(),
    'total_recipes': len(recipes),
    'cuisines': dict(sorted(cuisine_counts.items(), key=lambda x: -x[1])),
    'types': dict(sorted(type_counts.items(), key=lambda x: -x[1])),
    'methods': dict(sorted(method_counts.items(), key=lambda x: -x[1])),
    'recipes': recipes
}

with open(INDEX_FILE, 'w') as f:
    json.dump(new_index, f, indent=2)

print(f"\nIndex rebuilt: {len(recipes)} recipes")
print(f"Cuisines: {cuisine_counts}")
print(f"Types: {type_counts}")
print(f"Methods: {method_counts}")
