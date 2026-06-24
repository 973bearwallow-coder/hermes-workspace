#!/usr/bin/env python3
"""
RecipeTin Eats bulk importer for recipe vault.
Fetches recipe content and creates markdown files in all vault directories.
"""
import json
import os
import re
import time
import urllib.request
import urllib.error

VAULT_DIR = os.path.expanduser("~/hermes-workspace/projects/recipe-vault")
RECIPES_DIR = os.path.join(VAULT_DIR, "recipes")

# All 43 recipes with their URLs and classifications
RECIPES = [
    {
        "name": "French Chicken au Poivre Sauce",
        "url": "https://www.recipetineats.com/french-chicken-au-poivre-sauce",
        "cuisine": "french",
        "type": "main",
        "method": "stovetop",
        "filename": "french_chicken_au_poivre_sauce.md",
        "fetched": True,  # Already fetched above
    },
    {
        "name": "Thai Grilled Chicken (Gai Yang)",
        "url": "https://www.recipetineats.com/thai-grilled-chicken-gai-yang/",
        "cuisine": "thai",
        "type": "main",
        "method": "grilled",
        "filename": "thai_grilled_chicken_gai_yang.md",
        "fetched": True,
    },
    {
        "name": "Chicken Chasseur",
        "url": "https://www.recipetineats.com/chicken-chasseur/",
        "cuisine": "french",
        "type": "main",
        "method": "stovetop",
        "filename": "chicken_chasseur.md",
        "fetched": True,
    },
    {
        "name": "New Orleans Chicken Wings",
        "url": "https://www.recipetineats.com/new-orleans-chicken-wings/",
        "cuisine": "american",
        "type": "appetizer",
        "method": "baked",
        "filename": "new_orleans_chicken_wings.md",
        "fetched": True,
    },
    {
        "name": "Chicken Cacciatore (Italian Chicken Stew)",
        "url": "https://www.recipetineats.com/chicken-cacciatore-italian-chicken-stew/",
        "cuisine": "italian",
        "type": "main",
        "method": "stovetop",
        "filename": "chicken_cacciatore_italian_chicken_stew.md",
        "fetched": True,
    },
    {
        "name": "Chicken Francese",
        "url": "https://www.recipetineats.com/chicken-francese/",
        "cuisine": "italian",
        "type": "main",
        "method": "stovetop",
        "filename": "chicken_francese.md",
        "fetched": False,
    },
    {
        "name": "Vietnamese Caramel Ginger Chicken",
        "url": "https://www.recipetineats.com/vietnamese-caramel-ginger-chicken/",
        "cuisine": "vietnamese",
        "type": "main",
        "method": "stovetop",
        "filename": "vietnamese_caramel_ginger_chicken.md",
        "fetched": False,
    },
    {
        "name": "Chicken Marsala",
        "url": "https://www.recipetineats.com/chicken-marsala/",
        "cuisine": "italian",
        "type": "main",
        "method": "stovetop",
        "filename": "chicken_marsala.md",
        "fetched": False,
    },
    {
        "name": "One Pot Baked Greek Chicken Orzo Risoni",
        "url": "https://www.recipetineats.com/one-pot-baked-greek-chicken-orzo-risoni/",
        "cuisine": "greek",
        "type": "main",
        "method": "one-pot",
        "filename": "one_pot_baked_greek_chicken_orzo_risoni.md",
        "fetched": False,
    },
    {
        "name": "Thai Red Curry Pot Roast Chicken",
        "url": "https://www.recipetineats.com/thai-red-curry-with-chicken/",
        "cuisine": "thai",
        "type": "main",
        "method": "one-pot",
        "filename": "thai_red_curry_pot_roast_chicken.md",
        "fetched": False,
    },
    {
        "name": "Chicken in Creamy Mustard Sauce",
        "url": "https://www.recipetineats.com/chicken-in-creamy-mustard-sauce/",
        "cuisine": "french",
        "type": "main",
        "method": "stovetop",
        "filename": "chicken_in_creamy_mustard_sauce.md",
        "fetched": False,
    },
    {
        "name": "Chicken Shawarma (Middle Eastern)",
        "url": "https://www.recipetineats.com/chicken-shawarma/",
        "cuisine": "middle-eastern",
        "type": "main",
        "method": "stovetop",
        "filename": "chicken_shawarma_middle_eastern.md",
        "fetched": False,
    },
    {
        "name": "Coq au Vin",
        "url": "https://www.recipetineats.com/coq-au-vin/",
        "cuisine": "french",
        "type": "main",
        "method": "stovetop",
        "filename": "coq_au_vin.md",
        "fetched": False,
    },
    {
        "name": "Chicken Piccata",
        "url": "https://www.recipetineats.com/chicken-piccata/",
        "cuisine": "italian",
        "type": "main",
        "method": "stovetop",
        "filename": "chicken_piccata.md",
        "fetched": False,
    },
    {
        "name": "Creamy Chicken Mushroom Fettucine",
        "url": "https://www.recipetineats.com/creamy-chicken-mushroom-fettuccine/",
        "cuisine": "italian",
        "type": "main",
        "method": "stovetop",
        "filename": "creamy_chicken_mushroom_fettucine.md",
        "fetched": False,
    },
    {
        "name": "Creamy Tuscan Chicken Pasta Bake",
        "url": "https://www.recipetineats.com/creamy-tuscan-chicken-pasta-bake/",
        "cuisine": "italian",
        "type": "main",
        "method": "baked",
        "filename": "creamy_tuscan_chicken_pasta_bake.md",
        "fetched": False,
    },
    {
        "name": "Chicken Broccoli Stir Fry",
        "url": "https://www.recipetineats.com/chicken-broccoli-stir-fry/",
        "cuisine": "chinese",
        "type": "main",
        "method": "stir-fry",
        "filename": "chicken_broccoli_stir_fry.md",
        "fetched": False,
    },
    {
        "name": "Thai Chicken Lettuce Cups (Larb Gai / Laab Gai)",
        "url": "https://www.recipetineats.com/thai-chicken-lettuce-cups/",
        "cuisine": "thai",
        "type": "appetizer",
        "method": "stir-fry",
        "filename": "thai_chicken_lettuce_cups_larb_gai.md",
        "fetched": False,
    },
    {
        "name": "Chicken Pad Thai",
        "url": "https://www.recipetineats.com/chicken-pad-thai/",
        "cuisine": "thai",
        "type": "main",
        "method": "stir-fry",
        "filename": "chicken_pad_thai.md",
        "fetched": False,
    },
    {
        "name": "Chicken Chow Mein",
        "url": "https://www.recipetineats.com/chicken-chow-mein/",
        "cuisine": "chinese",
        "type": "main",
        "method": "stir-fry",
        "filename": "chicken_chow_mein.md",
        "fetched": False,
    },
    {
        "name": "Thai Basil Chicken Stir Fry",
        "url": "https://www.recipetineats.com/thai-basil-chicken-stir-fry/",
        "cuisine": "thai",
        "type": "main",
        "method": "stir-fry",
        "filename": "thai_basil_chicken_stir_fry.md",
        "fetched": False,
    },
    {
        "name": "Chicken with Creamy Sun Dried Tomato Sauce",
        "url": "https://www.recipetineats.com/chicken-with-creamy-sun-dried-tomato-sauce/",
        "cuisine": "italian",
        "type": "main",
        "method": "stovetop",
        "filename": "chicken_with_creamy_sun_dried_tomato_sauce.md",
        "fetched": False,
    },
    {
        "name": "Pad Kee Mao (Thai Drunken Noodles)",
        "url": "https://www.recipetineats.com/pad-keemao-thai-drunken-noodles/",
        "cuisine": "thai",
        "type": "main",
        "method": "stir-fry",
        "filename": "pad_keemao_thai_drunken_noodles.md",
        "fetched": False,
    },
    {
        "name": "Jambalaya Recipe",
        "url": "https://www.recipetineats.com/jambalaya-recipe/",
        "cuisine": "american",
        "type": "main",
        "method": "one-pot",
        "filename": "jambalaya_recipe.md",
        "fetched": False,
    },
    {
        "name": "Chicken Pasta Recipe",
        "url": "https://www.recipetineats.com/chicken-pasta-recipe/",
        "cuisine": "italian",
        "type": "main",
        "method": "stovetop",
        "filename": "chicken_pasta_recipe.md",
        "fetched": False,
    },
    {
        "name": "Chinese Cashew Chicken",
        "url": "https://www.recipetineats.com/chinese-cashew-chicken/",
        "cuisine": "chinese",
        "type": "main",
        "method": "stir-fry",
        "filename": "chinese_cashew_chicken.md",
        "fetched": False,
    },
    {
        "name": "Chicken Pot Pie",
        "url": "https://www.recipetineats.com/chicken-pot-pie/",
        "cuisine": "american",
        "type": "main",
        "method": "baked",
        "filename": "chicken_pot_pie.md",
        "fetched": False,
    },
    {
        "name": "Lemon Chicken Salad",
        "url": "https://www.recipetineats.com/lemon-chicken-salad/",
        "cuisine": "american",
        "type": "salad",
        "method": "stovetop",
        "filename": "lemon_chicken_salad.md",
        "fetched": False,
    },
    {
        "name": "Mexican Chicken Avocado Salad",
        "url": "https://www.recipetineats.com/mexican-chicken-avocado-salad/",
        "cuisine": "mexican",
        "type": "salad",
        "method": "stovetop",
        "filename": "mexican_chicken_avocado_salad.md",
        "fetched": False,
    },
    {
        "name": "Oven Baked Chicken and Rice Pilaf (Cranberry Walnut Apple)",
        "url": "https://www.recipetineats.com/oven-baked-chicken-and-rice-pilaf/",
        "cuisine": "american",
        "type": "main",
        "method": "baked",
        "filename": "oven_baked_chicken_and_rice_pilaf.md",
        "fetched": False,
    },
    {
        "name": "Vietnamese Coconut Caramel Chicken",
        "url": "https://www.recipetineats.com/vietnamese-coconut-caramel-chicken",
        "cuisine": "vietnamese",
        "type": "main",
        "method": "stovetop",
        "filename": "vietnamese_coconut_caramel_chicken.md",
        "fetched": False,
    },
    {
        "name": "Thai Coconut Chicken",
        "url": "https://www.recipetineats.com/thai-coconut-chicken/",
        "cuisine": "thai",
        "type": "main",
        "method": "stovetop",
        "filename": "thai_coconut_chicken.md",
        "fetched": False,
    },
    {
        "name": "Oven Baked Chicken Quesadillas",
        "url": "https://www.recipetineats.com/oven-baked-chicken-quesadillas/",
        "cuisine": "mexican",
        "type": "main",
        "method": "baked",
        "filename": "oven_baked_chicken_quesadillas.md",
        "fetched": False,
    },
    {
        "name": "Creamy Chicken and Bacon Pasta",
        "url": "https://www.recipetineats.com/creamy-chicken-and-bacon-pasta/",
        "cuisine": "italian",
        "type": "main",
        "method": "stovetop",
        "filename": "creamy_chicken_and_bacon_pasta.md",
        "fetched": False,
    },
    {
        "name": "Chicken and Mushroom Risotto",
        "url": "https://www.recipetineats.com/chicken-and-mushroom-risotto/",
        "cuisine": "italian",
        "type": "main",
        "method": "stovetop",
        "filename": "chicken_and_mushroom_risotto.md",
        "fetched": False,
    },
    {
        "name": "Mexican Shredded Chicken",
        "url": "https://www.recipetineats.com/mexican-shredded-chicken/",
        "cuisine": "mexican",
        "type": "main",
        "method": "stovetop",
        "filename": "mexican_shredded_chicken.md",
        "fetched": False,
    },
    {
        "name": "One Pot Chicken Enchilada Rice Casserole",
        "url": "https://www.recipetineats.com/one-pot-chicken-enchilada-rice-casserole/",
        "cuisine": "mexican",
        "type": "main",
        "method": "one-pot",
        "filename": "one_pot_chicken_enchilada_rice_casserole.md",
        "fetched": False,
    },
    {
        "name": "One Pot Creamy Parmesan Garlic Risotto with Lemon Pepper Chicken",
        "url": "https://www.recipetineats.com/one-pot-creamy-parmesan-garlic-risotto-with-lemon-pepper-chicken/",
        "cuisine": "italian",
        "type": "main",
        "method": "one-pot",
        "filename": "one_pot_creamy_parmesan_garlic_risotto.md",
        "fetched": False,
    },
    {
        "name": "One Pot Greek Chicken Lemon Rice",
        "url": "https://www.recipetineats.com/one-pot-greek-chicken-lemon-rice/",
        "cuisine": "greek",
        "type": "main",
        "method": "one-pot",
        "filename": "one_pot_greek_chicken_lemon_rice.md",
        "fetched": False,
    },
    {
        "name": "Jamaican Jerk Chicken Drumsticks with Caribbean Rice and Beans",
        "url": "https://www.recipetineats.com/jamaican-jerk-chicken-drumsticks/",
        "cuisine": "jamaican",
        "type": "main",
        "method": "baked",
        "filename": "jamaican_jerk_chicken_drumsticks.md",
        "fetched": False,
    },
    {
        "name": "One Pan Spanish Chicken Chorizo Tomato Potatoes",
        "url": "https://www.recipetineats.com/one-pan-spanish-chicken-chorizo-tomato-potatoes/",
        "cuisine": "spanish",
        "type": "main",
        "method": "one-pot",
        "filename": "one_pan_spanish_chicken_chorizo.md",
        "fetched": False,
    },
    {
        "name": "Crispy Shredded Chicken Noodle Stir Fry",
        "url": "https://www.recipetineats.com/crispy-shredded-chicken-noodle-stir-fry/",
        "cuisine": "chinese",
        "type": "main",
        "method": "stir-fry",
        "filename": "crispy_shredded_chicken_noodle_stir_fry.md",
        "fetched": False,
    },
    {
        "name": "10 Classic Chinese Dishes + Homemade Teriyaki Sauce",
        "url": "https://www.recipetineats.com/10-classic-chinese-dishes/",
        "cuisine": "chinese",
        "type": "main",
        "method": "stir-fry",
        "filename": "10_classic_chinese_dishes.md",
        "fetched": False,
    },
]


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def write_recipe_file(filepath, content):
    """Write a recipe markdown file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def copy_to_subdirs(recipe_info, content):
    """Copy recipe to by-cuisine, by-type, by-method subdirectories."""
    base = os.path.expanduser("~/hermes-workspace/projects/recipe-vault")
    fname = recipe_info["filename"]

    # by-cuisine
    cuisine_dir = os.path.join(base, "by-cuisine", recipe_info["cuisine"])
    ensure_dir(cuisine_dir)
    write_recipe_file(os.path.join(cuisine_dir, fname), content)

    # by-type
    type_dir = os.path.join(base, "by-type", recipe_info["type"])
    ensure_dir(type_dir)
    write_recipe_file(os.path.join(type_dir, fname), content)

    # by-method
    method_dir = os.path.join(base, "by-method", recipe_info["method"])
    ensure_dir(method_dir)
    write_recipe_file(os.path.join(method_dir, fname), content)


if __name__ == "__main__":
    # Just print the recipe list for verification
    print(f"Total recipes to process: {len(RECIPES)}")
    for r in RECIPES:
        status = "DONE" if r["fetched"] else "PENDING"
        print(f"  [{status}] {r['name']} -> {r['filename']}")
