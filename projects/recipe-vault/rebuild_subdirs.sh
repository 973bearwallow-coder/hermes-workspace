#!/bin/bash
# Rebuild by-cuisine, by-type, by-method subdirectories for the recipe vault
# Run this from the recipe-vault directory: cd ~/hermes-workspace/projects/recipe-vault && bash rebuild_subdirs.sh

VAULT="$(cd "$(dirname "$0")" && pwd)"
RECIPES="$VAULT/recipes"

# Clean and recreate subdirs
for sub in by-cuisine by-type by-method; do
    rm -rf "$VAULT/$sub"
    mkdir -p "$VAULT/$sub"
done

# Function to copy a recipe to all three subdirs
copy_recipe() {
    local file="$1" cuisine="$2" type="$3" method="$4"
    local basename=$(basename "$file")
    
    mkdir -p "$VAULT/by-cuisine/$cuisine"
    cp "$RECIPES/$basename" "$VAULT/by-cuisine/$cuisine/$basename"
    
    mkdir -p "$VAULT/by-type/$type"
    cp "$RECIPES/$basename" "$VAULT/by-type/$type/$basename"
    
    mkdir -p "$VAULT/by-method/$method"
    cp "$RECIPES/$basename" "$VAULT/by-method/$method/$basename"
}

# === All 43 new RecipeTin Eats recipes ===
copy_recipe "french_chicken_au_poivre_sauce.md" "french" "main" "stovetop"
copy_recipe "thai_grilled_chicken_gai_yang.md" "thai" "main" "grilled"
copy_recipe "chicken_chasseur.md" "french" "main" "stovetop"
copy_recipe "new_orleans_chicken_wings.md" "american" "appetizer" "baked"
copy_recipe "chicken_cacciatore.md" "italian" "main" "stovetop"
copy_recipe "chicken_francese.md" "italian" "main" "stovetop"
copy_recipe "vietnamese_caramel_ginger_chicken.md" "vietnamese" "main" "stovetop"
copy_recipe "chicken_marsala.md" "italian" "main" "stovetop"
copy_recipe "one_pot_baked_greek_chicken_orzo_risoni.md" "greek" "main" "one-pot"
copy_recipe "thai_red_curry_pot_roast_chicken.md" "thai" "main" "baked"
copy_recipe "chicken_in_creamy_mustard_sauce.md" "french" "main" "stovetop"
copy_recipe "chicken_shawarma_middle_eastern.md" "middle-eastern" "main" "stovetop"
copy_recipe "coq_au_vin.md" "french" "main" "stovetop"
copy_recipe "chicken_piccata.md" "italian" "main" "stovetop"
copy_recipe "creamy_chicken_mushroom_fettucine.md" "italian" "main" "stovetop"
copy_recipe "creamy_tuscan_chicken_pasta_bake.md" "italian" "main" "baked"
copy_recipe "chicken_broccoli_stir_fry.md" "chinese" "main" "stir-fry"
copy_recipe "thai_chicken_lettuce_cups_larb_gai.md" "thai" "appetizer" "stovetop"
copy_recipe "chicken_pad_thai.md" "thai" "main" "stir-fry"
copy_recipe "chicken_chow_mein.md" "chinese" "main" "stir-fry"
copy_recipe "thai_basil_chicken_stir_fry.md" "thai" "main" "stir-fry"
copy_recipe "chicken_with_creamy_sun_dried_tomato_sauce.md" "italian" "main" "stovetop"
copy_recipe "pad_keemao_thai_drunken_noodles.md" "thai" "main" "stir-fry"
copy_recipe "jambalaya_recipe.md" "american" "main" "one-pot"
copy_recipe "chicken_pasta_recipe.md" "italian" "main" "stovetop"
copy_recipe "chinese_cashew_chicken.md" "chinese" "main" "stir-fry"
copy_recipe "chicken_pot_pie.md" "american" "main" "baked"
copy_recipe "lemon_chicken_salad.md" "american" "salad" "stovetop"
copy_recipe "mexican_chicken_avocado_salad.md" "mexican" "salad" "grilled"
copy_recipe "oven_baked_chicken_and_rice_pilaf.md" "american" "main" "baked"
copy_recipe "vietnamese_coconut_caramel_chicken.md" "vietnamese" "main" "stovetop"
copy_recipe "thai_coconut_chicken.md" "thai" "main" "grilled"
copy_recipe "oven_baked_chicken_quesadillas.md" "mexican" "main" "baked"
copy_recipe "creamy_chicken_and_bacon_pasta.md" "italian" "main" "stovetop"
copy_recipe "chicken_and_mushroom_risotto.md" "italian" "main" "stovetop"
copy_recipe "mexican_shredded_chicken.md" "mexican" "main" "slow-cooker"
copy_recipe "one_pot_chicken_enchilada_rice_casserole.md" "mexican" "main" "one-pot"
copy_recipe "one_pot_creamy_parmesan_garlic_risotto.md" "italian" "main" "one-pot"
copy_recipe "one_pot_greek_chicken_lemon_rice.md" "greek" "main" "one-pot"
copy_recipe "jamaican_jerk_chicken_drumsticks.md" "jamaican" "main" "baked"
copy_recipe "one_pan_spanish_chicken_chorizo.md" "spanish" "main" "baked"
copy_recipe "crispy_shredded_chicken_noodle_stir_fry.md" "chinese" "main" "stir-fry"
copy_recipe "10_classic_chinese_dishes.md" "chinese" "main" "stir-fry"

