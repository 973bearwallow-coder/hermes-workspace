#!/bin/bash
# Create subdirectories and copy recipe files
VAULT="/home/tom/hermes-workspace/projects/recipe-vault"
RECIPES="$VAULT/recipes"

# Create subdirectories
mkdir -p "$VAULT/by-cuisine"
mkdir -p "$VAULT/by-type"
mkdir -p "$VAULT/by-method"

# Cuisines
for cuisine in french thai italian american mexican chinese jamaican spanish middle-eastern vietnamese greek; do
    mkdir -p "$VAULT/by-cuisine/$cuisine"
done

# Types
for type in main salad appetizer soup bread dessert breakfast snack side; do
    mkdir -p "$VAULT/by-type/$type"
done

# Methods
for method in grilled baked stovetop one-pot stir-fry slow-cooker fried no-cook overnight sheet-pan instant-pot roast blend; do
    mkdir -p "$VAULT/by-method/$method"
done

# Copy files to by-cuisine
cp "$RECIPES/french_chicken_au_poivre_sauce.md" "$VAULT/by-cuisine/french/"
cp "$RECIPES/chicken_chasseur.md" "$VAULT/by-cuisine/french/"
cp "$RECIPES/chicken_in_creamy_mustard_sauce.md" "$VAULT/by-cuisine/french/"
cp "$RECIPES/coq_au_vin.md" "$VAULT/by-cuisine/french/"

cp "$RECIPES/thai_grilled_chicken_gai_yang.md" "$VAULT/by-cuisine/thai/"
cp "$RECIPES/thai_red_curry_pot_roast_chicken.md" "$VAULT/by-cuisine/thai/"
cp "$RECIPES/thai_chicken_lettuce_cups_larb_gai.md" "$VAULT/by-cuisine/thai/"
cp "$RECIPES/chicken_pad_thai.md" "$VAULT/by-cuisine/thai/"
cp "$RECIPES/thai_basil_chicken_stir_fry.md" "$VAULT/by-cuisine/thai/"
cp "$RECIPES/pad_keemao_thai_drunken_noodles.md" "$VAULT/by-cuisine/thai/"
cp "$RECIPES/thai_coconut_chicken.md" "$VAULT/by-cuisine/thai/"

cp "$RECIPES/chicken_cacciatore.md" "$VAULT/by-cuisine/italian/"
cp "$RECIPES/chicken_francese.md" "$VAULT/by-cuisine/italian/"
cp "$RECIPES/chicken_marsala.md" "$VAULT/by-cuisine/italian/"
cp "$RECIPES/chicken_piccata.md" "$VAULT/by-cuisine/italian/"
cp "$RECIPES/creamy_chicken_mushroom_fettucine.md" "$VAULT/by-cuisine/italian/"
cp "$RECIPES/creamy_tuscan_chicken_pasta_bake.md" "$VAULT/by-cuisine/italian/"
cp "$RECIPES/chicken_pasta_recipe.md" "$VAULT/by-cuisine/italian/"
cp "$RECIPES/creamy_chicken_and_bacon_pasta.md" "$VAULT/by-cuisine/italian/"
cp "$RECIPES/chicken_and_mushroom_risotto.md" "$VAULT/by-cuisine/italian/"
cp "$RECIPES/chicken_with_creamy_sun_dried_tomato_sauce.md" "$VAULT/by-cuisine/italian/"
cp "$RECIPES/one_pot_creamy_parmesan_garlic_risotto.md" "$VAULT/by-cuisine/italian/"

cp "$RECIPES/new_orleans_chicken_wings.md" "$VAULT/by-cuisine/american/"
cp "$RECIPES/jambalaya_recipe.md" "$VAULT/by-cuisine/american/"
cp "$RECIPES/lemon_chicken_salad.md" "$VAULT/by-cuisine/american/"
cp "$RECIPES/oven_baked_chicken_and_rice_pilaf.md" "$VAULT/by-cuisine/american/"
cp "$RECIPES/chicken_pot_pie.md" "$VAULT/by-cuisine/american/"

cp "$RECIPES/mexican_chicken_avocado_salad.md" "$VAULT/by-cuisine/mexican/"
cp "$RECIPES/oven_baked_chicken_quesadillas.md" "$VAULT/by-cuisine/mexican/"
cp "$RECIPES/mexican_shredded_chicken.md" "$VAULT/by-cuisine/mexican/"
cp "$RECIPES/one_pot_chicken_enchilada_rice_casserole.md" "$VAULT/by-cuisine/mexican/"

cp "$RECIPES/chicken_broccoli_stir_fry.md" "$VAULT/by-cuisine/chinese/"
cp "$RECIPES/chicken_chow_mein.md" "$VAULT/by-cuisine/chinese/"
cp "$RECIPES/chinese_cashew_chicken.md" "$VAULT/by-cuisine/chinese/"
cp "$RECIPES/crispy_shredded_chicken_noodle_stir_fry.md" "$VAULT/by-cuisine/chinese/"
cp "$RECIPES/10_classic_chinese_dishes.md" "$VAULT/by-cuisine/chinese/"

