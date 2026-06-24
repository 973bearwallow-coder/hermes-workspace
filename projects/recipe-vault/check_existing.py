#!/usr/bin/env python3
"""Check which of the 43 recipes exist and which need to be added."""
import os
from pathlib import Path

VAULT_DIR = Path.home() / "hermes-workspace/projects/recipe-vault"
RECIPES_DIR = VAULT_DIR / "recipes"

recipes = [
    ("french", "main", "stovetop", "french_chicken_au_poivre_sauce.md", "French Chicken au Poivre Sauce", "https://www.recipetineats.com/french-chicken-au-poivre-sauce/"),
    ("thai", "main", "grilled", "thai_grilled_chicken_gai_yang.md", "Thai Grilled Chicken (Gai Yang)", "https://www.recipetineats.com/thai-grilled-chicken-gai-yang/"),
    ("french", "main", "stovetop", "chicken_chasseur.md", "Chicken Chasseur", "https://www.recipetineats.com/chicken-chasseur/"),
    ("american", "appetizer", "baked", "new_orleans_chicken_wings.md", "New Orleans Chicken Wings", "https://www.recipetineats.com/new-orleans-chicken-wings/"),
    ("italian", "main", "stovetop", "chicken_cacciatore_italian_chicken_stew.md", "Chicken Cacciatore (Italian Chicken Stew)", "https://www.recipetineats.com/chicken-cacciatore-italian-chicken-stew/"),
    ("italian", "main", "stovetop", "chicken_francese.md", "Chicken Francese", "https://www.recipetineats.com/chicken-francese/"),
    ("vietnamese", "main", "stovetop", "vietnamese_caramel_ginger_chicken.md", "Vietnamese Caramel Ginger Chicken", "https://www.recipetineats.com/vietnamese-caramel-ginger-chicken/"),
    ("italian", "main", "stovetop", "chicken_marsala.md", "Chicken Marsala", "https://www.recipetineats.com/chicken-marsala/"),
    ("greek", "main", "one-pot", "one_pot_baked_greek_chicken_orzo_risoni.md", "One Pot Baked Greek Chicken Orzo Risoni", "https://www.recipetineats.com/one-pot-baked-greek-chicken-orzo-risoni/"),
    ("thai", "main", "baked", "thai_red_curry_pot_roast_chicken.md", "Thai Red Curry Pot Roast Chicken", "https://www.recipetineats.com/thai-red-curry-pot-roast-chicken/"),
    ("french", "main", "stovetop", "chicken_in_creamy_mustard_sauce.md", "Chicken in Creamy Mustard Sauce", "https://www.recipetineats.com/chicken-in-creamy-mustard-sauce/"),
    ("middle-eastern", "main", "stovetop", "chicken_shawarma_middle_eastern.md", "Chicken Shawarma (Middle Eastern)", "https://www.recipetineats.com/chicken-sharwama-middle-eastern/"),
    ("french", "main", "baked", "coq_au_vin.md", "Coq au Vin", "https://www.recipetineats.com/coq-au-vin/"),
    ("italian", "main", "stovetop", "chicken_piccata.md", "Chicken Piccata", "https://www.recipetineats.com/chicken-piccata/"),
    ("italian", "main", "stovetop", "creamy_chicken_mushroom_fettucine.md", "Creamy Chicken Mushroom Fettucine", "https://www.recipetineats.com/creamy-chicken-mushroom-fettucine/"),
    ("italian", "main", "baked", "creamy_tuscan_chicken_pasta_bake.md", "Creamy Tuscan Chicken Pasta Bake", "https://www.recipetineats.com/creamy-tuscan-chicken-pasta-bake/"),
    ("chinese", "main", "stir-fry", "chicken_broccoli_stir_fry.md", "Chicken Broccoli Stir Fry", "https://www.recipetineats.com/chicken-broccoli-stir-fry/"),
    ("thai", "main", "stir-fry", "thai_chicken_lettuce_cups_larb_gai.md", "Thai Chicken Lettuce Cups (Larb Gai / Laab Gai)", "https://www.recipetineats.com/thai-chicken-lettuce-cups-larb-gai/"),
    ("thai", "main", "stir-fry", "chicken_pad_thai.md", "Chicken Pad Thai", "https://www.recipetineats.com/chicken-pad-thai/"),
    ("chinese", "main", "stir-fry", "chicken_chow_mein.md", "Chicken Chow Mein", "https://www.recipetineats.com/chicken-chow-mein/"),
    ("thai", "main", "stir-fry", "thai_basil_chicken_stir_fry.md", "Thai Basil Chicken Stir Fry", "https://www.recipetineats.com/thai-basil-chicken-stir-fry/"),
    ("italian", "main", "stovetop", "chicken_with_creamy_sun_dried_tomato_sauce.md", "Chicken with Creamy Sun Dried Tomato Sauce", "https://www.recipetineats.com/chicken-with-creamy-sun-dried-tomato-sauce/"),
    ("thai", "main", "stir-fry", "pad_keemao_thai_drunken_noodles.md", "Pad Kee Mao (Thai Drunken Noodles)", "https://www.recipetineats.com/pad-kee-mao-thai-drunken-noodles/"),
    ("american", "main", "one-pot", "jambalaya_recipe.md", "Jambalaya Recipe", "https://www.recipetineats.com/jambalaya-recipe/"),
    ("italian", "main", "stovetop", "chicken_pasta_recipe.md", "Chicken Pasta Recipe", "https://www.recipetineats.com/chicken-pasta-recipe/"),
    ("chinese", "main", "stir-fry", "chinese_cashew_chicken.md", "Chinese Cashew Chicken", "https://www.recipetineats.com/chinese-cashew-chicken/"),
    ("american", "main", "baked", "chicken_pot_pie.md", "Chicken Pot Pie", "https://www.recipetineats.com/chicken-pot-pie/"),
    ("american", "salad", "stovetop", "lemon_chicken_salad.md", "Lemon Chicken Salad", "https://www.recipetineats.com/lemon-chicken-salad/"),
    ("mexican", "salad", "grilled", "mexican_chicken_avocado_salad.md", "Mexican Chicken Avocado Salad", "https://www.recipetineats.com/mexican-chicken-avocado-salad/"),
    ("american", "main", "baked", "oven_baked_chicken_and_rice_pilaf.md", "Oven Baked Chicken and Rice Pilaf (Cranberry Walnut Apple)", "https://www.recipetineats.com/oven-baked-chicken-and-rice-pilaf-cranberry-walnut-apple/"),
    ("vietnamese", "main", "stovetop", "vietnamese_coconut_caramel_chicken.md", "Vietnamese Coconut Caramel Chicken", "https://www.recipetineats.com/vietnamese-coconut-caramel-chicken/"),
    ("thai", "main", "grilled", "thai_coconut_chicken.md", "Thai Coconut Chicken", "https://www.recipetineats.com/thai-coconut-chicken/"),
    ("mexican", "main", "baked", "oven_baked_chicken_quesadillas.md", "Oven Baked Chicken Quesadillas", "https://www.recipetineats.com/oven-baked-chicken-quesadillas/"),
    ("italian", "main", "stovetop", "creamy_chicken_and_bacon_pasta.md", "Creamy Chicken and Bacon Pasta", "https://www.recipetineats.com/creamy-chicken-and-bacon-pasta/"),
    ("italian", "main", "stovetop", "chicken_and_mushroom_risotto.md", "Chicken and Mushroom Risotto", "https://www.recipetineats.com/chicken-and-mushroom-risotto/"),
    ("mexican", "main", "slow-cooker", "mexican_shredded_chicken.md", "Mexican Shredded Chicken", "https://www.recipetineats.com/mexican-shredded-chicken/"),
    ("mexican", "main", "one-pot", "one_pot_chicken_enchilada_rice_casserole.md", "One Pot Chicken Enchilada Rice Casserole", "https://www.recipetineats.com/one-pot-chicken-enchilada-rice-casserole/"),
    ("italian", "main", "one-pot", "one_pot_creamy_parmesan_garlic_risotto.md", "One Pot Creamy Parmesan Garlic Risotto with Lemon Pepper Chicken", "https://www.recipetineats.com/one-pot-creamy-parmesan-garlic-risotto-with-lemon-pepper-chicken/"),
    ("greek", "main", "one-pot", "one_pot_greek_chicken_lemon_rice.md", "One Pot Greek Chicken Lemon Rice", "https://www.recipetineats.com/one-pot-greek-chicken-lemon-rice/"),
    ("jamaican", "main", "baked", "jamaican_jerk_chicken_drumsticks.md", "Jamaican Jerk Chicken Drumsticks with Caribbean Rice and Beans", "https://www.recipetineats.com/jamaican-jerk-chicken-drumsticks-with-caribbean-rice-with-beans/"),
    ("spanish", "main", "baked", "one_pan_spanish_chicken_chorizo.md", "One Pan Spanish Chicken Chorizo Tomato Potatoes", "https://www.recipetineats.com/one-pan-spanish-chicken-chorizo-tomato-potatoes/"),
    ("chinese", "main", "stir-fry", "crispy_shredded_chicken_noodle_stir_fry.md", "Crispy Shredded Chicken Noodle Stir Fry", "https://www.recipetineats.com/crispy-shredded-chicken-noodle-stir-fry/"),
    ("chinese", "main", "stir-fry", "10_classic_chinese_dishes.md", "10 Classic Chinese Dishes + Homemade Teriyaki Sauce", "https://www.recipetineats.com/10-classic-chinese-dishes/"),
]

existing = 0
missing = 0
missing_list = []

for (cuisine, type_, method, filename, name, url) in recipes:
    filepath = RECIPES_DIR / filename
    if filepath.exists():
        size = filepath.stat().st_size
        existing += 1
        print(f"  EXISTS ({size}b): {filename}")
    else:
        missing += 1
        missing_list.append((cuisine, type_, method, filename, name, url))
        print(f"  MISSING: {filename}")

print(f"\nTotal: {len(recipes)}, Existing: {existing}, Missing: {missing}")
if missing_list:
    print("\nMissing recipes:")
    for (c, t, m, f, n, u) in missing_list:
        print(f"  - {n} ({f})")
