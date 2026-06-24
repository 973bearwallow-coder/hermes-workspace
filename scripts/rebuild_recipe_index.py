#!/usr/bin/env python3
"""Rebuild recipe vault index from actual files on disk."""
import json
import os
import re
from datetime import datetime
from pathlib import Path

VAULT_DIR = Path.home() / "hermes-workspace" / "projects" / "recipe-vault"
RECIPES_DIR = VAULT_DIR / "recipes"
INDEX_FILE = VAULT_DIR / "index.json"

def clean(val):
    """Strip markdown bold markers and extra whitespace."""
    return val.replace('**', '').strip().lower()

def classify_from_content(filepath):
    """Read a recipe file and extract its classifications from the header."""
    try:
        with open(filepath) as f:
            content = f.read(800)
    except:
        return [], [], []
    
    cuisines = []
    types = []
    methods = []
    
    for line in content.split('\n'):
        line = line.strip()
        if line.lower().startswith('**cuisine:**'):
            val = clean(line.split(':', 1)[1])
            cuisines = [c.strip() for c in re.split(r'[,/]', val) if c.strip() and not c.strip().startswith('**')]
        elif line.lower().startswith('**type:**'):
            val = clean(line.split(':', 1)[1])
            types = [t.strip() for t in re.split(r'[,/]', val) if t.strip() and not t.strip().startswith('**')]
        elif line.lower().startswith('**method:**'):
            val = clean(line.split(':', 1)[1])
            methods = [m.strip() for m in re.split(r'[,/]', val) if m.strip() and not m.strip().startswith('**')]
    
    return cuisines, types, methods

def main():
    entries = []
    cuisines_count = {}
    types_count = {}
    methods_count = {}
    
    for filename in sorted(os.listdir(RECIPES_DIR)):
        if not filename.endswith('.md'):
            continue
        
        filepath = RECIPES_DIR / filename
        rel_path = f"recipes/{filename}"
        
        try:
            with open(filepath) as f:
                first_line = f.readline().strip()
                name = first_line.lstrip('#').strip()
        except:
            name = filename.replace('.md', '').replace('_', ' ').title()
        
        url = ""
        try:
            with open(filepath) as f:
                for line in f:
                    if '**Source:**' in line or '**source:**' in line:
                        url = line.split('](')[-1].rstrip(')').strip()
                        break
        except:
            pass
        
        cuisines, types, methods = classify_from_content(filepath)
        size = os.path.getsize(filepath)
        has_full = size > 2000
        
        entry = {
            "name": name,
            "file": rel_path,
            "cuisines": cuisines,
            "types": types,
            "methods": methods,
            "has_full_content": has_full,
            "url": url,
            "size": size,
        }
        entries.append(entry)
        
        for c in cuisines:
            cuisines_count[c] = cuisines_count.get(c, 0) + 1
        for t in types:
            types_count[t] = types_count.get(t, 0) + 1
        for m in methods:
            methods_count[m] = methods_count.get(m, 0) + 1
    
    index = {
        "generated": datetime.now().isoformat(),
        "total_recipes": len(entries),
        "cuisines": dict(sorted(cuisines_count.items(), key=lambda x: -x[1])),
        "types": dict(sorted(types_count.items(), key=lambda x: -x[1])),
        "methods": dict(sorted(methods_count.items(), key=lambda x: -x[1])),
        "recipes": entries,
    }
    
    INDEX_FILE.write_text(json.dumps(index, indent=2))
    
    full_count = sum(1 for e in entries if e["has_full_content"])
    print(f"✅ Index rebuilt: {len(entries)} recipes")
    print(f"   Full content: {full_count}")
    print(f"   Title only: {len(entries) - full_count}")
    print(f"\n   Cuisines: {json.dumps(cuisines_count, indent=2)}")
    print(f"   Types: {json.dumps(types_count, indent=2)}")
    print(f"   Methods: {json.dumps(methods_count, indent=2)}")

if __name__ == "__main__":
    main()
