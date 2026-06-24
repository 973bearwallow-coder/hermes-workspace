#!/usr/bin/env python3
"""
Build the recipe vault: write markdown files for all RecipeTin Eats recipes,
create symlinks in by-cuisine/, by-type/, by-method/ subdirectories,
and rebuild index.json.
"""
import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

VAULT = Path.home() / "hermes-workspace/projects/recipe-vault"
RECIPES_DIR = VAULT / "recipes"

for subdir in ["by-cuisine", "by-type", "by-method"]:
    (VAULT / subdir).mkdir(exist_ok=True)

def safe_filename(name, max_len=60):
    name = name.lower()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"\s+", "_", name.strip())
    name = re.sub(r"_+", "_", name)
    return name[:max_len].strip("_")


def write_recipe(recipe):
    """Write a single recipe markdown file."""
    fname = safe_filename(recipe["name"]) + ".md"
    fpath = RECIPES_DIR / fname

    lines = []
    lines.append(f"# {recipe['name']}")
    lines.append(f"**Source:** [RecipeTin Eats]({recipe['url']})")
    lines.append(f"**Cuisine:** {recipe['cuisine']}")
    lines.append(f"**Type:** {recipe['type']}")
    lines.append(f"**Method:** {recipe['method']}")
    if recipe.get('prep'): lines.append(f"**Prep Time:** {recipe['prep']}")
    if recipe.get('cook'): lines.append(f"**Cook Time:** {recipe['cook']}")
    if recipe.get('total'): lines.append(f"**Total Time:** {recipe['total']}")
    if recipe.get('yield'): lines.append(f"**Yield:** {recipe['yield']}")
    lines.append("")
    lines.append("## Description")
    lines.append(recipe.get('description', ''))
    lines.append("")
    lines.append("## Ingredients")
    for ing in recipe.get('ingredients', []):
        lines.append(f"- {ing}")
    lines.append("")
    lines.append("## Instructions")
    for i, step in enumerate(recipe.get('instructions', []), 1):
        lines.append(f"{i}. {step}")
    lines.append("")
    if recipe.get('tips'):
        lines.append("## Tips & Notes")
        for tip in recipe['tips']:
            lines.append(f"- {tip}")
        lines.append("")
    if recipe.get('nutrition'):
        lines.append("## Nutrition")
        lines.append(recipe['nutrition'])
        lines.append("")

    content = "\n".join(lines)
    fpath.write_text(content)
    return fname


def create_symlinks(fname, recipe):
    """Create symlinks in by-cuisine/, by-type/, by-method/."""
    # Clean old symlinks for this file
    for subdir in ["by-cuisine", "by-type", "by-method"]:
        target_dir = VAULT / subdir
        for existing in target_dir.iterdir():
            if existing.is_symlink() and existing.name.startswith(Path(fname).stem):
                existing.unlink()

    # by-cuisine
    cuisine_dir = VAULT / "by-cuisine" / recipe["cuisine"]
    cuisine_dir.mkdir(exist_ok=True)
    link = cuisine_dir / fname
    if not link.exists():
        link.symlink_to("../../recipes/" + fname)

    # by-type
    type_dir = VAULT / "by-type" / recipe["type"]
    type_dir.mkdir(exist_ok=True)
    link = type_dir / fname
    if not link.exists():
        link.symlink_to("../../recipes/" + fname)

    # by-method
    method_dir = VAULT / "by-method" / recipe["method"]
    method_dir.mkdir(exist_ok=True)
    link = method_dir / fname
    if not link.exists():
        link.symlink_to("../../recipes/" + fname)


def rebuild_index(recipe_entries):
    """Rebuild index.json with all recipes."""
    cuisines = {}
    types = {}
    methods = {}
    recipes_list = []

    for entry in recipe_entries:
        for c in entry.get("cuisines", [entry.get("cuisine", "unknown")]):
            cuisines[c] = cuisines.get(c, 0) + 1
        for t in entry.get("types", [entry.get("type", "unknown")]):
            types[t] = types.get(t, 0) + 1
        for m in entry.get("methods", [entry.get("method", "unknown")]):
            methods[m] = methods.get(m, 0) + 1

        fpath = RECIPES_DIR / entry["file"]
        size = fpath.stat().st_size if fpath.exists() else 0
        recipes_list.append({
            "name": entry["name"],
            "file": "recipes/" + entry["file"],
            "cuisines": entry.get("cuisines", [entry.get("cuisine", "unknown")]),
            "types": entry.get("types", [entry.get("type", "unknown")]),
            "methods": entry.get("methods", [entry.get("method", "unknown")]),
            "has_full_content": entry.get("has_full_content", True),
            "url": entry.get("url", ""),
            "size": size,
        })

    index = {
        "generated": datetime.now().isoformat(),
        "total_recipes": len(recipes_list),
        "cuisines": dict(sorted(cuisines.items())),
        "types": dict(sorted(types.items())),
        "methods": dict(sorted(methods.items())),
        "recipes": recipes_list,
    }

    index_path = VAULT / "index.json"
    index_path.write_text(json.dumps(index, indent=2))
    return index
