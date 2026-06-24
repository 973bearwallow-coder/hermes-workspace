#!/bin/bash
# Create symlinks for ALL recipes in the recipe vault classification directories
# Run from ~/hermes-workspace/projects/recipe-vault/

cd ~/hermes-workspace/projects/recipe-vault

# Clean existing symlinks
for sub in by-cuisine by-type by-method; do
    find "$sub" -type l -delete 2>/dev/null
done

count=0

# Function to create symlinks for a recipe
create_links() {
    local fname="$1"
    local cuisine="$2"
    local rtype="$3"
    local method="$4"
    
    for c in $cuisine; do
        mkdir -p "by-cuisine/$c"
        ln -sf "../../recipes/$fname" "by-cuisine/$c/$fname"
    done
    for t in $rtype; do
        mkdir -p "by-type/$t"
        ln -sf "../../recipes/$fname" "by-type/$t/$fname"
    done
    for m in $method; do
        mkdir -p "by-method/$m"
        ln -sf "../../recipes/$fname" "by-method/$m/$fname"
    done
    ((count++))
}

# === RecipeTin Eats ===
create_links "french_chicken_au_poivre_sauce.md" "french" "main" "stovetop"
create_links "thai_grilled_chicken_gai_yang.md" "thai" "main" "grilled"
create_links "chicken_chasseur.md" "french" "main" "stovetop"
create_links "new_orleans_chicken_wings.md" "american" "appetizer" "baked"
create_links "chicken_cacciatore_italian_chicken_stew.md" "italian" "main" "stovetop"
create_links "chicken_francese.md" "italian" "main" "stovetop"
create_links "vietnamese_caramel_ginger_chicken.md" "vietnamese" "main" "stovetop"
create_links "chicken_marsala.md" "italian" "main" "stovetop"
create_links "one_pot_baked_greek_chicken_orzo_risoni.md" "greek" "main" "one-pot"
create_links "thai_red_curry_pot_roast_chicken.md" "thai" "main" "baked"
create_links "chicken_in_creamy_mustard_sauce.md" "french" "main" "stovetop"
create_links "chicken_shawarma_middle_eastern.md" "middle-eastern" "main" "stovetop"
create_links "coq_au_vin.md" "french" "main" "baked"
create_links "chicken_piccata.md" "italian" "main" "stovetop"
create_links "creamy_chicken_mushroom_fettucine.md" "italian" "main" "stovetop"
create_links "creamy_tuscan_chicken_pasta_bake.md" "italian" "main" "baked"
create_links "chicken_broccoli_stir_fry.md" "chinese" "main" "stir-fry"
create_links "thai_chicken_lettuce_cups_larb_gai.md" "thai" "main" "stir-fry"
create_links "chicken_pad_thai.md" "thai" "main" "stir-fry"
create_links "chicken_chow_mein.md" "chinese" "main" "stir-fry"
create_links "thai_basil_chicken_stir_fry.md" "thai" "main" "stir-fry"
create_links "chicken_with_creamy_sun_dried_tomato_sauce.md" "italian" "main" "stovetop"
create_links "pad_keemao_thai_drunken_noodles.md" "thai" "main" "stir-fry"
create_links "jambalaya_recipe.md" "american" "main" "one-pot"
create_links "chicken_pasta_recipe.md" "italian" "main" "stovetop"
create_links "chinese_cashew_chicken.md" "chinese" "main" "stir-fry"
create_links "chicken_pot_pie.md" "american" "main" "baked"
create_links "lemon_chicken_salad.md" "american" "salad" "stovetop"
create_links "mexican_chicken_avocado_salad.md" "mexican" "salad" "stovetop"
create_links "oven_baked_chicken_and_rice_pilaf.md" "american" "main" "baked"
create_links "vietnamese_coconut_caramel_chicken.md" "vietnamese" "main" "stovetop"
create_links "thai_coconut_chicken.md" "thai" "main" "grilled"
create_links "oven_baked_chicken_quesadillas.md" "mexican" "main" "baked"
create_links "creamy_chicken_and_bacon_pasta.md" "italian" "main" "stovetop"
create_links "chicken_and_mushroom_risotto.md" "italian" "main" "stovetop"
create_links "mexican_shredded_chicken.md" "mexican" "main" "slow-cooker"
create_links "one_pot_chicken_enchilada_rice_casserole.md" "mexican" "main" "one-pot"
create_links "one_pot_creamy_parmesan_garlic_risotto.md" "italian" "main" "one-pot"
create_links "one_pot_greek_chicken_lemon_rice.md" "greek" "main" "one-pot"
create_links "jamaican_jerk_chicken_drumsticks.md" "jamaican" "main" "baked"
create_links "one_pan_spanish_chicken_chorizo.md" "spanish" "main" "baked"
create_links "crispy_shredded_chicken_noodle_stir_fry.md" "chinese" "main" "stir-fry"
create_links "10_classic_chinese_dishes.md" "chinese" "main" "stir-fry"
create_links "chicken_au_poivre_sauce.md" "french" "main" "stovetop"

