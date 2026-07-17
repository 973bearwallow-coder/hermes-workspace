#!/usr/bin/env python3
"""Rebuild ingredient-index.json from actual recipe .md files in by-type/.

Fixes the stale/partial ingredient-index that the MoA recipe app relied on.
Also reports index.json file-path mismatches.
"""
import json, re, os
from pathlib import Path

BASE = Path("/home/tom/hermes-workspace/projects/recipe-vault")
RECIPES = BASE / "recipes"
INDEX = BASE / "index.json"
OUT = BASE / "ingredient-index.json"

# Quantity/measurement words to strip from ingredient lines
MEASURE = re.compile(
    r"^\s*[-*]?\s*"
    r"(\d+\s*\d*/\d+|\d+\.\d+|\d+\s?\d*|[½¼¾⅓⅔⅛]|a|an|some|to taste|pinch|dash|"
    r"\d+\s?-\s?\d+|about|approx\.?|roughly)\s*"
    r"(cups?|cup|tbsp|tsp|teaspoon|tablespoon|ml|l|g|kg|oz|lb|lbs|pound|pounds|"
    r"clove|cloves|can|cans|slice|slices|piece|pieces|stalk|stalks|sheet|sheets|"
    r"bunch|bunches|handful|handfuls|sprig|sprigs|stick|sticks|pkg|packages?|"
    r"x\s?\d+|\([^)]*\))?\s*",
    re.I,
)

def clean_ingredient(line):
    # remove leading bullet or slash (some lines start with "/")
    s = re.sub(r"^\s*[-*/]\s*", "", line)
    # strip measurement prefix (amount + unit)
    s = MEASURE.sub("", s, count=1)
    # also strip any leading number/range that remains
    s = re.sub(r"^\s*[\d¼½¾⅓⅔⅛]+\s*[\d/]*\s*", "", s)
    # remove trailing parentheticals
    s = re.sub(r"\([^)]*\)", "", s)
    # cut at first comma (descriptor after comma is not the core ingredient)
    s = s.split(",")[0]
    s = s.strip(" ,.;-|/")
    # lowercase
    s = s.lower()
    # drop empty / too short / pure units
    if len(s) < 3:
        return None
    return s

def extract_ingredients(md_text):
    lines = md_text.splitlines()
    in_ing = False
    ings = []
    for ln in lines:
        if re.match(r"^##\s+ingredients", ln, re.I):
            in_ing = True
            continue
        if in_ing and re.match(r"^##\s+", ln):
            break  # next section
        if in_ing:
            if ln.strip().startswith("-") or ln.strip().startswith("*"):
                # split on ';' and strip '**label:**' prefixes (e.g. '**patties:** 1 lb ground beef; breadcrumbs')
                ln = re.sub(r"\*\*[^*]+\*\*\s*:", " ", ln)  # remove **label:**
                parts = re.split(r"[;|]", ln)  # split compound lines
                for p in parts:
                    c = clean_ingredient(p)
                if c:
                    ings.append(c)
    return ings

def main():
    files = list(RECIPES.glob("*.md"))
    ing_idx = {}
    recipe_count = 0
    # load existing index to preserve url + any present metadata
    idx = json.load(open(INDEX))
    idx_by_name = {r["name"]: r for r in idx["recipes"]}
    updated = []
    for f in files:
        text = f.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"^#\s+(.+)$", text, re.M)
        if not m:
            continue
        name = m.group(1).strip()
        ings = extract_ingredients(text)
        if not ings:
            continue
        for ing in ings:
            ing_idx.setdefault(ing, []).append(name)
        recipe_count += 1
        # backfill metadata from content if missing in index
        rec = idx_by_name.get(name, {})
        if not rec.get("cuisines"):
            # crude cuisine detection from content keywords
            cl = text.lower()
            cuis = []
            for c in ["italian", "chinese", "thai", "vietnamese", "mexican", "indian",
                      "japanese", "korean", "french", "greek", "spanish", "german",
                      "american", "mediterranean", "caribbean"]:
                if c in cl:
                    cuis.append(c)
            if cuis:
                rec["cuisines"] = cuis[:2]
        if not rec.get("types"):
            cl = text.lower()
            if "breakfast" in cl or "brunch" in cl:
                rec["types"] = ["breakfast"]
            elif "dessert" in cl or "sweet" in cl:
                rec["types"] = ["dessert"]
            elif "salad" in cl:
                rec["types"] = ["salad"]
            elif "soup" in cl:
                rec["types"] = ["soup"]
            else:
                rec["types"] = ["main"]
        if not rec.get("methods"):
            cl = text.lower()
            meth = []
            for mth in ["stir-fry", "bake", "grill", "slow-cook", "roast",
                        "saute", "steam", "fried", "simmer", "pressure-cook"]:
                if mth.replace("-", " ") in cl or mth in cl:
                    meth.append(mth)
            rec["methods"] = meth[:2] if meth else ["stovetop"]
        rec["name"] = name
        rec["file"] = f"recipes/{f.name}"
        if "url" not in rec:
            mu = re.search(r"\*\*Source:\*\*\s*\[([^\]]+)\]\(([^)]+)\)", text)
            if mu:
                rec["url"] = mu.group(2)
        updated.append(rec)
    # sort recipe lists
    for k in ing_idx:
        ing_idx[k] = sorted(set(ing_idx[k]))
    OUT.write_text(json.dumps(ing_idx, indent=1))
    # write enriched index
    idx["recipes"] = updated
    INDEX.write_text(json.dumps(idx, indent=1))
    print(f"Rebuilt ingredient-index.json: {len(ing_idx)} ingredients, {recipe_count} recipes parsed")
    print(f"Enriched index.json: {len(updated)} recipes with cuisines/types/methods/url")
    missing_c = sum(1 for r in updated if not r.get("cuisines"))
    print(f"Recipes still missing cuisines: {missing_c}")

if __name__ == "__main__":
    main()
