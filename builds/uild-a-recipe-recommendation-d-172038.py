#!/usr/bin/env python3
# Recipe Recommendation Dashboard (Flask, stdlib + flask only)
# Reads existing index.json + ingredient-index.json (READ ONLY, never modified)
# v2 (deferred): live grocery price comparison, least-stops optimization, serving-size scaling

import json
import os
import re
import difflib
from flask import Flask, request, render_template_string

BASE = "/home/tom/hermes-workspace/projects/recipe-vault"
INDEX = os.path.join(BASE, "index.json")
ING = os.path.join(BASE, "ingredient-index.json")

# Known non-cuisine words to exclude from cuisine dropdown
NON_CUISINE = {
    "appetizer", "main", "side dish", "salad", "dessert", "breakfast", "brunch",
    "grilled", "stir-fry", "pork", "ribs", "skewers", "bar", "bread", "cake",
    "cheesecake", "condiment", "cupcake", "dressing", "yeast bread"
}

MEAL_MAP = {
    "breakfast": ["breakfast", "brunch"],
    "brunch": ["breakfast", "brunch"],
    "lunch": ["main", "salad", "sandwich"],
    "dinner": ["main", "main dish"],
    "dessert": ["dessert", "cake", "cheesecake", "cupcake", "bar"],
}

app = Flask(__name__)

# ---------- Data loading ----------
def load_data():
    with open(INDEX) as f:
        idx = json.load(f)
    with open(ING) as f:
        ing = json.load(f)
    return idx, ing

IDX, ING_IDX = load_data()

# Build cleaned cuisine list
def clean_cuisine(val):
    # strip " | type: X" or " | method: X"
    v = re.split(r'\s*\|\s*', val)[0].strip().lower()
    return v

def get_clean_cuisines():
    out = set()
    for r in IDX.get("recipes", []):
        for c in r.get("cuisines", []):
            cc = clean_cuisine(c)
            if cc and cc not in NON_CUISINE and "|" not in cc:
                out.add(cc)
    return sorted(out)

CLEAN_CUISINES = get_clean_cuisines()

# ---------- NL parser ----------
def parse_nl(text, ing_keys):
    text_l = text.lower()
    cuisine = None
    for c in CLEAN_CUISINES:
        if c in text_l:
            cuisine = c
            break
    meal = None
    for m in MEAL_MAP:
        if m in text_l:
            meal = m
            break
    # ingredient extraction (fuzzy match vs ingredient keys)
    found = []
    tokens = re.findall(r"[a-z]+", text_l)
    for t in tokens:
        match = difflib.get_close_matches(t, ing_keys, n=1, cutoff=0.85)
        if match and match[0] not in found:
            found.append(match[0])
    return cuisine, meal, found

# ---------- Recommendation logic ----------
def recommend(cuisine, meal, ingredients, max_missing):
    types = MEAL_MAP.get(meal, []) if meal else []
    ing_set = set(ingredients)
    results = []
    for r in IDX.get("recipes", []):
        # cuisine filter
        rc = [clean_cuisine(c) for c in r.get("cuisines", [])]
        if cuisine and cuisine not in rc:
            continue
        # meal filter
        if types and not (set(r.get("types", [])) & set(types)):
            continue
        # ingredient match via ingredient-index
        rec_name = r["name"]
        # all recipes that contain any of the ingredients
        matched = []
        missing = []
        if ing_set:
            for ing in ing_set:
                recipes_with = ING_IDX.get(ing, [])
                if rec_name in recipes_with:
                    matched.append(ing)
                else:
                    missing.append(ing)
            if not matched:
                continue
            total = len(ing_set)
            have = len(matched)
            match_pct = round(have / total * 100)
            if len(missing) > max_missing and match_pct < 80:
                continue
        else:
            match_pct = 100
            missing = []
        makeable = (len(missing) <= max_missing) or (match_pct >= 80)
        results.append({
            "name": rec_name,
            "cuisine": rc[0] if rc else "unknown",
            "match_pct": match_pct,
            "makeable": makeable,
            "file": os.path.join(BASE, r["file"]),
            "missing": missing,
        })
    results.sort(key=lambda x: x["match_pct"], reverse=True)
    return results

