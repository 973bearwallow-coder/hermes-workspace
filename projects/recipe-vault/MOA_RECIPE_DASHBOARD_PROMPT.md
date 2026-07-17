# MoA Task: Build a Recipe Recommendation Dashboard (Flask)

You are building a **local Flask web app** that helps the user decide what to cook
from their existing recipe vault. The vault is ALREADY indexed — you do NOT scrape
or create recipes. You read two JSON files and build a UI on top of them.

---

## Data sources (already exist — read these, do not recreate)

- **Recipe index:** `/home/tom/hermes-workspace/projects/recipe-vault/index.json`
  - Structure: `{"recipes": [ {"name", "file", "cuisines":[...], "types":[...],
    "methods":[...], "has_full_content", "url", "size"}, ... ]}`
  - ~170 recipes. `file` is relative to
    `/home/tom/hermes-workspace/projects/recipe-vault/` (prefix `recipes/` — resolve correctly).
- **Ingredient index:** `/home/tom/hermes-workspace/projects/recipe-vault/ingredient-index.json`
  - Structure: `{"ingredient_name": ["Recipe Name", ...], ...}`
  - Use this to answer "what can I make with X?"

### DATA CLEANUP YOU MUST HANDLE (critical)
The `cuisines` field is MESSY. Examples of bad values you will see:
- `"chinese | type: beef"` → normalize to cuisine `"chinese"`
- `"thai | type: beef"` → normalize to `"thai"`
- `"main | method: stir-fry"` → this is NOT a cuisine; it's a type+method. Drop from cuisine list.
- `"appetizer"`, `"grilled"`, `"pork"`, `"ribs"` → these are TYPES/METHODS/PROTEINS, not cuisines.
  Exclude from the cuisine dropdown.

**Rule:** A valid cuisine = a value that does NOT contain `|` and is NOT one of the known
type/method words (appetizer, main, side dish, salad, dessert, breakfast, brunch, grilled,
stir-fry, pork, ribs, skewers, bar, bread, cake, cheesecake, condiment, cupcake, dressing,
yeast bread). Strip ` | type: X` / ` | method: X` suffixes. Build the cuisine dropdown from
CLEANED values only.

**Meal mapping:** Map user meal words to `types`:
- breakfast / brunch → `breakfast`, `brunch`
- lunch → `main`, `salad`, `sandwich` (best-effort)
- dinner → `main`, `main dish`
- dessert → `dessert`, `cake`, `cheesecake`, `cupcake`, `bar`

---

## Required Features

### 1. Input — ONE natural-language search box + optional filter row
Primary input is a single text box where the user types conversationally, e.g.:
- "I only have chicken, dinner recommendations"
- "Asian chicken soup"
- "Asian tonight, only have broccoli"
- "German, got pork what can I make"
- "breakfast eggs"

Below it, a collapsible filter row (all optional dropdowns):
- Cuisine: [Any ▼] (populated from CLEANED cuisines)
- Meal: [Any ▼] (breakfast / brunch / lunch / dinner / dessert)
- Ingredients: [+ add] (free tags)
- Max missing ingredients: [3 ▼] (default 3)

**Parser logic:** From the NL text, extract:
- cuisine (if a cleaned cuisine word appears)
- meal (breakfast/lunch/dinner/dessert → map to types)
- ingredients (nouns that look like foods — match against ingredient-index keys, fuzzy)
If dropdowns are also set, they OVERRIDE / AND with parsed values.

### 2. Recommendations
Query `index.json` (by cleaned cuisine + meal→types) and `ingredient-index.json`
(by extracted ingredients). For each candidate recipe:
- `match_pct = ingredients_have / ingredients_total * 100`
- "Makeable now" badge if `missing <= max_missing` OR `match_pct >= 80`
Sort results by `match_pct` descending. Show recipe name, cuisine, match %, badge.

### 3. Recipe detail + shopping list
Click a recipe → show:
- Full ingredient list with ✅ (have) / ❌ (need) split
- A **copyable shopping list** of only the ❌ items
- Link to source `file` (absolute path)

### 4. Output
- Save as a runnable Flask app at:
  `/home/tom/hermes-workspace/projects/recipe-vault/recipe_dashboard.py`
- Print the launch command at the end of your output:
  `python3 /home/tom/hermes-workspace/projects/recipe-vault/recipe_dashboard.py`
  (app should listen on 0.0.0.0:8780)
- Mobile-friendly CSS (user is often on phone).

---

## Hard constraints
- DO NOT modify index.json or ingredient-index.json.
- DO NOT invent recipes. Only use what's in the indexes.
- Output a SINGLE self-contained Python file (Flask). No external DB.
- Handle missing/empty states gracefully (no results → friendly message).
- Use ONLY stdlib + flask. No npm, no build step.

## Execution environment (CRITICAL — past runs failed here)
- Start the file with shebang: `#!/usr/bin/env python3`
- After imports, add Flask auto-install fallback:
  ```python
  try:
      from flask import Flask, request, render_template_string
  except ImportError:
      import subprocess, sys
      subprocess.run([sys.executable, "-m", "pip", "install", "flask"])
      from flask import Flask, request, render_template_string
  ```
- The file will be run with `/home/tom/.hermes/hermes-agent/venv/bin/python3`
  (this venv HAS flask). If run with bare `python3` and flask is missing,
  the fallback above installs it automatically.
- Listen on `0.0.0.0:8780` so it is reachable from any device on the LAN.

## Deferred (do NOT build, mention as "v2" in a comment)
- Live grocery price comparison
- Least-stops shopping optimization
- Serving-size scaling

## Success criteria (how the user will test)
1. App launches without error on port 8780
2. Cuisine dropdown shows ONLY cleaned cuisines (no "main | method: stir-fry")
3. Typing "Asian broccoli" returns Asian recipes containing broccoli, sorted by match
4. Clicking a recipe shows ✅/❌ split + copyable shopping list
5. Mobile viewport renders readably
