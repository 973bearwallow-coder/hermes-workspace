#!/usr/bin/env python3
"""
Recipe Vault Builder
Scrapes full recipe content from Mel's Kitchen Cafe URLs
and organizes them into a searchable vault.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

VAULT_DIR = Path.home() / "hermes-workspace" / "projects" / "recipe-vault"
RECIPES_DIR = VAULT_DIR / "recipes"
INDEX_FILE = VAULT_DIR / "index.json"

# Category definitions for classification
CATEGORIES = {
    "cuisine": ["american", "italian", "mexican", "asian", "chinese", "japanese", "thai", "indian", "mediterranean", "greek", "french", "southern", "bbq", "grilled"],
    "type": ["main", "side", "appetizer", "dessert", "breakfast", "soup", "salad", "bread", "snack", "beverage"],
    "method": ["grilled", "baked", "fried", "slow-cooker", "instant-pot", "one-pot", "sheet-pan", "air-fryer", "stovetop", "no-cook", "overnight"],
}

# The 48 Mel's Kitchen Cafe recipes with URLs
MELS_RECIPES = [
    {"name": "Strawberry Spinach Salad with Homemade Poppy Seed Dressing", "url": "https://www.melskitchencafe.com/strawberry-spinach-salad-with-homemade-poppy-seed-dressing/"},
    {"name": "Harvest Apple Salad", "url": "https://www.melskitchencafe.com/harvest-apple-salad/"},
    {"name": "Cinnamon Pull-Apart Bread", "url": "https://www.melskitchencafe.com/cinnamon-pull-apart-bread/"},
    {"name": "Caramel Pecan Sticky Buns", "url": "https://www.melskitchencafe.com/caramel-pecan-sticky-buns/"},
    {"name": "Lemon Chicken Orzo Soup", "url": "https://www.melskitchencafe.com/lemon-chicken-orzo-soup/"},
    {"name": "Raspberry Cream Angel Food Cake Dessert", "url": "https://www.melskitchencafe.com/raspberry-cream-angel-food-cake-dessert/"},
    {"name": "Slow Cooker Posole", "url": "https://www.melskitchencafe.com/slow-cooker-posole/"},
    {"name": "Spinach Salad with Sweet Spicy Nuts Apples Feta and Bacon", "url": "https://www.melskitchencafe.com/spinach-salad-with-sweet-spicy-nuts-apples-feta-and-bacon/"},
    {"name": "Beach Street Lemon Chicken Linguine", "url": "https://www.melskitchencafe.com/beach-street-lemon-chicken-linguine/"},
    {"name": "Cheesy Garlic Drop Biscuits", "url": "https://www.melskitchencafe.com/cheesy-garlic-drop-biscuits/"},
    {"name": "Cranberry Apple Pie", "url": "https://www.melskitchencafe.com/cranberry-apple-pie/"},
    {"name": "Avocado Chicken Salad", "url": "https://www.melskitchencafe.com/avocado-chicken-salad/"},
    {"name": "My Favorite Cherry Pie in the History of Ever", "url": "https://www.melskitchencafe.com/my-favorite-cherry-pie-in-the-history-of-ever/"},
    {"name": "Mexican Street Corn Salad", "url": "https://www.melskitchencafe.com/mexican-street-corn-salad/"},
    {"name": "The Best Spinach Artichoke Dip", "url": "https://www.melskitchencafe.com/the-best-spinach-artichoke-dip/"},
    {"name": "Soft and Chewy Caramel Popcorn", "url": "https://www.melskitchencafe.com/soft-and-chewy-caramel-popcorn/"},
    {"name": "Amazing Shrapnel Dip", "url": "https://www.melskitchencafe.com/amazing-shrapnel-dip/"},
    {"name": "Creamy Cilantro Lime Dressing", "url": "https://www.melskitchencafe.com/creamy-cilantro-lime-dressing/"},
    {"name": "Cheesy Au Gratin Potatoes", "url": "https://www.melskitchencafe.com/cheesy-au-gratin-potatoes-2/"},
    {"name": "White Chocolate Raspberry Truffle Cheesecake", "url": "https://www.melskitchencafe.com/white-chocolate-raspberry-truffle-cheesecake/"},
    {"name": "French Bread", "url": "https://www.melskitchencafe.com/french-bread/"},
    {"name": "Unbelievable Carrot Cake", "url": "https://www.melskitchencafe.com/unbelievable-carrot-cake/"},
    {"name": "Penne with Roasted Asparagus and Balsamic Butter", "url": "https://www.melskitchencafe.com/penne-with-roasted-asparagus-and-balsamic-butter/"},
    {"name": "Honey Lime Fruit Salad", "url": "https://www.melskitchencafe.com/honey-lime-fruit-salad/"},
    {"name": "Overnight Strawberry Cream Cheese Sweet Rolls", "url": "https://www.melskitchencafe.com/overnight-strawberry-cream-cheese-sweet-rolls/"},
    {"name": "Lemon Blueberry Cake with Whipped Lemon Cream Frosting", "url": "https://www.melskitchencafe.com/lemon-blueberry-cake-with-whipped-lemon-cream-frosting/"},
    {"name": "Overnight Cinnamon and Sugar Twists", "url": "https://www.melskitchencafe.com/overnight-cinnamon-and-sugar-twists/"},
    {"name": "Amazing Crustless Pumpkin Pie Cupcakes", "url": "https://www.melskitchencafe.com/amazing-crustless-pumpkin-pie-cupcakes/"},
    {"name": "Peanut Butter Cup Cheesecake with Chocolate Cookie Crust", "url": "https://www.melskitchencafe.com/peanut-butter-cup-cheesecake-with-chocolate-cookie-crust/"},
    {"name": "Amish Style Apple and Cinnamon Baked Oatmeal", "url": "https://www.melskitchencafe.com/amish-style-apple-and-cinnamon-baked-oatmeal/"},
    {"name": "Lemonies", "url": "https://www.melskitchencafe.com/lemonies/"},
    {"name": "Amazing Key Lime Cheesecake", "url": "https://www.melskitchencafe.com/amazing-key-lime-cheesecake/"},
    {"name": "Dark Chocolate Sea Salt Caramel Pretzel Bark Snappers Knock Off", "url": "https://www.melskitchencafe.com/dark-chocolate-sea-salt-caramel-pretzel-bark-snappers-knock-off/"},
    {"name": "Orange Zested Cranberry White Chocolate Bliss Bars", "url": "https://www.melskitchencafe.com/orange-zested-cranberry-white-chocolate-bliss-bars-a-slightly-lighter-version/"},
    {"name": "The Only Pie Crust Recipe Tutorial You'll Ever Need", "url": "https://www.melskitchencafe.com/the-only-pie-crust-recipe-tutorial-youll-ever-need/"},
    {"name": "Perfect Lemon Bars", "url": "https://www.melskitchencafe.com/perfect-lemon-bars/"},
    {"name": "Sweet Baked Ham", "url": "https://www.melskitchencafe.com/sweet-baked-ham-the-most-unique-and-delicious-ham-ive-ever-had/"},
    {"name": "Spaghetti Pie", "url": "https://www.melskitchencafe.com/spaghetti-pie-my-familys-favorite-dinner/"},
    {"name": "The Best Monkey Bread", "url": "https://www.melskitchencafe.com/the-best-monkey-bread/"},
    {"name": "Rustic Crusty Bread", "url": "https://www.melskitchencafe.com/rustic-crusty-bread-a-simple-how-to/"},
    {"name": "Creamy Garlic Alfredo Sauce", "url": "https://www.melskitchencafe.com/creamy-garlic-alfredo-sauce-my-go-to-dinner-saver/"},
    {"name": "Oreo Cheesecake Bites", "url": "https://www.melskitchencafe.com/oreo-cheesecake-bites/"},
    {"name": "Decadent Chocolate Cheesecake", "url": "https://www.melskitchencafe.com/decadent-chocolate-cheesecake/"},
    {"name": "Orange Sweet Rolls", "url": "https://www.melskitchencafe.com/orange-sweet-rolls/"},
    {"name": "Hot Fudge Pudding Cake", "url": "https://www.melskitchencafe.com/hot-fudge-pudding-cake/"},
    {"name": "Sugar Rush 11 My Mom's Famous Caramels", "url": "https://www.melskitchencafe.com/sugar-rush-11-my-moms-famous-caramels/"},
    {"name": "Chopped Greek Chicken Salad", "url": "https://www.melskitchencafe.com/chopped-greek-chicken-salad/"},
]


def setup_vault():
    """Create the vault directory structure."""
    for subdir in ["recipes", "by-cuisine", "by-type", "by-method"]:
        (VAULT_DIR / subdir).mkdir(parents=True, exist_ok=True)
    print(f"✅ Vault structure created at {VAULT_DIR}")


def scrape_recipe(url):
    """Use web_extract to get recipe content from a URL."""
    try:
        result = subprocess.run(
            ["curl", "-s", "-L", "--max-time", "30", url],
            capture_output=True, text=True, timeout=35
        )
        if result.returncode != 0:
            return None
        return result.stdout
    except Exception as e:
        print(f"  ⚠️ Error fetching {url}: {e}")
        return None


def extract_recipe_data(html_content, name, url):
    """Extract structured recipe data from HTML content."""
    if not html_content:
        return None

    # Use Python with regex to extract key parts
    try:
        # Try to find JSON-LD recipe data (common on recipe sites)
        json_ld_match = re.search(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html_content, re.DOTALL)
        if json_ld_match:
            try:
                data = json.loads(json_ld_match.group(1))
                if isinstance(data, list):
                    for item in data:
                        if item.get("@type") == "Recipe" or (isinstance(item.get("@type"), list) and "Recipe" in item["@type"]):
                            data = item
                            break
                    else:
                        data = data[0]
                if data.get("@type") == "Recipe" or (isinstance(data.get("@type"), list) and "Recipe" in data.get("@type", [])):
                    return parse_json_ld_recipe(data, name, url)
            except (json.JSONDecodeError, KeyError, IndexError):
                pass

        # Fallback: extract from HTML title and meta description
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.DOTALL)
        title = title_match.group(1).strip() if title_match else name
        # Clean HTML tags
        title = re.sub(r'<[^>]+>', '', title).strip()

        desc_match = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', html_content)
        description = desc_match.group(1) if desc_match else ""

        return {
            "name": title,
            "url": url,
            "description": description,
            "source": "Mel's Kitchen Cafe",
            "has_full_content": False,
            "raw_length": len(html_content),
        }
    except Exception as e:
        print(f"  ⚠️ Error parsing {name}: {e}")
        return None


def parse_json_ld_recipe(data, fallback_name, url):
    """Parse a JSON-LD Recipe object into our format."""
    name = data.get("name", fallback_name)
    description = data.get("description", "")
    recipe_ingredient = data.get("recipeIngredient", [])
    recipe_instructions = data.get("recipeInstructions", [])

    # Handle instructions - they can be strings or objects with "text" field
    instructions = []
    for step in recipe_instructions:
        if isinstance(step, str):
            instructions.append(step)
        elif isinstance(step, dict):
            text = step.get("text", step.get("name", ""))
            if text:
                instructions.append(text)

    # Extract times
    prep_time = data.get("prepTime", "")
    cook_time = data.get("cookTime", "")
    total_time = data.get("totalTime", "")

    # Extract cuisine
    cuisine = data.get("recipeCuisine", "")
    if isinstance(cuisine, list):
        cuisine = cuisine[0] if cuisine else ""

    # Extract category
    category = data.get("recipeCategory", "")
    if isinstance(category, list):
        category = category[0] if category else ""

    # Extract keywords/tags
    keywords = data.get("keywords", "")
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",")]

    # Extract image
    image = data.get("image", "")
    if isinstance(image, list):
        image = image[0] if image else ""
    if isinstance(image, dict):
        image = image.get("url", "")

    # Extract yield/servings
    yield_val = data.get("recipeYield", data.get("yield", ""))

    has_full = bool(recipe_ingredient and instructions)

    return {
        "name": name,
        "url": url,
        "description": description,
        "source": "Mel's Kitchen Cafe",
        "cuisine": cuisine,
        "category": category,
        "prep_time": prep_time,
        "cook_time": cook_time,
        "total_time": total_time,
        "yield": str(yield_val) if yield_val else "",
        "ingredients": recipe_ingredient,
        "instructions": instructions,
        "keywords": keywords,
        "image": image if isinstance(image, str) else "",
        "has_full_content": has_full,
    }


def classify_recipe(recipe):
    """Auto-classify a recipe by cuisine, type, and method."""
    text = " ".join([
        recipe.get("name", ""),
        recipe.get("description", ""),
        recipe.get("category", ""),
        " ".join(recipe.get("keywords", [])),
        " ".join(recipe.get("ingredients", [])[:5]),
    ]).lower()

    cuisines = []
    for kw in CATEGORIES["cuisine"]:
        if kw in text:
            cuisines.append(kw)

    types = []
    for kw in CATEGORIES["type"]:
        if kw in text:
            types.append(kw)

    methods = []
    for kw in CATEGORIES["method"]:
        if kw in text:
            methods.append(kw)

    # Default classifications
    if not cuisines:
        cuisines = ["american"]
    if not types:
        types = ["main"]
    if not methods:
        methods = ["stovetop"]

    return cuisines, types, methods


def save_recipe(recipe):
    """Save a recipe as a markdown file and update the index."""
    cuisines, types, methods = classify_recipe(recipe)

    # Create safe filename
    safe_name = re.sub(r'[^\w\s-]', '', recipe["name"]).strip().replace(' ', '_').lower()
    safe_name = safe_name[:60]  # Limit length

    # Build markdown content
    md_lines = [f"# {recipe['name']}", ""]
    md_lines.append(f"**Source:** [Mel's Kitchen Cafe]({recipe['url']})")
    md_lines.append(f"**Cuisine:** {', '.join(cuisines).title()}")
    md_lines.append(f"**Type:** {', '.join(types).title()}")
    md_lines.append(f"**Method:** {', '.join(methods).title()}")

    if recipe.get("prep_time"):
        md_lines.append(f"**Prep Time:** {recipe['prep_time']}")
    if recipe.get("cook_time"):
        md_lines.append(f"**Cook Time:** {recipe['cook_time']}")
    if recipe.get("total_time"):
        md_lines.append(f"**Total Time:** {recipe['total_time']}")
    if recipe.get("yield"):
        md_lines.append(f"**Yield:** {recipe['yield']}")

    md_lines.append("")

    if recipe.get("description"):
        md_lines.append(f"## Description")
        md_lines.append("")
        md_lines.append(recipe["description"])
        md_lines.append("")

    if recipe.get("ingredients"):
        md_lines.append("## Ingredients")
        md_lines.append("")
        for ing in recipe["ingredients"]:
            md_lines.append(f"- {ing}")
        md_lines.append("")

    if recipe.get("instructions"):
        md_lines.append("## Instructions")
        md_lines.append("")
        for i, step in enumerate(recipe["instructions"], 1):
            md_lines.append(f"{i}. {step}")
        md_lines.append("")

    if recipe.get("keywords"):
        md_lines.append(f"**Keywords:** {', '.join(recipe['keywords'])}")
        md_lines.append("")

    # Save to main recipes directory
    recipe_file = RECIPES_DIR / f"{safe_name}.md"
    recipe_file.write_text("\n".join(md_lines))

    # Create symlinks/copies in category directories
    for cuisine in cuisines:
        cuisine_dir = VAULT_DIR / "by-cuisine" / cuisine.lower()
        cuisine_dir.mkdir(parents=True, exist_ok=True)
        (cuisine_dir / f"{safe_name}.md").write_text("\n".join(md_lines))

    for dish_type in types:
        type_dir = VAULT_DIR / "by-type" / dish_type.lower()
        type_dir.mkdir(parents=True, exist_ok=True)
        (type_dir / f"{safe_name}.md").write_text("\n".join(md_lines))

    for method in methods:
        method_dir = VAULT_DIR / "by-method" / method.lower()
        method_dir.mkdir(parents=True, exist_ok=True)
        (method_dir / f"{safe_name}.md").write_text("\n".join(md_lines))

    return {
        "name": recipe["name"],
        "file": str(recipe_file.relative_to(VAULT_DIR)),
        "cuisines": cuisines,
        "types": types,
        "methods": methods,
        "has_full_content": recipe.get("has_full_content", False),
        "url": recipe["url"],
    }


def build_index(entries):
    """Build the searchable index."""
    index = {
        "generated": datetime.now().isoformat(),
        "total_recipes": len(entries),
        "cuisines": {},
        "types": {},
        "methods": {},
        "recipes": entries,
    }

    for entry in entries:
        for c in entry["cuisines"]:
            index["cuisines"][c] = index["cuisines"].get(c, 0) + 1
        for t in entry["types"]:
            index["types"][t] = index["types"].get(t, 0) + 1
        for m in entry["methods"]:
            index["methods"][m] = index["methods"].get(m, 0) + 1

    INDEX_FILE.write_text(json.dumps(index, indent=2))
    print(f"\n📋 Index saved to {INDEX_FILE}")
    print(f"   Cuisines: {dict(sorted(index['cuisines'].items()))}")
    print(f"   Types: {dict(sorted(index['types'].items()))}")
    print(f"   Methods: {dict(sorted(index['methods'].items()))}")


def main():
    setup_vault()

    print(f"\n🔍 Scraping {len(MELS_RECIPES)} recipes from Mel's Kitchen Cafe...")
    print("(This will take a few minutes)\n")

    entries = []
    for i, recipe_info in enumerate(MELS_RECIPES, 1):
        name = recipe_info["name"]
        url = recipe_info["url"]
        print(f"[{i:2d}/{len(MELS_RECIPES)}] {name[:50]}...")

        html = scrape_recipe(url)
        if html:
            recipe = extract_recipe_data(html, name, url)
            if recipe:
                entry = save_recipe(recipe)
                entries.append(entry)
                status = "✅" if recipe.get("has_full_content") else "⚠️ (partial)"
                print(f"  {status} → {entry['file']}")
            else:
                print(f"  ❌ Failed to parse")
        else:
            print(f"  ❌ Failed to fetch")

    build_index(entries)

    full_count = sum(1 for e in entries if e["has_full_content"])
    print(f"\n{'='*60}")
    print(f"📊 VAULT SUMMARY")
    print(f"{'='*60}")
    print(f"Total recipes: {len(entries)}")
    print(f"Full content: {full_count}")
    print(f"Partial/title only: {len(entries) - full_count}")
    print(f"Vault location: {VAULT_DIR}")
    print(f"\nSearch by:")
    print(f"  Cuisine: {VAULT_DIR / 'by-cuisine'}")
    print(f"  Type:    {VAULT_DIR / 'by-type'}")
    print(f"  Method:  {VAULT_DIR / 'by-method'}")
    print(f"  Index:   {INDEX_FILE}")


if __name__ == "__main__":
    main()
