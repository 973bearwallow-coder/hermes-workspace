#!/bin/bash
# Script to rebuild all RecipeTin Eats recipe files and index
cd ~/hermes-workspace/projects/recipe-vault

# Remove old symlinks
find by-cuisine by-type by-method -type l -delete 2>/dev/null

# Run the Python build script
python3 << 'PYEOF'
import json, os, re
from datetime import datetime
from pathlib import Path

VAULT = Path.home() / "hermes-workspace/projects/recipe-vault"
RECIPES_DIR = VAULT / "recipes"

for subdir in ["by-cuisine", "by-type", "by-method"]:
    (VAULT / subdir).mkdir(exist_ok=True)

def sf(name):
    name = name.lower()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"\s+", "_", name.strip())
    name = re.sub(r"_+", "_", name)
    return name[:60].strip("_")

recipe_data = [
  # (name, url, cuisine, type, method, prep, cook, total, yield, description, ingredients, instructions, tips, nutrition)
]

print("Build script loaded. Recipe data will be injected by the build process.")
PYEOF
