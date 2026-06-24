#!/bin/bash
# Copy all RecipeTin Eats recipes to by-cuisine, by-type, by-method subdirectories
VAULT=~/hermes-workspace/projects/recipe-vault
R=$VAULT/recipes

# Function to copy a file to multiple subdirs
copy_recipe() {
    local file=$1
    shift
    for dir in "$@"; do
        mkdir -p "$dir"
        cp "$R/$file" "$dir/$file"
    done
}

echo "Copying recipes to by-cuisine/..."
# French
mkdir -p "$VAULT/by-cuisine/french"
cp "$R/french_chicken_au_poivre_sauce.md" "$VAULT/by-cuisine/french/"
cp "$R/chicken_chasseur.md" "$VAULT/by-cuisine/french/"
cp "$R/chicken_in_creamy_mustard_sauce.md" "$VAULT/by-cuisine/french/"
cp "$R/coq_au_vin.md" "$VAULT/by-cuisine/french/"

# Thai
mkdir -p "$VAULT/by-cuisine/thai"
cp "$R/thai_grilled_chicken_gai_yang.md" "$VAULT/by-cuisine/thai/"
cp "$R/thai_red_curry_pot_roast_chicken.md" "$VAULT/by-cuisine/thai/"
cp "$R/thai_chicken_lettuce_cups_larb_gai.md" "$VAULT/by-cuisine/thai/"
cp "$R/chicken_pad_thai.md" "$VAULT/by-cuisine/thai/"
cp "$R/thai_basil_chicken_stir_fry.md" "$VAULT/by-cuisine/thai/"
cp "$R/pad_keemao_thai_drunken_noodles.md" "$VAULT/by-cuisine/thai/"
cp "$R/thai_coconut_chicken.md" "$VAULT/by-cuisine/thai/"

# Italian
mkdir -p "$VAULT/by-cuisine/italian"
cp "$R/chicken_cacciatore_italian_chicken_stew.md" "$VAULT/by-cuisine/italian/"
cp "$R/chicken_francese.md" "$VAULT/by-cuisine/italian/"
cp "$R/chicken_marsala.md" "$VAULT/by-cuisine/italian/"
cp "$R/chicken_piccata.md" "$VAULT/by-cuisine/italian/"
cp "$R/creamy_chicken_mushroom_fettucine.md" "$VAULT/by-cuisine/italian/"
cp "$R/creamy_tuscan_chicken_pasta_bake.md" "$VAULT/by-cuisine/italian/"
cp "$R/chicken_with_creamy_sun_dried_tomato_sauce.md" "$VAULT/by-cuisine/italian/"
cp "$R/chicken_pasta_recipe.md" "$VAULT/by-cuisine/italian/"
cp "$R/creamy_chicken_and_bacon_pasta.md" "$VAULT/by-cuisine/italian/"
cp "$R/chicken_and_mushroom_risotto.md" "$VAULT/by-cuisine/italian/"
cp "$R/one_pot_creamy_parmesan_garlic_risotto.md" "$VAULT/by-cuisine/italian/"

# American
mkdir -p "$VAULT/by-cuisine/american"
cp "$R/new_orleans_chicken_wings.md" "$VAULT/by-cuisine/american/"
cp "$R/jambalaya_recipe.md" "$VAULT/by-cuisine/american/"
cp "$R/chicken_pot_pie.md" "$VAULT/by-cuisine/american/"
cp "$R/lemon_chicken_salad.md" "$VAULT/by-cuisine/american/"
cp "$R/oven_baked_chicken_and_rice_pilaf.md" "$VAULT/by-cuisine/american/"

# Chinese
mkdir -p "$VAULT/by-cuisine/chinese"
cp "$R/chicken_broccoli_stir_fry.md" "$VAULT/by-cuisine/chinese/"
cp "$R/chicken_chow_mein.md" "$VAULT/by-cuisine/chinese/"
cp "$R/chinese_cashew_chicken.md" "$VAULT/by-cuisine/chinese/"
cp "$R/crispy_shredded_chicken_noodle_stir_fry.md" "$VAULT/by-cuisine/chinese/"
cp "$R/10_classic_chinese_dishes.md" "$VAULT/by-cuisine/chinese/"

# Vietnamese
mkdir -p "$VAULT/by-cuisine/vietnamese"
cp "$R/vietnamese_caramel_ginger_chicken.md" "$VAULT/by-cuisine/vietnamese/"
cp "$R/vietnamese_coconut_caramel_chicken.md" "$VAULT/by-cuisine/vietnamese/"

# Greek
mkdir -p "$VAULT/by-cuisine/greek"
cp "$R/one_pot_baked_greek_chicken_orzo_risoni.md" "$VAULT/by-cuisine/greek/"
cp "$R/one_pot_greek_chicken_lemon_rice.md" "$VAULT/by-cuisine/greek/"

# Mexican
mkdir -p "$VAULT/by-cuisine/mexican"
cp "$R/mexican_chicken_avocado_salad.md" "$VAULT/by-cuisine/mexican/"
cp "$R/oven_baked_chicken_quesadillas.md" "$VAULT/by-cuisine/mexican/"
cp "$R/mexican_shredded_chicken.md" "$VAULT/by-cuisine/mexican/"
cp "$R/one_pot_chicken_enchilada_rice_casserole.md" "$VAULT/by-cuisine/mexican/"

