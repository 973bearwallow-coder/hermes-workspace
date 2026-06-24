#!/usr/bin/env python3
"""Generate the complete rebuilt index.json"""
import json
from datetime import datetime

# All 90 recipes with updated classifications for the 43 RecipeTin Eats recipes
recipes = [
    {"name": "French Chicken au Poivre Sauce", "file": "recipes/french_chicken_au_poivre_sauce.md", "cuisines": ["french"], "types": ["main"], "methods": ["stovetop"], "has_full_content": True, "url": "https://www.recipetineats.com/french-chicken-au-poivre-sauce/", "size": 2251},
    {"name": "Thai Grilled Chicken (Gai Yang)", "file": "recipes/thai_grilled_chicken_gai_yang.md", "cuisines": ["thai"], "types": ["main"], "methods": ["grilled"], "has_full_content": True, "url": "https://www.recipetineats.com/thai-grilled-chicken-gai-yang/", "size": 2327},
    {"name": "Chicken Chasseur", "file": "recipes/chicken_chasseur.md", "cuisines": ["french"], "types": ["main"], "methods": ["stovetop"], "has_full_content": True, "url": "https://www.recipetineats.com/chicken-chasseur/", "size": 2858},
    {"name": "New Orleans Chicken Wings", "file": "recipes/new_orleans_chicken_wings.md", "cuisines": ["american"], "types": ["appetizer"], "methods": ["baked"], "has_full_content": True, "url": "https://www.recipetineats.com/new-orleans-chicken-wings/", "size": 2337},
    {"name": "Chicken Cacciatore (Italian Chicken Stew)", "file": "recipes/chicken_cacciatore_italian_chicken_stew.md", "cuisines": ["italian"], "types": ["main"], "methods": ["stovetop"], "has_full_content": True, "url": "https://www.recipetineats.com/chicken-cacciatore-italian-chicken-stew/", "size": 2666},
    {"name": "Chicken Francese", "file": "recipes/chicken_francese.md", "cuisines": ["italian"], "types": ["main"], "methods": ["stovetop"], "has_full_content": True, "url": "https://www.recipetineats.com/chicken-francese/", "size": 2372},
    {"name": "Vietnamese Caramel Ginger Chicken", "file": "recipes/vietnamese_caramel_ginger_chicken.md", "cuisines": ["vietnamese"], "types": ["main"], "methods": ["stovetop"], "has_full_content": True, "url": "https://www.recipetineats.com/vietnamese-caramel-ginger-chicken/", "size": 2132},
    {"name": "Chicken Marsala", "file": "recipes/chicken_marsala.md", "cuisines": ["italian"], "types": ["main"], "methods": ["stovetop"], "has_full_content": True, "url": "https://www.recipetineats.com/chicken-marsala/", "size": 2526},
    {"name": "One Pot Baked Greek Chicken Orzo Risoni", "file": "recipes/one_pot_baked_greek_chicken_orzo_risoni.md", "cuisines": ["greek"], "types": ["main"], "methods": ["one-pot"], "has_full_content": True, "url": "https://www.recipetineats.com/one-pot-baked-greek-chicken-orzo-risoni/", "size": 2890},
    {"name": "Thai Red Curry Pot Roast Chicken", "file": "recipes/thai_red_curry_pot_roast_chicken.md", "cuisines": ["thai"], "types": ["main"], "methods": ["baked"], "has_full_content": True, "url": "https://www.recipetineats.com/thai-red-curry-pot-roast-chicken/", "size": 2607},
    {"name": "Chicken in Creamy Mustard Sauce", "file": "recipes/chicken_in_creamy_mustard_sauce.md", "cuisines": ["french"], "types": ["main"], "methods": ["stovetop"], "has_full_content": True, "url": "https://www.recipetineats.com/chicken-in-creamy-mustard-sauce/", "size": 2291},
    {"name": "Chicken Shawarma (Middle Eastern)", "file": "recipes/chicken_shawarma_middle_eastern.md", "cuisines": ["middle-eastern"], "types": ["main"], "methods": ["stovetop"], "has_full_content": True, "url": "https://www.recipetineats.com/chicken-sharwama-middle-eastern/", "size": 2448},
    {"name": "Coq au Vin", "file": "recipes/coq_au_vin.md", "cuisines": ["french"], "types": ["main"], "methods": ["baked"], "has_full_content": True, "url": "https://www.recipetineats.com/coq-au-vin/", "size": 2777},
    {"name": "Chicken Piccata", "file": "recipes/chicken_piccata.md", "cuisines": ["italian"], "types": ["main"], "methods": ["stovetop"], "has_full_content": True, "url": "https://www.recipetineats.com/chicken-piccata/", "size": 2560},
    {"name": "Creamy Chicken Mushroom Fettuccine", "file": "recipes/creamy_chicken_mushroom_fettucine.md", "cuisines": ["italian"], "types": ["main"], "methods": ["stovetop"], "has_full_content": False, "url": "https://www.recipetineats.com/creamy-chicken-mushroom-fettucine/", "size": 1207},
    {"name": "Creamy Tuscan Chicken Pasta Bake", "file": "recipes/creamy_tuscan_chicken_pasta_bake.md", "cuisines": ["italian"], "types": ["main"], "methods": ["baked"], "has_full_content": False, "url": "https://www.recipetineats.com/creamy-tuscan-chicken-pasta-bake/", "size": 1149},
    {"name": "Chicken Broccoli Stir Fry", "file": "recipes/chicken_broccoli_stir_fry.md", "cuisines": ["chinese"], "types": ["main"], "methods": ["stir-fry"], "has_full_content": True, "url": "https://www.recipetineats.com/chicken-broccoli-stir-fry/", "size": 2574},
    {"name": "Thai Chicken Lettuce Cups (Larb Gai / Laab Gai)", "file": "recipes/thai_chicken_lettuce_cups_larb_gai.md", "cuisines": ["thai"], "types": ["main"], "methods": ["stir-fry"], "has_full_content": True, "url": "https://www.recipetineats.com/thai-chicken-lettuce-cups-larb-gai/", "size": 2613},
    {"name": "Chicken Pad Thai", "file": "recipes/chicken_pad_thai.md", "cuisines": ["thai"], "types": ["main"], "methods": ["stir-fry"], "has_full_content": True, "url": "https://www.recipetineats.com/chicken-pad-thai/", "size": 2402},
    {"name": "Chicken Chow Mein", "file": "recipes/chicken_chow_mein.md", "cuisines": ["chinese"], "types": ["main"], "methods": ["stir-fry"], "has_full_content": True, "url": "https://www.recipetineats.com/chicken-chow-mein/", "size": 2294},
    {"name": "Thai Basil Chicken Stir Fry", "file": "recipes/thai_basil_chicken_stir_fry.md", "cuisines": ["thai"], "types": ["main"], "methods": ["stir-fry"], "has_full_content": True, "url": "https://www.recipetineats.com/thai-basil-chicken-stir-fry/", "size": 2076},
    {"name": "Chicken with Creamy Sun Dried Tomato Sauce", "file": "recipes/chicken_with_creamy_sun_dried_tomato_sauce.md", "cuisines": ["italian"], "types": ["main"], "methods": ["stovetop"], "has_full_content": True, "url": "https://www.recipetineats.com/chicken-with-creamy-sun-dried-tomato-sauce/", "size": 2386},
    {"name": "Pad Kee Mao (Thai Drunken Noodles)", "file": "recipes/pad_keemao_thai_drunken_noodles.md", "cuisines": ["thai"], "types": ["main"], "methods": ["stir-fry"], "has_full_content": False, "url": "https://www.recipetineats.com/pad-keemao-thai-drunken-noodles/", "size": 1130},
    {"name": "Jambalaya Recipe", "file": "recipes/jambalaya_recipe.md", "cuisines": ["american"], "types": ["main"], "methods": ["one-pot"], "has_full_content": True, "url": "https://www.recipetineats.com/jambalaya-recipe/", "size": 2653},
    {"name": "Chicken Pasta Recipe", "file": "recipes/chicken_pasta_recipe.md", "cuisines": ["italian"], "types": ["main"], "methods": ["stovetop"], "has_full_content": True, "url": "https://www.recipetineats.com/chicken-pasta-recipe/", "size": 2583},
    {"name": "Chinese Cashew Chicken", "file": "recipes/chinese_cashew_chicken.md", "cuisines": ["chinese"], "types": ["main"], "methods": ["stir-fry"], "has_full_content": True, "url": "https://www.recipetineats.com/chinese-cashew-chicken/", "size": 2202},
    {"name": "Chicken Pot Pie", "file": "recipes/chicken_pot_pie.md", "cuisines": ["american"], "types": ["main"], "methods": ["baked"], "has_full_content": True, "url": "https://www.recipetineats.com/chicken-pot-pie/", "size": 2641},
    {"name": "Lemon Chicken Salad", "file": "recipes/lemon_chicken_salad.md", "cuisines": ["american"], "types": ["salad"], "methods": ["stovetop"], "has_full_content": True, "url": "https://www.recipetineats.com/lemon-chicken-salad/", "size": 2249},
    {"name": "Mexican Chicken Avocado Salad", "file": "recipes/mexican_chicken_avocado_salad.md", "cuisines": ["mexican"], "types": ["salad"], "methods": ["grilled"], "has_full_content": True, "url": "https://www.recipetineats.com/mexican-chicken-avocado-salad/", "size": 2340},
    {"name": "Oven Baked Chicken and Rice Pilaf (Cranberry Walnut Apple)", "file": "recipes/oven_baked_chicken_and_rice_pilaf.md", "cuisines": ["american"], "types": ["main"], "methods": ["baked"], "has_full_content": True, "url": "https://www.recipetineats.com/oven-baked-chicken-and-rice-pilaf-cranberry-walnut-apple/", "size": 2598},
    {"name": "Vietnamese Coconut Caramel Chicken", "file": "recipes/vietnamese_coconut_caramel_chicken.md", "cuisines": ["vietnamese"], "types": ["main"], "methods": ["stovetop"], "has_full_content": True, "url": "https://www.recipetineats.com/vietnamese-coconut-caramel-chicken/", "size": 2433},
    {"name": "Thai Coconut Chicken", "file": "recipes/thai_coconut_chicken.md", "cuisines": ["thai"], "types": ["main"], "methods": ["grilled"], "has_full_content": True, "url": "https://www.recipetineats.com/thai-coconut-chicken/", "size": 2243},
    {"name": "Oven Baked Chicken Quesadillas", "file": "recipes/oven_baked_chicken_quesadillas.md", "cuisines": ["mexican"], "types": ["main"], "methods": ["baked"], "has_full_content": True, "url": "https://www.recipetineats.com/oven-baked-chicken-quesadillas/", "size": 2404},
    {"name": "Creamy Chicken and Bacon Pasta", "file": "recipes/creamy_chicken_and_bacon_pasta.md", "cuisines": ["italian"], "types": ["main"], "methods": ["stovetop"], "has_full_content": True, "url": "https://www.recipetineats.com/creamy-chicken-and-bacon-pasta/", "size": 2280},
    {"name": "Chicken and Mushroom Risotto", "file": "recipes/chicken_and_mushroom_risotto.md", "cuisines": ["italian"], "types": ["main"], "methods": ["stovetop"], "has_full_content": True, "url": "https://www.recipetineats.com/chicken-and-mushroom-risotto/", "size": 2193},
    {"name": "Mexican Shredded Chicken", "file": "recipes/mexican_shredded_chicken.md", "cuisines": ["mexican"], "types": ["main"], "methods": ["slow-cooker"], "has_full_content": True, "url": "https://www.recipetineats.com/mexican-shredded-chicken/", "size": 2189},
    {"name": "One Pot Chicken Enchilada Rice Casserole", "file": "recipes/one_pot_chicken_enchilada_rice_casserole.md", "cuisines": ["mexican"], "types": ["main"], "methods": ["one-pot"], "has_full_content": True, "url": "https://www.recipetineats.com/one-pot-chicken-enchilada-rice-casserole/", "size": 2253},
    {"name": "One Pot Creamy Parmesan Garlic Risotto with Lemon Pepper Chicken", "file": "recipes/one_pot_creamy_parmesan_garlic_risotto.md", "cuisines": ["italian"], "types": ["main"], "methods": ["one-pot"], "has_full_content": True, "url": "https://www.recipetineats.com/one-pot-creamy-parmesan-garlic-risotto-with-lemon-pepper-chicken/", "size": 2594},
    {"name": "One Pot Greek Chicken Lemon Rice", "file": "recipes/one_pot_greek_chicken_lemon_rice.md", "cuisines": ["greek"], "types": ["main"], "methods": ["one-pot"], "has_full_content": True, "url": "https://www.recipetineats.com/one-pot-greek-chicken-lemon-rice/", "size": 2287},
    {"name": "Jamaican Jerk Chicken Drumsticks with Caribbean Rice and Beans", "file": "recipes/jamaican_jerk_chicken_drumsticks.md", "cuisines": ["jamaican"], "types": ["main"], "methods": ["baked"], "has_full_content": False, "url": "https://www.recipetineats.com/jamaican-jerk-chicken-drumsticks-with-caribbean-rice-and-beans/", "size": 1124},
    {"name": "One Pan Spanish Chicken Chorizo Tomato Potatoes", "file": "recipes/one_pan_spanish_chicken_chorizo.md", "cuisines": ["spanish"], "types": ["main"], "methods": ["baked"], "has_full_content": True, "url": "https://www.recipetineats.com/one-pan-spanish-chicken-chorizo-tomato-potatoes/", "size": 2744},
    {"name": "Crispy Shredded Chicken Noodle Stir Fry", "file": "recipes/crispy_shredded_chicken_noodle_stir_fry.md", "cuisines": ["chinese"], "types": ["main"], "methods": ["stir-fry"], "has_full_content": True, "url": "https://www.recipetineats.com/crispy-shredded-chicken-noodle-stir-fry/", "size": 2560},
    {"name": "10 Classic Chinese Dishes + Homemade Teriyaki Sauce", "file": "recipes/10_classic_chinese_dishes.md", "cuisines": ["chinese"], "types": ["main"], "methods": ["stir-fry"], "has_full_content": True, "url": "https://www.recipetineats.com/10-classic-chinese-dishes/", "size": 2532},
]