# === Copy remaining vault recipes by parsing their headers ===
for f in "$RECIPES"/*.md; do
    base=$(basename "$f")
    # Skip if already copied (one of our 43)
    case "$base" in
        french_chicken_au_poivre_sauce.md|thai_grilled_chicken_gai_yang.md|chicken_chasseur.md|new_orleans_chicken_wings.md|chicken_cacciatore.md|chicken_francese.md|vietnamese_caramel_ginger_chicken.md|chicken_marsala.md|one_pot_baked_greek_chicken_orzo_risoni.md|thai_red_curry_pot_roast_chicken.md|chicken_in_creamy_mustard_sauce.md|chicken_shawarma_middle_eastern.md|coq_au_vin.md|chicken_piccata.md|creamy_chicken_mushroom_fettucine.md|creamy_tuscan_chicken_pasta_bake.md|chicken_broccoli_stir_fry.md|thai_chicken_lettuce_cups_larb_gai.md|chicken_pad_thai.md|chicken_chow_mein.md|thai_basil_chicken_stir_fry.md|chicken_with_creamy_sun_dried_tomato_sauce.md|pad_keemao_thai_drunken_noodles.md|jambalaya_recipe.md|chicken_pasta_recipe.md|chinese_cashew_chicken.md|chicken_pot_pie.md|lemon_chicken_salad.md|mexican_chicken_avocado_salad.md|oven_baked_chicken_and_rice_pilaf.md|vietnamese_coconut_caramel_chicken.md|thai_coconut_chicken.md|oven_baked_chicken_quesadillas.md|creamy_chicken_and_bacon_pasta.md|chicken_and_mushroom_risotto.md|mexican_shredded_chicken.md|one_pot_chicken_enchilada_rice_casserole.md|one_pot_creamy_parmesan_garlic_risotto.md|one_pot_greek_chicken_lemon_rice.md|jamaican_jerk_chicken_drumsticks.md|one_pan_spanish_chicken_chorizo.md|crispy_shredded_chicken_noodle_stir_fry.md|10_classic_chinese_dishes.md)
            continue ;;
    esac
    
    # Parse cuisine/type/method from file header
    cuisine=$(grep -m1 '^\*\*Cuisine:\*\*' "$f" | sed 's/\*\*Cuisine:\*\*\s*//' | grep -v '^$' | head -1)
    type=$(grep -m1 '^\*\*Type:\*\*' "$f" | sed 's/\*\*Type:\*\*\s*//' | grep -v '^$' | head -1)
    method=$(grep -m1 '^\*\*Method:\*\*' "$f" | sed 's/\*\*Method:\*\*\s*//' | grep -v '^$' | head -1)
    
    # Fallback values
    [ -z "$cuisine" ] && cuisine="unknown"
    [ -z "$type" ] && type="main"
    [ -z "$method" ] && method="stovetop"
    
    mkdir -p "$VAULT/by-cuisine/$cuisine"
    cp "$f" "$VAULT/by-cuisine/$cuisine/$base"
    
    mkdir -p "$VAULT/by-type/$type"
    cp "$f" "$VAULT/by-type/$type/$base"
    
    mkdir -p "$VAULT/by-method/$method"
    cp "$f" "$VAULT/by-method/$method/$base"
done

# Count files
echo "=== Subdirectory rebuild complete ==="
for sub in by-cuisine by-type by-method; do
    count=$(find "$VAULT/$sub" -name "*.md" | wc -l)
    echo "  $sub: $count files"
done
echo "Total recipes in vault: $(ls "$RECIPES"/*.md | wc -l)"
