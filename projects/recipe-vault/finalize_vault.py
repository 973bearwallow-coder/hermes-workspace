#!/usr/bin/env python3
"""
Master recipe file writer - creates all by-cuisine, by-type, by-method copies
and the final index.json for all 43 RecipeTin Eats recipes.
Run this after all recipe files have been written to recipes/
"""
import json
import os
import shutil
from datetime import datetime

VAULT = os.path.expanduser("~/hermes-workspace/projects/recipe-vault")

# All 43 recipes with metadata
NEW_RECIPES = [
    {"name": "French Chicken au Poivre Sauce", "file": "french_chicken_au_poivre_sauce.md", "cuisines": ["french"], "types": ["main"], "methods": ["stovetop"], "url": "https://www.recipetineats.com/french-chicken-au-poivre-sauce"},
    {"name": "Thai Grilled Chicken (Gai Yang)", "file": "thai_grilled_chicken_gai_yang.md", "cuisines": ["thai"], "types": ["main"], "methods": ["grilled"], "url": "https://www.recipetineats.com/thai-grilled-chicken-gai-yang/"},
    {"name": "Chicken Chasseur", "file": "chicken_chasseur.md", "cuisines": ["french"], "types": ["main"], "methods": ["stovetop"], "url": "https://www.recipetineats.com/chicken-chasseur/"},
    {"name": "New Orleans Chicken Wings", "file": "new_orleans_chicken_wings.md", "cuisines": ["american"], "types": ["appetizer"], "methods": ["baked"], "url": "https://www.recipetineats.com/new-orleans-chicken-wings/"},
    {"name": "Chicken Cacciatore (Italian Chicken Stew)", "file": "chicken_cacciatore_italian_chicken_stew.md", "cuisines": ["italian"], "types": ["main"], "methods": ["stovetop"], "url": "https://www.recipetineats.com/chicken-cacciatore-italian-chicken-stew/"},
    {"name": "Chicken Francese", "file": "chicken_francese.md", "cuisines": ["italian"], "types": ["main"], "methods": ["stovetop"], "url": "https://www.recipetineats.com/chicken-francese/"},
    {"name": "Vietnamese Caramel Ginger Chicken", "file": "vietnamese_caramel_ginger_chicken.md", "cuisines": ["vietnamese"], "types": ["main"], "methods": ["stovetop"], "url": "https://www.recipetineats.com/vietnamese-caramel-ginger-chicken/"},
    {"name": "Chicken Marsala", "file": "chicken_marsala.md", "cuisines": ["italian"], "types": ["main"], "methods": ["stovetop"], "url": "https://www.recipetineats.com/chicken-marsala/"},
    {"name": "One Pot Baked Greek Chicken Orzo Risoni", "file": "one_pot_baked_greek_chicken_orzo_risoni.md", "cuisines": ["greek"], "types": ["main"], "methods": ["one-pot"], "url": "https://www.recipetineats.com/one-pot-baked-greek-chicken-orzo-risoni/"},
    {"name": "Thai Red Curry Pot Roast Chicken", "file": "thai_red_curry_pot_roast_chicken.md", "cuisines": ["thai"], "types": ["main"], "methods": ["one-pot"], "url": "https://www.recipetineats.com/thai-red-curry-with-chicken/"},
    {"name": "Chicken in Creamy Mustard Sauce", "file": "chicken_in_creamy_mustard_sauce.md", "cuisines": ["french"], "types": ["main"], "methods": ["stovetop"], "url": "https://www.recipetineats.com/chicken-in-creamy-mustard-sauce/"},
    {"name": "Chicken Shawarma (Middle Eastern)", "file": "chicken_shawarma_middle_eastern.md", "cuisines": ["middle-eastern"], "types": ["main"], "methods": ["stovetop"], "url": "https://www.recipetineats.com/chicken-shawarma/"},
    {"name": "Coq au Vin", "file": "coq_au_vin.md", "cuisines": ["french"], "types": ["main"], "methods": ["stovetop"], "url": "https://www.recipetineats.com/coq-au-vin/"},
    {"name": "Chicken Piccata", "file": "chicken_piccata.md", "cuisines": ["italian"], "types": ["main"], "methods": ["stovetop"], "url": "https://www.recipetineats.com/chicken-piccata/"},
    {"name": "Creamy Chicken Mushroom Fettucine", "file": "creamy_chicken_mushroom_fettucine.md", "cuisines": ["italian"], "types": ["main"], "methods": ["stovetop"], "url": "https://www.recipetineats.com/creamy-chicken-mushroom-fettuccine/"},
    {"name": "Creamy Tuscan Chicken Pasta Bake", "file": "creamy_tuscan_chicken_pasta_bake.md", "cuisines": ["italian"], "types": ["main"], "methods": ["baked"], "url": "https://www.recipetineats.com/creamy-tuscan-chicken-pasta-bake/"},
    {"name": "Chicken Broccoli Stir Fry", "file": "chicken_broccoli_stir_fry.md", "cuisines": ["chinese"], "types": ["main"], "methods": ["stir-fry"], "url": "https://www.recipetineats.com/chicken-broccoli-stir-fry/"},
    {"name": "Thai Chicken Lettuce Cups (Larb Gai / Laab Gai)", "file": "thai_chicken_lettuce_cups_larb_gai.md", "cuisines": ["thai"], "types": ["appetizer"], "methods": ["stir-fry"], "url": "https://www.recipetineats.com/thai-chicken-lettuce-cups/"},
    {"name": "Chicken Pad Thai", "file": "chicken_pad_thai.md", "cuisines": ["thai"], "types": ["main"], "methods": ["stir-fry"], "url": "https://www.recipetineats.com/chicken-pad-thai/"},
    {"name": "Chicken Chow Mein", "file": "chicken_chow_mein.md", "cuisines": ["chinese"], "types": ["main"], "methods": ["stir-fry"], "url": "https://www.recipetineats.com/chicken-chow-mein/"},
    {"name": "Thai Basil Chicken Stir Fry", "file": "thai_basil_chicken_stir_fry.md", "cuisines": ["thai"], "types": ["main"], "methods": ["stir-fry"], "url": "https://www.recipetineats.com/thai-basil-chicken-stir-fry/"},
    {"name": "Chicken with Creamy Sun Dried Tomato Sauce", "file": "chicken_with_creamy_sun_dried_tomato_sauce.md", "cuisines": ["italian"], "types": ["main"], "methods": ["stovetop"], "url": "https://www.recipetineats.com/chicken-with-creamy-sun-dried-tomato-sauce/"},
    {"name": "Pad Kee Mao (Thai Drunken Noodles)", "file": "pad_keemao_thai_drunken_noodles.md", "cuisines": ["thai"], "types": ["main"], "methods": ["stir-fry"], "url": "https://www.recipetineats.com/pad-keemao-thai-drunken-noodles/"},
    {"name": "Jambalaya Recipe", "file": "jambalaya_recipe.md", "cuisines": ["american"], "types": ["main"], "methods": ["one-pot"], "url": "https://www.recipetineats.com/jambalaya-recipe/"},
    {"name": "Chicken Pasta Recipe", "file": "chicken_pasta_recipe.md", "cuisines": ["italian"], "types": ["main"], "methods": ["stovetop"], "url": "https://www.recipetineats.com/chicken-pasta-recipe/"},
    {"name": "Chinese Cashew Chicken", "file": "chinese_cashew_chicken.md", "cuisines": ["chinese"], "types": ["main"], "methods": ["stir-fry"], "url": "https://www.recipetineats.com/chinese-cashew-chicken/"},
    {"name": "Chicken Pot Pie", "file": "chicken_pot_pie.md", "cuisines": ["american"], "types": ["main"], "methods": ["baked"], "url": "https://www.recipetineats.com/chicken-pot-pie/"},
    {"name": "Lemon Chicken Salad", "file": "lemon_chicken_salad.md", "cuisines": ["american"], "types": ["salad"], "methods": ["stovetop"], "url": "https://www.recipetineats.com/lemon-chicken-salad/"},
    {"name": "Mexican Chicken Avocado Salad", "file": "mexican_chicken_avocado_salad.md", "cuisines": ["mexican"], "types": ["salad"], "methods": ["stovetop"], "url": "https://www.recipetineats.com/mexican-chicken-avocado-salad/"},
    {"name": "Oven Baked Chicken and Rice Pilaf (Cranberry Walnut Apple)", "file": "oven_baked_chicken_and_rice_pilaf.md", "cuisines": ["american"], "types": ["main"], "methods": ["baked"], "url": "https://www.recipetineats.com/oven-baked-chicken-and-rice-pilaf/"},
    {"name": "Vietnamese Coconut Caramel Chicken", "file": "vietnamese_coconut_caramel_chicken.md", "cuisines": ["vietnamese"], "types": ["main"], "methods": ["stovetop"], "url": "https://www.recipetineats.com/vietnamese-coconut-caramel-chicken"},
    {"name": "Thai Coconut Chicken", "file": "thai_coconut_chicken.md", "cuisines": ["thai"], "types": ["main"], "methods": ["stovetop"], "url": "https://www.recipetineats.com/thai-coconut-chicken/"},
    {"name": "Oven Baked Chicken Quesadillas", "file": "oven_baked_chicken_quesadillas.md", "cuisines": ["mexican"], "types": ["main"], "methods": ["baked"], "url": "https://www.recipetineats.com/oven-baked-chicken-quesadillas/"},
    {"name": "Creamy Chicken and Bacon Pasta", "file": "creamy_chicken_and_bacon_pasta.md", "cuisines": ["italian"], "types": ["main"], "methods": ["stovetop"], "url": "https://www.recipetineats.com/creamy-chicken-and-bacon-pasta/"},
    {"name": "Chicken and Mushroom Risotto", "file": "chicken_and_mushroom_risotto.md", "cuisines": ["italian"], "types": ["main"], "methods": ["stovetop"], "url": "https://www.recipetineats.com/chicken-and-mushroom-risotto/"},
    {"name": "Mexican Shredded Chicken", "file": "mexican_shredded_chicken.md", "cuisines": ["mexican"], "types": ["main"], "methods": ["stovetop"], "url": "https://www.recipetineats.com/mexican-shredded-chicken/"},
    {"name": "One Pot Chicken Enchilada Rice Casserole", "file": "one_pot_chicken_enchilada_rice_casserole.md", "cuisines": ["mexican"], "types": ["main"], "methods": ["one-pot"], "url": "https://www.recipetineats.com/one-pot-chicken-enchilada-rice-casserole/"},
    {"name": "One Pot Creamy Parmesan Garlic Risotto with Lemon Pepper Chicken", "file": "one_pot_creamy_parmesan_garlic_risotto.md", "cuisines": ["italian"], "types": ["main"], "methods": ["one-pot"], "url": "https://www.recipetineats.com/one-pot-creamy-parmesan-garlic-risotto-with-lemon-pepper-chicken/"},
    {"name": "One Pot Greek Chicken Lemon Rice", "file": "one_pot_greek_chicken_lemon_rice.md", "cuisines": ["greek"], "types": ["main"], "methods": ["one-pot"], "url": "https://www.recipetineats.com/one-pot-greek-chicken-lemon-rice/"},
    {"name": "Jamaican Jerk Chicken Drumsticks with Caribbean Rice and Beans", "file": "jamaican_jerk_chicken_drumsticks.md", "cuisines": ["jamaican"], "types": ["main"], "methods": ["baked"], "url": "https://www.recipetineats.com/jamaican-jerk-chicken-drumsticks/"},
    {"name": "One Pan Spanish Chicken Chorizo Tomato Potatoes", "file": "one_pan_spanish_chicken_chorizo.md", "cuisines": ["spanish"], "types": ["main"], "methods": ["one-pot"], "url": "https://www.recipetineats.com/one-pan-spanish-chicken-chorizo-tomato-potatoes/"},
    {"name": "Crispy Shredded Chicken Noodle Stir Fry", "file": "crispy_shredded_chicken_noodle_stir_fry.md", "cuisines": ["chinese"], "types": ["main"], "methods": ["stir-fry"], "url": "https://www.recipetineats.com/crispy-shredded-chicken-noodle-stir-fry/"},
    {"name": "10 Classic Chinese Dishes + Homemade Teriyaki Sauce", "file": "10_classic_chinese_dishes.md", "cuisines": ["chinese"], "types": ["main"], "methods": ["stir-fry"], "url": "https://www.recipetineats.com/10-classic-chinese-dishes/"},
]


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def copy_recipe_files():
    """Copy each recipe from recipes/ to by-cuisine/, by-type/, by-method/ subdirectories."""
    recipes_dir = os.path.join(VAULT, "recipes")
    copied = 0
    missing = 0
    for recipe in NEW_RECIPES:
        src = os.path.join(recipes_dir, recipe["file"])
        if not os.path.exists(src):
            print(f"  MISSING: {recipe['file']}")
            missing += 1
            continue
        with open(src, 'r', encoding='utf-8') as f:
            content = f.read()
        # Copy to each cuisine dir
        for cuisine in recipe["cuisines"]:
            dest_dir = os.path.join(VAULT, "by-cuisine", cuisine)
            ensure_dir(dest_dir)
            with open(os.path.join(dest_dir, recipe["file"]), 'w', encoding='utf-8') as f:
                f.write(content)
        # Copy to each type dir
        for rtype in recipe["types"]:
            dest_dir = os.path.join(VAULT, "by-type", rtype)
            ensure_dir(dest_dir)
            with open(os.path.join(dest_dir, recipe["file"]), 'w', encoding='utf-8') as f:
                f.write(content)
        # Copy to each method dir
        for method in recipe["methods"]:
            dest_dir = os.path.join(VAULT, "by-method", method)
            ensure_dir(dest_dir)
            with open(os.path.join(dest_dir, recipe["file"]), 'w', encoding='utf-8') as f:
                f.write(content)
        copied += 1
    print(f"Copied {copied} recipes to subdirectories, {missing} missing")
    return missing == 0