cp "$RECIPES/jamaican_jerk_chicken_drumsticks.md" "$VAULT/by-cuisine/jamaican/"
cp "$RECIPES/one_pan_spanish_chicken_chorizo.md" "$VAULT/by-cuisine/spanish/"
cp "$RECIPES/chicken_shawarma_middle_eastern.md" "$VAULT/by-cuisine/middle-eastern/"
cp "$RECIPES/vietnamese_caramel_ginger_chicken.md" "$VAULT/by-cuisine/vietnamese/"
cp "$RECIPES/vietnamese_coconut_caramel_chicken.md" "$VAULT/by-cuisine/vietnamese/"
cp "$RECIPES/one_pot_baked_greek_chicken_orzo_risoni.md" "$VAULT/by-cuisine/greek/"
cp "$RECIPES/one_pot_greek_chicken_lemon_rice.md" "$VAULT/by-cuisine/greek/"

# Copy files to by-type
cp "$RECIPES/french_chicken_au_poivre_sauce.md" "$VAULT/by-type/main/"
cp "$RECIPES/thai_grilled_chicken_gai_yang.md" "$VAULT/by-type/main/"
cp "$RECIPES/chicken_chasseur.md" "$VAULT/by-type/main/"
cp "$RECIPES/new_orleans_chicken_wings.md" "$VAULT/by-type/main/"
cp "$RECIPES/chicken_cacciatore.md" "$VAULT/by-type/main/"
cp "$RECIPES/chicken_francese.md" "$VAULT/by-type/main/"
cp "$RECIPES/vietnamese_caramel_ginger_chicken.md" "$VAULT/by-type/main/"
cp "$RECIPES/chicken_marsala.md" "$VAULT/by-type/main/"
cp "$RECIPES/one_pot_baked_greek_chicken_orzo_risoni.md" "$VAULT/by-type/main/"
cp "$RECIPES/thai_red_curry_pot_roast_chicken.md" "$VAULT/by-type/main/"
cp "$RECIPES/chicken_in_creamy_mustard_sauce.md" "$VAULT/by-type/main/"
cp "$RECIPES/chicken_shawarma_middle_eastern.md" "$VAULT/by-type/main/"
cp "$RECIPES/coq_au_vin.md" "$VAULT/by-type/main/"
cp "$RECIPES/chicken_piccata.md" "$VAULT/by-type/main/"
cp "$RECIPES/creamy_chicken_mushroom_fettucine.md" "$VAULT/by-type/main/"
cp "$RECIPES/creamy_tuscan_chicken_pasta_bake.md" "$VAULT/by-type/main/"
cp "$RECIPES/chicken_broccoli_stir_fry.md" "$VAULT/by-type/main/"
cp "$RECIPES/chicken_pad_thai.md" "$VAULT/by-type/main/"
cp "$RECIPES/chicken_chow_mein.md" "$VAULT/by-type/main/"
cp "$RECIPES/thai_basil_chicken_stir_fry.md" "$VAULT/by-type/main/"
cp "$RECIPES/chicken_with_creamy_sun_dried_tomato_sauce.md" "$VAULT/by-type/main/"
cp "$RECIPES/pad_keemao_thai_drunken_noodles.md" "$VAULT/by-type/main/"
cp "$RECIPES/jambalaya_recipe.md" "$VAULT/by-type/main/"
cp "$RECIPES/chicken_pasta_recipe.md" "$VAULT/by-type/main/"
cp "$RECIPES/chinese_cashew_chicken.md" "$VAULT/by-type/main/"
cp "$RECIPES/chicken_pot_pie.md" "$VAULT/by-type/main/"
cp "$RECIPES/oven_baked_chicken_and_rice_pilaf.md" "$VAULT/by-type/main/"
cp "$RECIPES/vietnamese_coconut_caramel_chicken.md" "$VAULT/by-type/main/"
cp "$RECIPES/thai_coconut_chicken.md" "$VAULT/by-type/main/"
cp "$RECIPES/oven_baked_chicken_quesadillas.md" "$VAULT/by-type/main/"
cp "$RECIPES/creamy_chicken_and_bacon_pasta.md" "$VAULT/by-type/main/"
cp "$RECIPES/chicken_and_mushroom_risotto.md" "$VAULT/by-type/main/"
cp "$RECIPES/mexican_shredded_chicken.md" "$VAULT/by-type/main/"
cp "$RECIPES/one_pot_chicken_enchilada_rice_casserole.md" "$VAULT/by-type/main/"
cp "$RECIPES/one_pot_creamy_parmesan_garlic_risotto.md" "$VAULT/by-type/main/"
cp "$RECIPES/one_pot_greek_chicken_lemon_rice.md" "$VAULT/by-type/main/"
cp "$RECIPES/jamaican_jerk_chicken_drumsticks.md" "$VAULT/by-type/main/"
cp "$RECIPES/one_pan_spanish_chicken_chorizo.md" "$VAULT/by-type/main/"
cp "$RECIPES/crispy_shredded_chicken_noodle_stir_fry.md" "$VAULT/by-type/main/"
cp "$RECIPES/10_classic_chinese_dishes.md" "$VAULT/by-type/main/"

