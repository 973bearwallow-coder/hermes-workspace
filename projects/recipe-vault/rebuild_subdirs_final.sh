#!/bin/bash
# Rebuild by-cuisine, by-type, by-method subdirectories
# Run from recipe-vault directory
cd "$(dirname "$0")"

# Clean and recreate
for sub in by-cuisine by-type by-method; do
    rm -rf "$sub"
    mkdir -p "$sub"
done

# Parse each recipe file and copy to appropriate subdirs
for f in recipes/*.md; do
    base=$(basename "$f")
    # Extract metadata from headers
    cuisine=$(grep -m1 '^\*\*Cuisine:\*\*' "$f" | sed 's/\*\*Cuisine:\*\*\s*//' | tr -d '\n' | grep -v '^$' | head -1)
    type=$(grep -m1 '^\*\*Type:\*\*' "$f" | sed 's/\*\*Type:\*\*\s*//' | tr -d '\n' | grep -v '^$' | head -1)
    method=$(grep -m1 '^\*\*Method:\*\*' "$f" | sed 's/\*\*Method:\*\*\s*//' | tr -d '\n' | grep -v '^$' | head -1)
    
    # Fallbacks
    [ -z "$cuisine" ] && cuisine="unknown"
    [ -z "$type" ] && type="main"
    [ -z "$method" ] && method="stovetop"
    
    # Copy to each subdir
    mkdir -p "by-cuisine/$cuisine"
    cp "$f" "by-cuisine/$cuisine/$base"
    
    mkdir -p "by-type/$type"
    cp "$f" "by-type/$type/$base"
    
    mkdir -p "by-method/$method"
    cp "$f" "by-method/$method/$base"
done

echo "=== Subdirectory rebuild complete ==="
for sub in by-cuisine by-type by-method; do
    count=$(find "$sub" -name "*.md" | wc -l)
    echo "  $sub: $count files"
done
echo "Total recipes in vault: $(ls recipes/*.md | wc -l)"
