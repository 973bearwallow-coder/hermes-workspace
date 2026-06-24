#!/bin/bash
# List all recipe files with sizes
echo "=== /recipes/ ==="
find /home/tom/hermes-workspace/projects/recipe-vault/recipes -name "*.md" -exec wc -c {} \; | sort -t/ -k10

echo ""
echo "=== /by-cuisine/ ==="
find /home/tom/hermes-workspace/projects/recipe-vault/by-cuisine -name "*.md" -exec wc -c {} \; | sort -t/ -k10

echo ""
echo "=== /by-type/ ==="
find /home/tom/hermes-workspace/projects/recipe-vault/by-type -name "*.md" -exec wc -c {} \; | sort -t/ -k10

echo ""
echo "=== /by-method/ ==="
find /home/tom/hermes-workspace/projects/recipe-vault/by-method -name "*.md" -exec wc -c {} \; | sort -t/ -k10
