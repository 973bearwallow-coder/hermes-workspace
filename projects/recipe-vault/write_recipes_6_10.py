#!/usr/bin/env python3
"""
Bulk create recipe files for recipes 6-43.
Uses pre-fetched content stored in this script.
"""
import os
import json
from datetime import datetime

VAULT = os.path.expanduser("~/hermes-workspace/projects/recipe-vault")

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def make_recipe_content(name, url, cuisine, rtype, method, prep, cook, total, yield_s, description, ingredients, instructions, tips, nutrition):
    return f"""# {name}
**Source:** [RecipeTin Eats]({url})
**Cuisine:** {cuisine}
**Type:** {rtype}
**Method:** {method}
**Prep Time:** {prep}
**Cook Time:** {cook}
**Total Time:** {total}
**Yield:** {yield_s}

## Description
{description}

## Ingredients
{ingredients}

## Instructions
{instructions}

## Tips & Notes
{tips}

## Nutrition
{nutrition}
"""

def write_all_copies(name, url, cuisine, rtype, method, prep, cook, total, yield_s, description, ingredients, instructions, tips, nutrition, filename):
    content = make_recipe_content(name, url, cuisine, rtype, method, prep, cook, total, yield_s, description, ingredients, instructions, tips, nutrition)
    # Main recipes dir
    write_file(os.path.join(VAULT, "recipes", filename), content)
    # by-cuisine
    write_file(os.path.join(VAULT, "by-cuisine", cuisine, filename), content)
    # by-type
    write_file(os.path.join(VAULT, "by-type", rtype, filename), content)
    # by-method
    write_file(os.path.join(VAULT, "by-method", method, filename), content)

# Recipe 6: Chicken Francese
write_all_copies(
    "Chicken Francese",
    "https://www.recipetineats.com/chicken-francese/",
    "italian", "main", "stovetop",
    "10 minutes", "15 minutes", "25 minutes", "4 servings",
    "Lightly battered pan-fried chicken breast served in an elegant white wine lemon sauce. Restaurant-quality yet simple to make at home. Unlike Chicken Piccata, this version features a thicker, more abundant sauce with subtle lemon flavor and no capers.",
    """- 2 large chicken breasts (250–300g each), halved horizontally → 4 thin steaks
- ¼ cup plain flour
- 1 tsp kosher/cooking salt + 1 tsp black pepper
- 2 large eggs + 1 tbsp milk
- 3 tbsp extra virgin olive oil
- 1 lemon, thinly sliced (0.3cm)
- 50g / 3 tbsp unsalted butter
- 2 tbsp flour (for roux)
- 2 cups low-sodium chicken stock/broth
- ⅓ cup Chardonnay or dry white wine
- ½ tsp salt
- 1 tbsp chopped parsley (optional garnish)""",
    """1. Cut each breast horizontally → 4 thin steaks.
2. Whisk eggs + milk in a bowl. Mix flour, salt, pepper on a plate. Coat chicken in flour → shake off excess.
3. Heat olive oil in large nonstick pan over medium-high. Dip floured chicken in egg → let excess drip → place in pan.
4. Cook 3 min until golden → flip → reduce heat to medium → cook 4 min more (internal temp: 68°C / 155°F). Remove to plate.
5. In same pan, cook lemon slices ~1.5 min per side until soft/lightly browned. Remove.
6. Wipe pan with paper towels. Melt butter over medium heat → add 2 tbsp flour → stir 1 min (roux).
7. Slowly pour in half the stock while stirring → once smooth, add remaining stock + wine + salt.
8. Simmer 3–4 min until sauce reaches maple syrup thickness.
9. Return chicken + lemon slices to sauce → simmer 30 sec to warm through.
10. Spoon sauce generously over chicken → garnish with parsley.""",
    """- Lemon flavor is subtle—not sour or lip-puckering
- Sauce thickens further when chicken returns to pan
- Leftovers: Keep refrigerated up to 3 days (crust softens but still tasty)
- Serve with mashed potato, rice, orzo, or crusty bread for mopping""",
    "Per serving (with all sauce): 368 cal | 32g protein | 21g fat | 11g carbs | 783mg sodium",
    "chicken_francese.md"
)