cp "$RECIPES/lemon_chicken_salad.md" "$VAULT/by-type/salad/"
cp "$RECIPES/mexican_chicken_avocado_salad.md" "$VAULT/by-type/salad/"

cp "$RECIPES/thai_chicken_lettuce_cups_larb_gai.md" "$VAULT/by-type/appetizer/"

# Copy files to by-method
cp "$RECIPES/thai_grilled_chicken_gai_yang.md" "$VAULT/by-method/grilled/"
cp "$RECIPES/thai_coconut_chicken.md" "$VAULT/by-method/grilled/"

cp "$RECIPES/new_orleans_chicken_wings.md" "$VAULT/by-method/baked/"
cp "$RECIPES/chicken_pot_pie.md" "$VAULT/by-method/baked/"
cp "$RECIPES/oven_baked_chicken_and_rice_pilaf.md" "$VAULT/by-method/baked/"
cp "$RECIPES/oven_baked_chicken_quesadillas.md" "$VAULT/by-method/baked/"
cp "$RECIPES/jamaican_jerk_chicken_drumsticks.md" "$VAULT/by-method/baked/"
cp "$RECIPES/one_pan_spanish_chicken_chorizo.md" "$VAULT/by-method/baked/"
cp "$RECIPES/creamy_tuscan_chicken_pasta_bake.md" "$VAULT/by-method/baked/"

cp "$RECIPES/french_chicken_au_poivre_sauce.md" "$VAULT/by-method/stovetop/"
cp "$RECIPES/chicken_chasseur.md" "$VAULT/by-method/stovetop/"
cp "$RECIPES/chicken_cacciatore.md" "$VAULT/by-method/stovetop/"
cp "$RECIPES/chicken_francese.md" "$VAULT/by-method/stovetop/"
cp "$RECIPES/vietnamese_caramel_ginger_chicken.md" "$VAULT/by-method/stovetop/"
cp "$RECIPES/chicken_marsala.md" "$VAULT/by-method/stovetop/"
cp "$RECIPES/chicken_in_creamy_mustard_sauce.md" "$VAULT/by-method/stovetop/"
cp "$RECIPES/chicken_shawarma_middle_eastern.md" "$VAULT/by-method/stovetop/"
cp "$RECIPES/coq_au_vin.md" "$VAULT/by-method/stovetop/"
cp "$RECIPES/chicken_piccata.md" "$VAULT/by-method/stovetop/"
cp "$RECIPES/creamy_chicken_mushroom_fettucine.md" "$VAULT/by-method/stovetop/"
cp "$RECIPES/chicken_pasta_recipe.md" "$VAULT/by-method/stovetop/"
cp "$RECIPES/chicken_with_creamy_sun_dried_tomato_sauce.md" "$VAULT/by-method/stovetop/"
cp "$RECIPES/chicken_and_mushroom_risotto.md" "$VAULT/by-method/stovetop/"
cp "$RECIPES/creamy_chicken_and_bacon_pasta.md" "$VAULT/by-method/stovetop/"

cp "$RECIPES/one_pot_baked_greek_chicken_orzo_risoni.md" "$VAULT/by-method/one-pot/"
cp "$RECIPES/jambalaya_recipe.md" "$VAULT/by-method/one-pot/"
cp "$RECIPES/one_pot_chicken_enchilada_rice_casserole.md" "$VAULT/by-method/one-pot/"
cp "$RECIPES/one_pot_creamy_parmesan_garlic_risotto.md" "$VAULT/by-method/one-pot/"
cp "$RECIPES/one_pot_greek_chicken_lemon_rice.md" "$VAULT/by-method/one-pot/"

cp "$RECIPES/chicken_broccoli_stir_fry.md" "$VAULT/by-method/stir-fry/"
cp "$RECIPES/chicken_pad_thai.md" "$VAULT/by-method/stir-fry/"
cp "$RECIPES/chicken_chow_mein.md" "$VAULT/by-method/stir-fry/"
cp "$RECIPES/thai_basil_chicken_stir_fry.md" "$VAULT/by-method/stir-fry/"
cp "$RECIPES/pad_keemao_thai_drunken_noodles.md" "$VAULT/by-method/stir-fry/"
cp "$RECIPES/chinese_cashew_chicken.md" "$VAULT/by-method/stir-fry/"
cp "$RECIPES/crispy_shredded_chicken_noodle_stir_fry.md" "$VAULT/by-method/stir-fry/"

cp "$RECIPES/mexican_shredded_chicken.md" "$VAULT/by-method/slow-cooker/"

echo "Done copying files to subdirectories"
