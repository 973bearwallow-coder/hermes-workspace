#!/bin/bash
# Rebuild recipe vault: clean stubs, create subdirectories, rebuild index

VAULT="/home/tom/hermes-workspace/projects/recipe-vault"
RECIPES="$VAULT/recipes"

# 1. Remove empty stub files
rm -f "$RECIPES/chicken_au_poivre_creamy_peppercorn_sauce.md"
rm -f "$RECIPES/chicken_au_poivre_sauce.md"
rm -f "$RECIPES/chicken_cacciatore.md"

# 2. Remove old subdirectory contents (if any)
rm -rf "$VAULT/by-cuisine/"*.md
rm -rf "$VAULT/by-type/"*.md
rm -rf "$VAULT/by-method/"*.md

# 3. Copy each recipe to appropriate subdirectories
for f in "$RECIPES"/*.md; do
  [ -f "$f" ] || continue
  fname=$(basename "$f")
  
  # Extract cuisine(s) - can be multiple
  cuisines=$(grep -m1 '^\*\*Cuisine:\*\*' "$f" | sed 's/\*\*Cuisine:\*\* //' | tr ',' '\n' | sed 's/^ *//;s/ *$//')
  # Extract type(s)
  types=$(grep -m1 '^\*\*Type:\*\*' "$f" | sed 's/\*\*Type:\*\* //' | tr ',' '\n' | sed 's/^ *//;s/ *$//')
  # Extract method(s)
  methods=$(grep -m1 '^\*\*Method:\*\*' "$f" | sed 's/\*\*Method:\*\* //' | tr ',' '\n' | sed 's/^ *//;s/ *$//')
  
  for c in $cuisines; do
    [ -n "$c" ] && cp "$f" "$VAULT/by-cuisine/${c}_${fname}"
  done
  for t in $types; do
    [ -n "$t" ] && cp "$f" "$VAULT/by-type/${t}_${fname}"
  done
  for m in $methods; do
    [ -n "$m" ] && cp "$f" "$VAULT/by-method/${m}_${fname}"
  done
done

echo "Subdirectory copies created."
echo "Recipe count: $(ls -1 "$RECIPES"/*.md | wc -l)"
echo "by-cuisine count: $(ls -1 "$VAULT/by-cuisine"/*.md 2>/dev/null | wc -l)"
echo "by-type count: $(ls -1 "$VAULT/by-type"/*.md 2>/dev/null | wc -l)"
echo "by-method count: $(ls -1 "$VAULT/by-method"/*.md 2>/dev/null | wc -l)"