# === Mel's Kitchen Cafe ===
create_links "amazing_crustless_pumpkin_pie_cupcakes.md" "american" "dessert" "baked"
create_links "amazing_key_lime_cheesecake.md" "american" "dessert" "baked"
create_links "amazing_spinach_salad_with_sweet-spicy_nuts_apples_feta_and_.md" "american" "salad" "stovetop"
create_links "amish-style_apple_and_cinnamon_baked_oatmeal.md" "american" "breakfast" "baked"
create_links "apple_cranberry_pie_my_favorite_thanksgiving_pie.md" "american" "dessert" "baked"
create_links "avocado_chicken_salad.md" "american" "salad" "no-cook"
create_links "beach_street_lemon_chicken_pasta.md" "american" "main" "stovetop"
create_links "buttery_cinnamon_pull-apart_bread_dollywood_bread_knockoff.md" "american" "bread" "baked"
create_links "cheesy_funeral_potatoes_au_gratin_potatoes.md" "american" "side" "baked"
create_links "chopped_greek_chicken_salad_with_pita_croutons_and_tzatziki_.md" "greek" "salad" "grilled"
create_links "creamy_cilantro_lime_dressing.md" "american mexican" "side" "no-cook"
create_links "creamy_garlic_alfredo_sauce_my_go-to_dinner_saver.md" "american italian" "main" "stovetop"
create_links "dark_chocolate_sea_salt_caramel_pretzel_bark_snappers_knock_.md" "american" "dessert" "stovetop"
create_links "decadent_chocolate_cheesecake.md" "american" "dessert" "baked"
create_links "easy_cowboy_caviar_dip_aka_shrapnel_dip.md" "american mexican" "appetizer" "no-cook"
create_links "easy_homemade_french_bread.md" "french" "bread" "baked"
create_links "easy_rustic_crusty_bread_with_tutorial_no_mixer_no_kneading.md" "american" "bread" "baked"
create_links "harvest_apple_salad.md" "american" "salad" "no-cook"
create_links "heavenly_raspberry_cream_angel_food_cake_dessert.md" "american" "dessert" "no-cook"
create_links "honey_lime_fruit_salad.md" "american" "salad" "no-cook"
create_links "hot_fudge_pudding_cake.md" "american" "dessert" "baked"
create_links "lemon_blueberry_cake_with_whipped_lemon_cream_frosting.md" "american" "dessert" "baked"
create_links "lemon_chicken_orzo_soup.md" "american" "soup" "stovetop"
create_links "little_lemonies_yummy_lemon_brownies.md" "american" "dessert" "baked"
create_links "mexican_street_corn_salad.md" "mexican" "salad" "stovetop"
create_links "my_favorite_cherry_pie_in_the_history_of_ever.md" "american" "dessert" "baked"
create_links "my_mom8217s_famous_caramels.md" "american" "dessert" "stovetop"
create_links "orange_sweet_rolls.md" "american" "bread" "baked"
create_links "orange_zested_cranberry_white_chocolate_bliss_bars.md" "american" "dessert" "baked"
create_links "oreo_cheesecake_bites.md" "american" "dessert" "baked"
create_links "overnight_cinnamon_and_sugar_sweet_rolls.md" "american" "bread" "baked overnight"
create_links "overnight_strawberry_cream_cheese_sweet_rolls.md" "american" "bread" "baked overnight"
create_links "peanut_butter_cup_cheesecake_with_chocolate_cookie_crust.md" "american" "dessert" "baked"
create_links "penne_with_roasted_asparagus_and_balsamic_butter.md" "american italian" "main" "stovetop"
create_links "perfect_caramel_pecan_sticky_buns.md" "american" "bread" "baked"
create_links "slow_cooker_posole.md" "mexican" "soup" "slow-cooker"
create_links "soft_and_chewy_caramel_popcorn.md" "american" "snack" "stovetop"
create_links "spaghetti_pie.md" "american italian" "main" "baked"
create_links "strawberry_spinach_salad_with_homemade_poppy_seed_dressing.md" "american" "salad" "no-cook"
create_links "sweet_baked_ham.md" "american" "main" "baked"
create_links "the_best_and_only_pie_crust_recipe_038_tutorial_you8217ll_ev.md" "american" "bread" "baked"
create_links "the_best_carrot_cake_with_whipped_cream_cheese_frosting.md" "american" "dessert" "baked"
create_links "the_best_cheesy_garlic_drop_biscuits_red_lobster_knockoff.md" "american" "side" "baked"
create_links "the_best_lemon_bars.md" "american" "dessert" "baked"
create_links "the_best_monkey_bread.md" "american" "bread" "baked"
create_links "the_best_spinach_artichoke_dip.md" "american" "appetizer" "baked"
create_links "white_chocolate_raspberry_truffle_cheesecake.md" "american" "dessert" "baked"

echo "Created symlinks for $count recipes across by-cuisine/, by-type/, and by-method/"
echo ""
echo "Cuisine directories:"
ls -1 by-cuisine/
echo ""
echo "Type directories:"
ls -1 by-type/
echo ""
echo "Method directories:"
ls -1 by-method/