# Recipe 7: Vietnamese Caramel Ginger Chicken
write_all_copies(
    "Vietnamese Caramel Ginger Chicken",
    "https://www.recipetineats.com/vietnamese-caramel-ginger-chicken/",
    "vietnamese", "main", "stovetop",
    "7 minutes", "15 minutes", "22 minutes", "5 servings",
    "A fast, flavorful Vietnamese dish featuring juicy chicken thighs braised in a rich caramel-ginger glaze. Only 5 core ingredients, 12-minute braise, no marinating required. Traditional Vietnamese caramel technique.",
    """- 1 kg / 2 lb boneless chicken thighs, cut into large 5cm/2" pieces
- ¼ cup brown sugar, packed
- 3 tbsp fish sauce
- ⅓ cup ginger, finely julienned
- 1 bird's eye or Thai chilli (optional)
- 2 eschalots (French onions/shallots), optional
- 3 tbsp vegetable oil
- ½ cup boiling water""",
    """1. Toss chicken with fish sauce and chilli. Set aside.
2. Use a large non-stick pan (30cm/12"+).
3. Make caramel: Heat oil + sugar over medium-high. Once melted, remove from heat before adding chicken (will sizzle!).
4. Add chicken, ginger, eschalots. Toss briefly. Caramel may harden—will re-melt on return to heat.
5. Cook chicken: Return to stove. Stir until exterior turns pink → white.
6. Add boiling water. Bring to rapid simmer.
7. Braise 10–12 mins: Simmer rapidly until liquid reduces to a thick, sticky glaze. Stir occasionally early, frequently at end.
8. Serve over jasmine rice. Garnish with cilantro/green onion and sliced red chilli.""",
    """- Pan size is crucial: Too small = slow reduction
- Simmer rapidly: High heat speeds evaporation and caramelization
- Chicken breast not recommended (dries out)
- Leftovers: Keep 3 days in fridge. Freezes well.
- Eschalots: Use true eschalots or red onion as substitute""",
    "Per serving (chicken only): 370 cal | 39g protein | 17g fat | 14g carbs (12g sugar) | 1032mg sodium",
    "vietnamese_caramel_ginger_chicken.md"
)

# Recipe 8: Chicken Marsala
write_all_copies(
    "Chicken Marsala",
    "https://www.recipetineats.com/chicken-marsala/",
    "italian", "main", "stovetop",
    "10 minutes", "15 minutes", "25 minutes", "4 servings",
    "A beloved Italian-American classic featuring golden, crispy chicken cutlets in a rich, creamy Marsala wine sauce with mushrooms and eschalots. Restaurant-quality yet easy and economical.",
    """- 2 large chicken breasts (split horizontally → 4 thin steaks) or 4 boneless thighs
- ½ cup dry Marsala wine (not sweet/dessert version)
- ½ cup heavy/thickened cream
- 1 cup chicken stock/broth, low sodium
- 2 eschalots (shallots), finely chopped
- 200g / 7oz white or cremini mushrooms, sliced
- 30g / 2 tbsp unsalted butter (divided)
- 2 tbsp olive oil (divided)
- 3 tbsp plain flour (for coating)
- 2 cloves garlic, minced
- Salt and pepper
- Parsley for garnish""",
    """1. Pound each breast half to 1 cm / 0.4" thickness. Season with salt & pepper, dust lightly with flour. Shake off excess.
2. Heat half the butter + oil in a large non-stick pan over medium-high heat.
3. Cook 3–4 min per side until golden and crispy. Remove to plate.
4. Add remaining butter + oil. Sauté eschalots + garlic for 1 min.
5. Add mushrooms; cook 3–5 min until soft.
6. Pour in Marsala wine; boil rapidly 3 min until reduced by half.
7. Add stock, cream, salt, pepper; simmer 3–5 min until creamy.
8. Return chicken + any juices to sauce; simmer 30 sec–1 min to reheat.
9. Garnish with parsley. Serve over mashed potatoes, polenta, pasta, or rice.""",
    """- Use dry Marsala, not sweet/dessert version
- Substitutes for Marsala: Port, sherry, madeira
- Eschalots preferred for sweetness; sub with ½ small onion
- Cream substitute: Evaporated milk for lower calories
- Leftovers: Keep 3–4 days in fridge
- Not recommended for children due to higher alcohol content""",
    "Per serving: 524 cal | 36g protein | 28g fat (13g saturated) | 16g carbs | 638mg sodium",
    "chicken_marsala.md"
)