def build_index():
    """Build index.json with all recipes (existing + new)."""
    # Load existing index
    index_path = os.path.join(VAULT, "index.json")
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            index = json.load(f)
    else:
        index = {"generated": "", "total_recipes": 0, "cuisines": {}, "types": {}, "methods": {}, "recipes": []}

    # Mark existing recipes
    existing_files = set(r["file"] for r in index.get("recipes", []))

    # Add new recipes
    for recipe in NEW_RECIPES:
        if recipe["file"] not in existing_files:
            index["recipes"].append({
                "name": recipe["name"],
                "file": f"recipes/{recipe['file']}",
                "cuisines": recipe["cuisines"],
                "types": recipe["types"],
                "methods": recipe["methods"],
                "has_full_content": True,
                "url": recipe["url"]
            })

    # Recalculate totals
    cuisines = {}
    types = {}
    methods = {}
    for r in index["recipes"]:
        for c in r.get("cuisines", []):
            cuisines[c] = cuisines.get(c, 0) + 1
        for t in r.get("types", []):
            types[t] = types.get(t, 0) + 1
        for m in r.get("methods", []):
            methods[m] = methods.get(m, 0) + 1

    index["generated"] = datetime.utcnow().isoformat()
    index["total_recipes"] = len(index["recipes"])
    index["cuisines"] = cuisines
    index["types"] = types
    index["methods"] = methods

    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)

    print(f"Index rebuilt: {index['total_recipes']} total recipes")
    print(f"  Cuisines: {cuisines}")
    print(f"  Types: {types}")
    print(f"  Methods: {methods}")
    return index


if __name__ == "__main__":
    print("=== Recipe Vault Bulk Import ===")
    print("\n1. Copying recipe files to subdirectories...")
    all_copied = copy_recipe_files()
    print("\n2. Building index.json...")
    index = build_index()
    print(f"\nDone! Total recipes in vault: {index['total_recipes']}")
