#!/bin/bash
# Rebuild recipe vault subdirectories and index
# Run from the recipe-vault directory

cd "$(dirname "$0")"

VAULT_DIR="$(pwd)"
RECIPES_DIR="$VAULT_DIR/recipes"
BY_CUISINE_DIR="$VAULT_DIR/by-cuisine"
BY_TYPE_DIR="$VAULT_DIR/by-type"
BY_METHOD_DIR="$VAULT_DIR/by-method"

echo "=== Recipe Vault Rebuild ==="
echo ""

# Step 1: Clean subdirectories
echo "Step 1: Cleaning subdirectories..."
rm -rf "$BY_CUISINE_DIR"/* "$BY_TYPE_DIR"/* "$BY_METHOD_DIR"/*
echo "  Done."

# Step 2: For each .md file in recipes/, read its metadata and create symlinks
echo "Step 2: Creating symlinks for all recipes..."
count=0

for filepath in "$RECIPES_DIR"/*.md; do
    filename=$(basename "$filepath")
    
    # Extract metadata from the file
    cuisine=$(grep -m1 '^\*\*Cuisine:\*\*' "$filepath" | sed 's/\*\*Cuisine:\*\*\s*//')
    type=$(grep -m1 '^\*\*Type:\*\*' "$filepath" | sed 's/\*\*Type:\*\*\s*//')
    method=$(grep -m1 '^\*\*Method:\*\*' "$filepath" | sed 's/\*\*Method:\*\*\s*//')
    
    # Skip if no metadata
    if [ -z "$cuisine" ] && [ -z "$type" ] && [ -z "$method" ]; then
        echo "  SKIP (no metadata): $filename"
        continue
    fi
    
    # Create symlinks in by-cuisine
    if [ -n "$cuisine" ]; then
        IFS=',' read -ra CUISINES <<< "$cuisine"
        for c in "${CUISINES[@]}"; do
            c=$(echo "$c" | xargs)  # trim
            mkdir -p "$BY_CUISINE_DIR/$c"
            if [ ! -e "$BY_CUISINE_DIR/$c/$filename" ]; then
                ln -s "../recipes/$filename" "$BY_CUISINE_DIR/$c/$filename"
            fi
        done
    fi
    
    # Create symlinks in by-type
    if [ -n "$type" ]; then
        IFS=',' read -ra TYPES <<< "$type"
        for t in "${TYPES[@]}"; do
            t=$(echo "$t" | xargs)  # trim
            mkdir -p "$BY_TYPE_DIR/$t"
            if [ ! -e "$BY_TYPE_DIR/$t/$filename" ]; then
                ln -s "../recipes/$filename" "$BY_TYPE_DIR/$t/$filename"
            fi
        done
    fi
    
    # Create symlinks in by-method
    if [ -n "$method" ]; then
        IFS=',' read -ra METHODS <<< "$method"
        for m in "${METHODS[@]}"; do
            m=$(echo "$m" | xargs)  # trim
            mkdir -p "$BY_METHOD_DIR/$m"
            if [ ! -e "$BY_METHOD_DIR/$m/$filename" ]; then
                ln -s "../recipes/$filename" "$BY_METHOD_DIR/$m/$filename"
            fi
        done
    fi
    
    count=$((count + 1))
done

echo "  Processed $count recipe files."

# Step 3: Count results
echo ""
echo "Step 3: Counting results..."
echo "  by-cuisine entries: $(find "$BY_CUISINE_DIR" -type l | wc -l)"
echo "  by-type entries: $(find "$BY_TYPE_DIR" -type l | wc -l)"
echo "  by-method entries: $(find "$BY_METHOD_DIR" -type l | wc -l)"

echo ""
echo "=== Subdirectory rebuild complete ==="
echo ""
echo "NOTE: index.json rebuild requires Python - run rebuild_vault_final.py separately"