# Recipe 9: One Pot Baked Greek Chicken Orzo Risoni
write_all_copies(
    "One Pot Baked Greek Chicken Orzo Risoni",
    "https://www.recipetineats.com/one-pot-baked-greek-chicken-orzo-risoni/",
    "greek", "main", "one-pot",
    "15 minutes", "35 minutes", "50 minutes", "4–5 servings",
    "A one-pot baked Greek chicken risoni (orzo) that delivers risotto-like creaminess without the constant stirring. Features lemon-garlic chicken, hidden vegetables, oozy tomato risoni, and bright Greek flavors with feta.",
    """### Lemon Garlic Chicken
- 1 lb / 500g boneless skinless chicken thighs, cut into 2 cm / 1" pieces
- 2 garlic cloves, finely minced
- 1 tbsp dried oregano
- 1 tbsp olive oil
- ½ tbsp lemon juice
- 1 tsp lemon zest
- ½ tsp each salt and pepper

### Orzo / Risoni Base
- 2 tbsp olive oil
- 2 garlic cloves, minced
- 1 small onion, finely chopped
- 2 medium zucchini, cut into 1 cm cubes
- 1 red bell pepper / capsicum, cut into 1 cm cubes
- 1 tbsp dried oregano
- 2½ cups low-sodium chicken broth/stock
- 14 oz / 400g canned crushed tomatoes
- 1 tbsp tomato paste
- 1½ cups orzo / risoni
- 1½ cups cherry tomatoes
- 1 tsp cooking salt
- ½ tsp black pepper

### Garnishes
- 2 tbsp lemon juice (for drizzling)
- ½ cup (100g) Greek feta cheese, crumbled
- Fresh oregano leaves (optional)""",
    """1. Marinate chicken with lemon juice, zest, garlic, oregano, olive oil, salt, and pepper for 20 minutes (or up to overnight).
2. Preheat oven to 180°C / 350°F (160°C fan).
3. Heat 1 tbsp olive oil in a large ovenproof skillet over high heat. Cook chicken 2–3 minutes until lightly browned but still pink inside. Remove.
4. Add remaining 1 tbsp olive oil, garlic, and onion. Sauté 1 minute. Add zucchini and capsicum; cook 2 minutes.
5. Stir in risoni, oregano, broth, crushed tomatoes, tomato paste, salt, and pepper.
6. Scatter browned chicken and cherry tomatoes over the top—do not stir in.
7. Bake uncovered for 15 minutes until risoni is tender but still firm.
8. Drizzle with 2 tbsp lemon juice. Crumble feta over top. Sprinkle with fresh oregano.""",
    """- Risoni vs. Orzo: Same thing—rice-shaped pasta
- Feta is non-negotiable for authentic flavor
- Don't overcook on stove: Transfer to oven as soon as liquid simmers
- Leftovers: Keep 3 days in fridge. Reheat with splash of water.
- Vegetable swaps: Use any sauté-able veg—carrot, beans, peas, fennel, celery, corn""",
    "Per serving (5 servings): 575 cal | 29g protein | 29g fat (8g saturated) | 53g carbs | 1174mg sodium",
    "one_pot_baked_greek_chicken_orzo_risoni.md"
)

# Recipe 10: Thai Red Curry Pot Roast Chicken
write_all_copies(
    "Thai Red Curry Pot Roast Chicken",
    "https://www.recipetineats.com/thai-red-curry-with-chicken/",
    "thai", "main", "one-pot",
    "5 minutes", "20 minutes", "25 minutes", "4 servings",
    "A fast, flavorful Thai Red Curry with Chicken that delivers bold, authentic Thai flavors in under 30 minutes. Features creamy red curry sauce with chicken, pumpkin, and green beans. Sauce should look slightly split/oily—this is authentic!",
    """### Curry Paste (choose ONE):
- 5–6 tbsp store-bought Thai red curry paste (Maesri recommended)
- OR 1 batch homemade Thai Red Curry Paste

### Extras (only for jar paste):
- 2 large garlic cloves, minced
- 2 tsp fresh ginger, finely grated
- 1 tbsp lemongrass paste or finely chopped fresh lemongrass

### Curry Base:
- 3 tbsp vegetable, canola, or peanut oil
- 1 cup (250 ml) low-sodium chicken broth
- 400 ml (14 oz) full-fat coconut milk
- 6 kaffir lime leaves
- 1 tbsp sugar (white, brown, or palm)
- 2 tsp fish sauce (+ more to taste)

### Protein & Vegetables:
- 350g (12 oz) boneless, skinless chicken thighs, sliced 0.75" thick
- 150g (5 oz) pumpkin or butternut squash, cubed (~1.5 cm)
- 120g (4 oz) green beans, cut into 5 cm (2") pieces
- 12 Thai basil leaves

### Garnishes & Serving:
- Fresh red chilli slices
- Fresh coriander/cilantro
- Steamed jasmine rice""",
    """1. Heat oil in a large skillet over medium-high heat.
2. Sauté curry paste + extras (if using jar paste) for 2 minutes until fragrant and slightly dried.
3. Add chicken broth, stir to dissolve paste, simmer 3 minutes until reduced by half.
4. Add coconut milk, lime leaves, sugar, fish sauce. Stir.
5. Add chicken, spread out, bring to simmer, then reduce heat to medium. Simmer 8–10 minutes.
6. Taste and adjust: Add more fish sauce (salt/umami) or sugar (sweetness).
7. Add pumpkin and green beans, cook 3 minutes until pumpkin is tender.
8. Remove from heat, stir in Thai basil.
9. Serve over jasmine rice, garnished with chilli and coriander.""",
    """- Sauce should look slightly split/oily—this is authentic and correct!
- Maesri brand curry paste recommended (small cans, ~$1.30)
- Chicken thighs preferred (juicier), but breast works
- Thai basil has distinct anise-like flavor; sub with regular basil if needed
- Seafood allergy: Replace fish sauce with light soy sauce
- No hard rules about what goes into a Thai Red Curry—use any vegetables""",
    "Per serving: Calories not specified in source",
    "thai_red_curry_pot_roast_chicken.md"
)

print("Recipes 6-10 written successfully!")