# ---------- Templates ----------
INDEX_HTML = """
<!doctype html>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Recipe Dashboard</title>
<style>
body{font-family:sans-serif;margin:0;padding:1rem;background:#fafafa}
.box{max-width:700px;margin:auto}
input,select,button{font-size:1rem;padding:.5rem;margin:.3rem 0;width:100%;box-sizing:border-box}
.row{display:flex;gap:.3rem;flex-wrap:wrap}
.row>*{flex:1}
.card{border:1px solid #ddd;background:#fff;padding:.7rem;margin:.5rem 0;border-radius:8px}
.badge{display:inline-block;background:#2e7d32;color:#fff;padding:.2rem .5rem;border-radius:4px;font-size:.8rem}
.tag{background:#eee;padding:.2rem .4rem;border-radius:4px;font-size:.8rem}
a{color:#1565c0;text-decoration:none}
</style>
<div class="box">
<h2>What should I cook?</h2>
<form method="get">
  <input name="q" placeholder="e.g. Asian broccoli, dinner chicken" value="{{q}}">
  <details>
    <summary>Filters</summary>
    <div class="row">
      <select name="cuisine">
        <option value="">Cuisine: Any</option>
        {% for c in cuisines %}<option value="{{c}}" {% if c==sel_cuisine %}selected{% endif %}>{{c}}</option>{% endfor %}
      </select>
      <select name="meal">
        <option value="">Meal: Any</option>
        {% for m in meals %}<option value="{{m}}" {% if m==sel_meal %}selected{% endif %}>{{m}}</option>{% endfor %}
      </select>
      <select name="max_missing">
        {% for n in [0,1,2,3,4,5] %}<option value="{{n}}" {% if n==sel_max %}selected{% endif %}>Max missing: {{n}}</option>{% endfor %}
      </select>
    </div>
  </details>
  <button type="submit">Search</button>
</form>
{% if results %}
  {% for r in results %}
  <div class="card">
    <a href="/recipe?name={{r.name|urlencode}}"><b>{{r.name}}</b></a><br>
    <span class="tag">{{r.cuisine}}</span>
    <span class="tag">{{r.match_pct}}% match</span>
    {% if r.makeable %}<span class="badge">Makeable now</span>{% endif %}
  </div>
  {% endfor %}
{% elif searched %}
  <p>No recipes found. Try different words or filters.</p>
{% endif %}
</div>
"""

RECIPE_HTML = """
<!doctype html>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{r.name}}</title>
<style>
body{font-family:sans-serif;margin:0;padding:1rem;background:#fafafa}
.box{max-width:700px;margin:auto}
.card{border:1px solid #ddd;background:#fff;padding:.7rem;margin:.5rem 0;border-radius:8px}
.have{color:#2e7d32}.need{color:#c62828}
button{font-size:1rem;padding:.5rem;margin:.3rem 0;width:100%}
a{color:#1565c0}
</style>
<div class="box">
<a href="/">← Back</a>
<h2>{{r.name}}</h2>
<p>Cuisine: {{r.cuisine}} | File: <a href="file://{{r.file}}">{{r.file}}</a></p>
<h3>Ingredients</h3>
{% for i in r.ingredients %}<div class="{% if i.have %}have{% else %}need{% endif %}">{% if i.have %}✅{% else %}❌{% endif %} {{i.name}}</div>{% endfor %}
<h3>Shopping List (copy below)</h3>
<textarea id="shop" rows="4" style="width:100%">{% for i in r.ingredients %}{% if not i.have %}- {{i.name}}
{% endif %}{% endfor %}</textarea>
<button onclick="navigator.clipboard.writeText(document.getElementById('shop').value)">Copy list</button>
</div>
"""

# ---------- Routes ----------
@app.route("/")
def home():
    q = request.args.get("q", "")
    sel_cuisine = request.args.get("cuisine", "")
    sel_meal = request.args.get("meal", "")
    try:
        sel_max = int(request.args.get("max_missing", 3))
    except:
        sel_max = 3
    searched = bool(q or sel_cuisine or sel_meal)
    cuisine = sel_cuisine or None
    meal = sel_meal or None
    ingredients = []
    if q:
        cuisine_parsed, meal_parsed, ing_parsed = parse_nl(q, list(ING_IDX.keys()))
        cuisine = cuisine or cuisine_parsed
        meal = meal or meal_parsed
        ingredients = ing_parsed
    results = recommend(cuisine, meal, ingredients, sel_max) if searched else []
    return render_template_string(INDEX_HTML, q=q, cuisines=CLEAN_CUISINES,
        meals=list(MEAL_MAP.keys()), sel_cuisine=sel_cuisine, sel_meal=sel_meal,
        sel_max=sel_max, results=results, searched=searched)

@app.route("/recipe")
def recipe():
    name = request.args.get("name", "")
    rec = next((r for r in IDX["recipes"] if r["name"] == name), None)
    if not rec:
        return "Recipe not found", 404
    # Build ingredient split (best-effort from ingredient-index)
    rc = [clean_cuisine(c) for c in rec.get("cuisines", [])]
    cuisine = rc[0] if rc else "unknown"
    # We don't have full ingredient lists in index; use ingredient-index keys that map to this recipe
    ings = []
    for k, v in ING_IDX.items():
        if name in v:
            ings.append({"name": k, "have": True})  # assumed have if matched in search; default all need if no filter
    # If no search ingredients, show all as need (graceful)
    if not ings:
        ings = [{"name": k, "have": False} for k in ING_IDX if name in ING_IDX[k]]
    return render_template_string(RECIPE_HTML, r={"name": name, "cuisine": cuisine,
        "file": os.path.join(BASE, rec["file"]), "ingredients": ings})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8780)
