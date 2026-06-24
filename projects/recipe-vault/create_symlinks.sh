#!/bin/bash
# Run this script to create symlinks in by-cuisine/, by-type/, by-method/ directories
# Usage: bash create_symlinks.sh

VAULT_DIR="$HOME/hermes-workspace/projects/recipe-vault"
RECIPES_DIR="$VAULT_DIR/recipes"

# Clean existing symlinks
for sub in "by-cuisine" "by-type" "by-method"; do
    sub_path="$VAULT_DIR/$sub"
    if [ -d "$sub_path" ]; then
        find "$sub_path" -type l -delete
    fi
done

# Function to create symlinks for a recipe
create_symlinks() {
    local filename="$1"
    local recipe_path="$RECIPES_DIR/$filename"
    
    if [ ! -f "$recipe_path" ]; then
        echo "  WARNING: $filename not found, skipping"
        return
    fi
    
    # Parse cuisines, types, methods from the file
    local cuisines=$(grep '^\*\*Cuisine:\*\*' "$recipe_path" | head -1 | sed 's/\*\*Cuisine:\*\*//;s/^ //')
    local types=$(grep '^\*\*Type:\*\*' "$recipe_path" | head -1 | sed 's/\*\*Type:\*\*//;s/^ //')
    local methods=$(grep '^\*\*Method:\*\*' "$recipe_path" | head -1 | sed 's/\*\*Method:\*\*//;s/^ //')
    
    # Create cuisine symlinks
    IFS=',' read -ra CUISINE_ARR <<< "$cuisines"
    for c in "${CUISINE_ARR[@]}"; do
        c=$(echo "$c" | tr -d '[:space:]')
        [ -z "$c" ] && continue
        mkdir -p "$VAULT_DIR/by-cuisine/$c"
        ln -sf "$(realpath --relative-to="$VAULT_DIR/by-cuisine/$c" "$recipe_path")" "$VAULT_DIR/by-cuisine/$c/$filename"
    done
    
    # Create type symlinks
    IFS=',' read -ra TYPE_ARR <<< "$types"
    for t in "${TYPE_ARR[@]}"; do
        t=$(echo "$t" | tr -d '[:space:]')
        [ -z "$t" ] && continue
        mkdir -p "$VAULT_DIR/by-type/$t"
        ln -sf "$(realpath --relative-to="$VAULT_DIR/by-type/$t" "$recipe_path")" "$VAULT_DIR/by-type/$t/$filename"
    done
    
    # Create method symlinks
    IFS=',' read -ra METHOD_ARR <<< "$methods"
    for m in "${METHOD_ARR[@]}"; do
        m=$(echo "$m" | tr -d '[:space:]')
        [ -z "$m" ] && continue
        mkdir -p "$VAULT_DIR/by-method/$m"
        ln -sf "$(realpath --relative-to="$VAULT_DIR/by-method/$m" "$recipe_path")" "$VAULT_DIR/by-method/$m/$filename"
    done
}

echo "Creating symlinks for all recipes..."