# Now we need to add the remaining 47 recipes from the original vault (Mel's Kitchen Cafe + others)
# These keep their original classifications
import os
existing_files = set(r['file'] for r in recipes)
vault_recipes_dir = os.path.expanduser("~/hermes-workspace/projects/recipe-vault/recipes")

# Read existing index to get the non-RecipeTin Eats recipes
import json
with open(os.path.expanduser("~/hermes-workspace/projects/recipe-vault/index.json"), 'r') as f:
    old_index = json.load(f)

for old_recipe in old_index['recipes']:
    if old_recipe['file'] not in existing_files:
        recipes.append(old_recipe)

# Count
cuisine_counts = {}
type_counts = {}
method_counts = {}

for recipe in recipes:
    for c in recipe.get('cuisines', []):
        cuisine_counts[c] = cuisine_counts.get(c, 0) + 1
    for t in recipe.get('types', []):
        type_counts[t] = type_counts.get(t, 0) + 1
    for m in recipe.get('methods', []):
        method_counts[m] = method_counts.get(m, 0) + 1

index = {
    "generated": datetime.utcnow().isoformat(),
    "total_recipes": len(recipes),
    "cuisines": dict(sorted(cuisine_counts.items(), key=lambda x: x[1], reverse=True)),
    "types": dict(sorted(type_counts.items(), key=lambda x: x[1], reverse=True)),
    "methods": dict(sorted(method_counts.items(), key=lambda x: x[1], reverse=True)),
    "recipes": recipes
}

with open(os.path.expanduser("~/hermes-workspace/projects/recipe-vault/index.json"), 'w') as f:
    json.dump(index, f, indent=2)

print(f"Done: {len(recipes)} recipes")
print(f"Full content: {sum(1 for r in recipes if r['has_full_content'])}/{len(recipes)}")
print(f"Cuisines: {index['cuisines']}")