# Middle Eastern
mkdir -p "$VAULT/by-cuisine/middle-eastern"
cp "$R/chicken_shawarma_middle_eastern.md" "$VAULT/by-cuisine/middle-eastern/"

# Jamaican
mkdir -p "$VAULT/by-cuisine/jamaican"
cp "$R/jamaican_jerk_chicken_drumsticks.md" "$VAULT/by-cuisine/jamaican/"

# Spanish
mkdir -p "$VAULT/by-cuisine/spanish"
cp "$R/one_pan_spanish_chicken_chorizo.md" "$VAULT/by-cuisine/spanish/"

echo "Copying recipes to by-type/..."
# main
mkdir -p "$VAULT/by-type/main"
for f in french_chicken_au_poivre_sauce thai_grilled_chicken_gai_yang chicken_chasseur chicken_cacciatore_italian_chicken_stew chicken_francese vietnamese_caramel_ginger_chicken chicken_marsala one_pot_baked_greek_chicken_orzo_risoni thai_red_curry_pot_roast_chicken chicken_in_creamy_mustard_sauce chicken_shawarma_middle_eastern coq_au_vin chicken_piccata creamy_chicken_mushroom_fettucine creamy_tuscan_chicken_pasta_bake chicken_broccoli_stir_fry chicken_pad_thai chicken_chow_mein thai_basil_chicken_stir_fry chicken_with_creamy_sun_dried_tomato_sauce pad_keemao_thai_drunken_noodles jambalaya_recipe chicken_pasta_recipe chinese_cashew_chicken chicken_pot_pie oven_baked_chicken_and_rice_pilaf vietnamese_coconut_caramel_chicken thai_coconut_chicken oven_baked_chicken_quesadillas creamy_chicken_and_bacon_pasta chicken_and_mushroom_risotto mexican_shredded_chicken one_pot_chicken_enchilada_rice_casserole one_pot_creamy_parmesan_garlic_risotto one_pot_greek_chicken_lemon_rice jamaican_jerk_chicken_drumsticks one_pan_spanish_chicken_chorizo crispy_shredded_chicken_noodle_stir_fry 10_classic_chinese_dishes; do
    cp "$R/${f}.md" "$VAULT/by-type/main/" 2>/dev/null
done

# appetizer
mkdir -p "$VAULT/by-type/appetizer"
cp "$R/new_orleans_chicken_wings.md" "$VAULT/by-type/appetizer/"
cp "$R/thai_chicken_lettuce_cups_larb_gai.md" "$VAULT/by-type/appetizer/"

# salad
mkdir -p "$VAULT/by-type/salad"
cp "$R/lemon_chicken_salad.md" "$VAULT/by-type/salad/"
cp "$R/mexican_chicken_avocado_salad.md" "$VAULT/by-type/salad/"

echo "Copying recipes to by-method/..."
# stovetop
mkdir -p "$VAULT/by-method/stovetop"
for f in french_chicken_au_poivre_sauce chicken_chasseur chicken_cacciatore_italian_chicken_stew chicken_francese vietnamese_caramel_ginger_chicken chicken_marsala chicken_in_creamy_mustard_sauce chicken_shawarma_middle_eastern coq_au_vin chicken_piccata creamy_chicken_mushroom_fettucine chicken_with_creamy_sun_dried_tomato_sauce chicken_pasta_recipe creamy_chicken_and_bacon_pasta chicken_and_mushroom_risotto vietnamese_coconut_caramel_chicken thai_coconut_chicken mexican_shredded_chicken lemon_chicken_salad mexican_chicken_avocado_salad; do
    cp "$R/${f}.md" "$VAULT/by-method/stovetop/" 2>/dev/null
done

# grilled
mkdir -p "$VAULT/by-method/grilled"
cp "$R/thai_grilled_chicken_gai_yang.md" "$VAULT/by-method/grilled/"

# baked
mkdir -p "$VAULT/by-method/baked"
for f in new_orleans_chicken_wings creamy_tuscan_chicken_pasta_bake chicken_pot_pie oven_baked_chicken_and_rice_pilaf oven_baked_chicken_quesadillas jamaican_jerk_chicken_drumsticks; do
    cp "$R/${f}.md" "$VAULT/by-method/baked/" 2>/dev/null
done

# one-pot
mkdir -p "$VAULT/by-method/one-pot"
for f in one_pot_baked_greek_chicken_orzo_risoni thai_red_curry_pot_roast_chicken jambalaya_recipe one_pot_chicken_enchilada_rice_casserole one_pot_creamy_parmesan_garlic_risotto one_pot_greek_chicken_lemon_rice one_pan_spanish_chicken_chorizo; do
    cp "$R/${f}.md" "$VAULT/by-method/one-pot/" 2>/dev/null
done

# stir-fry
mkdir -p "$VAULT/by-method/stir-fry"
for f in chicken_broccoli_stir_fry thai_chicken_lettuce_cups_larb_gai chicken_pad_thai chicken_chow_mein thai_basil_chicken_stir_fry pad_keemao_thai_drunken_noodles chinese_cashew_chicken crispy_shredded_chicken_noodle_stir_fry 10_classic_chinese_dishes; do
    cp "$R/${f}.md" "$VAULT/by-method/stir-fry/" 2>/dev/null
done

echo "Done! All recipes copied to subdirectories."