# RecipeTin Eats recipes
create_symlinks "french_chicken_au_poivre_sauce.md"
create_symlinks "thai_grilled_chicken_gai_yang.md"
create_symlinks "chicken_chasseur.md"
create_symlinks "new_orleans_chicken_wings.md"
create_symlinks "chicken_cacciatore_italian_chicken_stew.md"
create_symlinks "chicken_francese.md"
create_symlinks "vietnamese_caramel_ginger_chicken.md"
create_symlinks "chicken_marsala.md"
create_symlinks "one_pot_baked_greek_chicken_orzo_risoni.md"
create_symlinks "thai_red_curry_pot_roast_chicken.md"
create_symlinks "chicken_in_creamy_mustard_sauce.md"
create_symlinks "chicken_shawarma_middle_eastern.md"
create_symlinks "coq_au_vin.md"
create_symlinks "chicken_piccata.md"
create_symlinks "creamy_chicken_mushroom_fettucine.md"
create_symlinks "creamy_tuscan_chicken_pasta_bake.md"
create_symlinks "chicken_broccoli_stir_fry.md"
create_symlinks "thai_chicken_lettuce_cups_larb_gai.md"
create_symlinks "chicken_pad_thai.md"
create_symlinks "chicken_chow_mein.md"
create_symlinks "thai_basil_chicken_stir_fry.md"
create_symlinks "chicken_with_creamy_sun_dried_tomato_sauce.md"
create_symlinks "pad_keemao_thai_drunken_noodles.md"
create_symlinks "jambalaya_recipe.md"
create_symlinks "chicken_pasta_recipe.md"
create_symlinks "chinese_cashew_chicken.md"
create_symlinks "chicken_pot_pie.md"
create_symlinks "lemon_chicken_salad.md"
create_symlinks "mexican_chicken_avocado_salad.md"
create_symlinks "oven_baked_chicken_and_rice_pilaf.md"
create_symlinks "vietnamese_coconut_caramel_chicken.md"
create_symlinks "thai_coconut_chicken.md"
create_symlinks "oven_baked_chicken_quesadillas.md"
create_symlinks "creamy_chicken_and_bacon_pasta.md"
create_symlinks "chicken_and_mushroom_risotto.md"
create_symlinks "mexican_shredded_chicken.md"
create_symlinks "one_pot_chicken_enchilada_rice_casserole.md"
create_symlinks "one_pot_creamy_parmesan_garlic_risotto.md"
create_symlinks "one_pot_greek_chicken_lemon_rice.md"
create_symlinks "jamaican_jerk_chicken_drumsticks.md"
create_symlinks "one_pan_spanish_chicken_chorizo.md"
create_symlinks "crispy_shredded_chicken_noodle_stir_fry.md"
create_symlinks "10_classic_chinese_dishes.md"

# Mel's Kitchen Cafe recipes
for f in "$RECIPES_DIR"/*.md; do
    fname=$(basename "$f")
    # Skip if already processed (RecipeTin Eats)
    case "$fname" in
        french_chicken_au_poivre_sauce|thai_grilled_chicken_gai_yang|chicken_chasseur|new_orleans_chicken_wings|chicken_cacciatore_italian_chicken_stew|chicken_francese|vietnamese_caramel_ginger_chicken|chicken_marsala|one_pot_baked_greek_chicken_orzo_risoni|thai_red_curry_pot_roast_chicken|chicken_in_creamy_mustard_sauce|chicken_shawarma_middle_eastern|coq_au_vin|chicken_piccata|creamy_chicken_mushroom_fettucine|creamy_tuscan_chicken_pasta_bake|chicken_broccoli_stir_fry|thai_chicken_lettuce_cups_larb_gai|chicken_pad_thai|chicken_chow_mein|thai_basil_chicken_stir_fry|chicken_with_creamy_sun_dried_tomato_sauce|pad_keemao_thai_drunken_noodles|jambalaya_recipe|chicken_pasta_recipe|chinese_cashew_chicken|chicken_pot_pie|lemon_chicken_salad|mexican_chicken_avocado_salad|oven_baked_chicken_and_rice_pilaf|vietnamese_coconut_caramel_chicken|thai_coconut_chicken|oven_baked_chicken_quesadillas|creamy_chicken_and_bacon_pasta|chicken_and_mushroom_risotto|mexican_shredded_chicken|one_pot_chicken_enchilada_rice_casserole|one_pot_creamy_parmesan_garlic_risotto|one_pot_greek_chicken_lemon_rice|jamaican_jerk_chicken_drumsticks|one_pan_spanish_chicken_chorizo|crispy_shredded_chicken_noodle_stir_fry|10_classic_chinese_dishes) continue ;;
    esac
    create_symlinks "$fname"
done

echo "Done! Counting symlinks..."
find "$VAULT_DIR/by-cuisine" "$VAULT_DIR/by-type" "$VAULT_DIR/by-method" -type l | wc -l
