#!/usr/bin/env python3
"""recipe_query.py — callable recipe interface for Atlas (Tom's food efficiency system).

Usage:
  recipe_query.py "asian chicken dinner 3 people"
  recipe_query.py --ingredient ground_beef --cuisine italian --meal dinner
  recipe_query.py --sale pork --count 5   (diverse meal plan)

Output: JSON to stdout (Atlas reads this and replies to Tom in natural language).
"""
import json, re, sys, argparse
from pathlib import Path

BASE = Path("/home/tom/hermes-workspace/projects/recipe-vault")
INDEX = json.load(open(BASE / "index.json"))
ING = json.load(open(BASE / "ingredient-index.json"))
RECIPES = INDEX["recipes"]

CLEAN_CUISINES = sorted({c.lower() for r in RECIPES for c in r.get("cuisines", [])})
MEAL_MAP = {
    "breakfast": ["breakfast", "brunch"],
    "brunch": ["breakfast", "brunch"],
    "lunch": ["lunch", "main"],
    "dinner": ["main", "dinner"],
    "dessert": ["dessert"],
    "salad": ["salad"],
    "soup": ["soup"],
}
# regional aliases -> specific cuisines in vault
REGION_MAP = {
    "asian": ["chinese", "thai", "vietnamese", "japanese", "korean", "indian"],
    "oriental": ["chinese", "thai", "vietnamese", "japanese", "korean"],
    "european": ["italian", "french", "greek", "spanish", "german", "mediterranean"],
    "latin": ["mexican", "spanish", "caribbean"],
}

def clean_cuisine(c):
    return c.split("|")[0].strip()

def parse_nl(text):
    text_l = text.lower()
    cuisine = next((c for c in CLEAN_CUISINES if c in text_l), None)
    if not cuisine:
        for region, cuis in REGION_MAP.items():
            if region in text_l:
                cuisine = cuis  # list of cuisines
                break
    meal = next((m for m in MEAL_MAP if m in text_l), None)
    # ingredient extraction — find user words that map to ANY index key
    found = []
    tokens = re.findall(r"[a-z]+", text_l)
    for t in tokens:
        if len(t) < 3:
            continue
        if t in ("the", "and", "for", "with", "some", "people", "servings", "dinner",
                 "lunch", "breakfast", "asian", "european", "latino", "oriental"):
            continue
        # does this token appear in any ingredient key? (e.g. 'chicken' in 'bone-in chicken thighs')
        hits = [k for k in ING if t in k.lower()]
        if hits and t not in found:
            found.append(t)  # store the clean user word, not the key
    # servings
    serv = None
    m = re.search(r"(\d+)\s*(people|servings|portions)", text_l)
    if m:
        serv = int(m.group(1))
    return cuisine, meal, found, serv

def recommend(cuisine, meal, ingredients, max_missing=0):
    types = MEAL_MAP.get(meal, []) if meal else []
    cuisines = cuisine if isinstance(cuisine, list) else ([cuisine] if cuisine else [])
    ing_set = set(ingredients)
    results = []
    for r in RECIPES:
        rc = [clean_cuisine(c) for c in r.get("cuisines", [])]
        if cuisines and not (set(rc) & set(cuisines)):
            continue
        if types and not (set(r.get("types", [])) & set(types)):
            continue
        matched, missing = [], []
        if ing_set:
            for ing in ing_set:
                # fuzzy: does this recipe have ANY ingredient key containing `ing`?
                found_for_ing = False
                for key, recipes in ING.items():
                    if ing in key and r["name"] in recipes:
                        found_for_ing = True
                        break
                if found_for_ing:
                    matched.append(ing)
                else:
                    missing.append(ing)
            if missing:
                missing = list(ing_set - set(matched))
            total = len(ing_set)
            have = len(matched)
            pct = round(have / total * 100)
            if missing and len(missing) > max_missing:
                continue
        else:
            pct = 100
        results.append({
            "name": r["name"],
            "cuisine": rc[0] if rc else "unknown",
            "url": r.get("url", ""),
            "match_pct": pct,
            "has_ingredients": matched,
            "missing_ingredients": missing,
        })
    results.sort(key=lambda x: x["match_pct"], reverse=True)
    return results

def diverse_plan(protein, count=5):
    """Pick N recipes with `protein` that are diverse in cuisine + method."""
    # fuzzy: any recipe whose ingredient keys contain `protein`
    protein_recipes = set()
    for key, recipes in ING.items():
        if protein in key.lower():
            protein_recipes.update(recipes)
    cands = [r for r in RECIPES if r["name"] in protein_recipes]
    picked = []
    used_cuisine = set()
    used_method = set()
    for r in sorted(cands, key=lambda x: len(x.get("cuisines", [])), reverse=True):
        rc = r.get("cuisines", ["unknown"])[0]
        rm = r.get("methods", ["unknown"])[0]
        # enforce diversity: don't repeat cuisine+method combo
        if (rc, rm) in {(c, m) for c in used_cuisine for m in used_method}:
            continue
        picked.append(r)
        used_cuisine.add(rc)
        used_method.add(rm)
        if len(picked) >= count:
            break
    return picked

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="*")
    ap.add_argument("--ingredient", action="append", default=[])
    ap.add_argument("--cuisine", default="")
    ap.add_argument("--meal", default="")
    ap.add_argument("--sale", default="", help="protein on sale -> diverse meal plan")
    ap.add_argument("--count", type=int, default=5)
    ap.add_argument("--max-missing", type=int, default=0)
    args = ap.parse_args()

    if args.sale:
        plan = diverse_plan(args.sale, args.count)
        out = {
            "mode": "sale_plan",
            "protein": args.sale,
            "count": len(plan),
            "recipes": [{
                "name": r["name"], "cuisine": clean_cuisine(r.get("cuisines", ["?"])[0]),
                "method": r.get("methods", ["?"])[0], "url": r.get("url", "")
            } for r in plan],
        }
        print(json.dumps(out, indent=1))
        return

    if args.query:
        text = " ".join(args.query)
        cuisine, meal, ings, serv = parse_nl(text)
    else:
        cuisine, meal, ings = args.cuisine, args.meal, args.ingredient

    results = recommend(cuisine, meal, ings, args.max_missing)
    out = {
        "mode": "recommend",
        "parsed": {"cuisine": cuisine, "meal": meal, "ingredients": ings, "servings": serv},
        "count": len(results),
        "recipes": results[:10],
    }
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
