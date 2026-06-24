#!/usr/bin/env python3
"""Build all RecipeTin Eats recipe files, symlinks, and index.json"""
import json, os, re
from datetime import datetime
from pathlib import Path

VAULT = Path.home() / "hermes-workspace/projects/recipe-vault"
RECIPES_DIR = VAULT / "recipes"
for d in ["by-cuisine", "by-type", "by-method"]:
    (VAULT / d).mkdir(exist_ok=True)

def sf(name):
    n = re.sub(r"[^\w\s-]", "", name.lower())
    n = re.sub(r"\s+", "_", n.strip())
    return re.sub(r"_+", "_", n)[:60].strip("_")

def write_md(name, url, cuisine, rtype, method, prep, cook, total, yield_, desc, ings, steps, tips, nutrition):
    fname = sf(name) + ".md"
    lines = [
        f"# {name}",
        f"**Source:** [RecipeTin Eats]({url})",
        f"**Cuisine:** {cuisine}",
        f"**Type:** {rtype}",
        f"**Method:** {method}",
    ]
    if prep: lines.append(f"**Prep Time:** {prep}")
    if cook: lines.append(f"**Cook Time:** {cook}")
    if total: lines.append(f"**Total Time:** {total}")
    if yield_: lines.append(f"**Yield:** {yield_}")
    lines += ["", "## Description", desc, "", "## Ingredients"]
    for i in ings: lines.append(f"- {i}")
    lines += ["", "## Instructions"]
    for n, s in enumerate(steps, 1): lines.append(f"{n}. {s}")
    if tips:
        lines += ["", "## Tips & Notes"]
        for t in tips: lines.append(f"- {t}")
    if nutrition:
        lines += ["", "## Nutrition", nutrition]
    lines.append("")
    (RECIPES_DIR / fname).write_text("\n".join(lines))
    return fname

def link(fname, cuisine, rtype, method):
    for sub, key in [("by-cuisine", cuisine), ("by-type", rtype), ("by-method", method)]:
        d = VAULT / sub / key
        d.mkdir(exist_ok=True)
        for e in d.iterdir():
            if e.is_symlink(): e.unlink()
        ln = d / fname
        if not ln.exists(): ln.symlink_to("../../recipes/" + fname)

# ============================================================================
# RECIPES
# ============================================================================

recipes_meta = []  # (name, url, cuisine, type, method, fname)

# 1
f = write_md("French Chicken au Poivre Sauce","https://www.recipetineats.com/french-chicken-au-poivre-sauce","french","main","stovetop","8 mins","20 mins","28 mins","4 servings",
"A quick, elegant French-inspired dish featuring golden pan-seared chicken in a rich, creamy peppercorn sauce with brandy.",
["2 large boneless skinless chicken breasts (250-300g each) sliced horizontally into 4 thin steaks","3/4 tsp kosher salt","2 tbsp vegetable oil","2 tsp whole black peppercorns coarsely crushed","1/3 cup brandy/cognac","1 1/2 cups low-sodium beef stock","3/4 cup thickened/heavy cream"],
["Cut each breast horizontally into 2 thin steaks (4 total). Season with salt only.","Heat oil in a 28cm pan over high heat. Sear chicken 2-3 min per side until golden.","Turn heat off, carefully add brandy. Let bubble 20-30 sec to burn off alcohol; scrape fond.","Add beef stock, return to high heat, simmer 4 min until reduced by half.","Stir in cream and crushed peppercorns. Simmer 3-4 min until sauce coats back of spoon.","Return chicken + resting juices to pan. Simmer 2-3 min. Serve immediately."],
["Use beef stock for deeper richer flavor","Don't use expensive brandy","Potatoes are essential - mashed fondant or roasted"],
"Calories: 442 kcal | Protein: 35g | Fat: 27g | Carbs: 3g | Sodium: 788mg")
link(f,"french","main","stovetop"); recipes_meta.append(("French Chicken au Poivre Sauce","https://www.recipetineats.com/french-chicken-au-poivre-sauce","french","main","stovetop",f))

# 2
f = write_md("Thai Grilled Chicken (Gai Yang)","https://www.recipetineats.com/thai-grilled-chicken-gai-yang/","thai","main","grilled","8 mins","12 mins","20 mins + marinating","4-6 servings",
"A simplified home-cook-friendly version of Thailand's iconic street-food grilled chicken. Uses boneless thighs and a stick-blender marinade.",
["2 lb / 1 kg boneless skinless chicken thighs","1 large lemongrass stalk (white part only sliced)","4 cloves garlic","2 1/2 tbsp fish sauce","1 tbsp light soy sauce","2 tsp dark soy sauce","3 tbsp brown sugar","2 tbsp neutral oil"],
["Blitz marinade ingredients with stick blender until lemongrass is pulverized.","Coat chicken thoroughly. Marinate overnight (24 hrs ideal) minimum 3 hours.","Preheat BBQ or pan on high. Cook 5-6 min per side until golden-brown with charred edges.","Rest 3-5 min. Serve with coconut rice lime wedges and dipping sauce."],
["Boneless skinless thighs are best","Breast can be used - split horizontally or pound to even thickness","Use both light and dark soy sauce"],
"Calories: 280 kcal | Protein: 39g | Fat: 11g | Carbs: 4g | Sodium: 596mg")
link(f,"thai","main","grilled"); recipes_meta.append(("Thai Grilled Chicken (Gai Yang)","https://www.recipetineats.com/thai-grilled-chicken-gai-yang/","thai","main","grilled",f))

# 3
f = write_md("Chicken Chasseur","https://www.recipetineats.com/chicken-chasseur","french","main","stovetop","15 mins","45 mins","1 hour","4 servings",
"A classic French dish featuring chicken braised in a rich mushroom-tomato sauce with brandy and fresh tarragon.",
["4 bone-in skin-on chicken thighs + 4 drumsticks","3/4 tsp kosher salt + 1/2 tsp black pepper","3 tbsp plain flour","2 tbsp vegetable oil + 30g unsalted butter","400g white mushrooms sliced","2 brown onions sliced","3 garlic cloves minced","1/4 cup brandy","1/2 cup Chardonnay","3 tbsp tomato paste","2 1/2 cups low-sodium beef stock","30g cold butter cubed","1 tbsp fresh tarragon"],
["Pat chicken dry. Season and coat in flour. Sear in large lidded skillet until golden.","Add mushrooms and onions cook 5 min. Add garlic cook 30 sec.","Add brandy let bubble. Add wine reduce by half. Add tomato paste cook 1 min.","Add beef stock. Return chicken skin-side up. Cover cook 10 min.","Remove lid simmer uncovered 20 min. Turn off heat stir in cold butter cubes.","Return chicken to sauce sprinkle with tarragon. Serve with mashed potato."],
["Browning is essential for flavor","Cold butter finish must be cold and cubed","Beef stock over chicken stock for deeper flavor"],
"Calories: 854 kcal | Protein: 53g | Fat: 57g | Carbs: 18g | Sodium: 1489mg")
link(f,"french","main","stovetop"); recipes_meta.append(("Chicken Chasseur","https://www.recipetineats.com/chicken-chasseur","french","main","stovetop",f))

# 4
f = write_md("New Orleans Chicken Wings","https://www.recipetineats.com/new-orleans-chicken-wings","american","appetizer","baked","10 mins","50 mins","1 hour","4-10 servings",
"Bold spicy and bursting with Louisiana flavor. Homemade Creole seasoning and garlic butter basting for rich caramelized flavor. Baked not fried.",
["1.25 kg / 2.5 lb chicken wings cut into drumettes & wingettes","50g unsalted butter melted","2 garlic cloves crushed","Creole Seasoning: 1 1/2 tbsp brown sugar 2 1/2 tsp paprika 1 1/2 tsp salt 1 tsp garlic powder 1 tsp onion powder 1/2 tsp black pepper 1/2 tsp dried thyme 1/2 tsp dried oregano 1/4 tsp cayenne"],
["Preheat oven to 200C/390F. Line tray with foil + baking paper.","Mix garlic into butter. Combine Creole seasoning. Toss wings with seasoning then garlic butter.","Arrange skin-side up in single layer. Bake 45-50 mins basting at 30 40 and end.","Serve with tray juices poured over."],
["Don't crowd the tray","Baste generously for caramelized flavor","Brown sugar is essential"],
"Calories: ~350 kcal per serving | Protein: 25g | Fat: 22g")
link(f,"american","appetizer","baked"); recipes_meta.append(("New Orleans Chicken Wings","https://www.recipetineats.com/new-orleans-chicken-wings","american","appetizer","baked",f))

# 5
f = write_md("Chicken Cacciatore (Italian Chicken Stew)","https://www.recipetineats.com/chicken-cacciatore-italian-chicken-stew/","italian","main","stovetop","15 mins","55 mins","1 hour 10 mins","4-6 servings",
"A hearty rustic Italian stew with chicken and vegetables simmered in a tomato sauce rich with wine and herbs.",
["Bone-in skin-on thighs and drumsticks (4 of each ~1.6 kg total)","Salt pepper olive oil","Mushrooms capsicum onion garlic","Anchovies (the secret ingredient!)","Red wine (Pinot noir or any dry red)","Kalamata olives","Chicken stock crushed tomato tomato paste","Bay leaves rosemary dried oregano"],
["Season and brown chicken in large deep lidded pan.","Sauté onion rosemary bay leaves oregano. Add garlic and anchovies mash until golden.","Add mushrooms and capsicum cook 5 min. Add tomato paste cook 2 min.","Add wine reduce by 75%. Add stock tomato salt pepper.","Return chicken skin-side up. Cover simmer 20 min. Uncover add olives simmer 10 min.","Serve over mashed potatoes or polenta."],
["Anchovies add umami depth without fishy taste","Kalamata olives are essential","Bone-in skin-on cuts are best for juiciness"],
"Calories: 495 kcal | Protein: 37g | Fat: 30g | Carbs: 15g | Sodium: 976mg")
link(f,"italian","main","stovetop"); recipes_meta.append(("Chicken Cacciatore (Italian Chicken Stew)","https://www.recipetineats.com/chicken-cacciatore-italian-chicken-stew/","italian","main","stovetop",f))

# 6
f = write_md("Chicken Francese","https://www.recipetineats.com/chicken-francese/","italian","main","stovetop","10 mins","15 mins","25 mins","4 servings",
"A restaurant-quality dish featuring lightly battered pan-fried chicken breasts in an elegant white wine lemon sauce. Like Chicken Piccata but with a thicker more abundant sauce and no capers.",
["2 large chicken breasts (250-300g each) halved horizontally","1/4 cup plain flour 1 tsp salt 1 tsp black pepper","2 large eggs + 1 tbsp milk","3 tbsp extra virgin olive oil","1 lemon thinly sliced","50g unsalted butter","2 cups low-sodium chicken stock","1/3 cup Chardonnay","1 tbsp parsley"],
["Cut breasts horizontally into 2 thin steaks. Whisk eggs + milk. Mix flour salt pepper.","Coat chicken in flour then egg. Pan-fry 3 min first side reduce heat cook 4 min more.","Cook lemon slices ~1.5 min until soft. Remove. Wipe pan.","Melt butter add 2 tbsp flour stir 1 min. Slowly add stock then wine. Simmer 3-4 min.","Return chicken + lemons to sauce. Simmer 30 sec. Garnish with parsley."],
["Chardonnay is the best all-rounder cooking wine","Frying lemon slices captures fond and infuses deep flavor","Sauce should coat back of spoon like syrup"],
"Calories: 368 kcal | Protein: 32g | Fat: 21g | Carbs: 11g | Sodium: 783mg")
link(f,"italian","main","stovetop"); recipes_meta.append(("Chicken Francese","https://www.recipetineats.com/chicken-francese/","italian","main","stovetop",f))

# 7
f = write_md("Vietnamese Caramel Ginger Chicken","https://www.recipetineats.com/vietnamese-caramel-ginger-chicken/","vietnamese","main","stovetop","7 mins","15 mins","22 mins","5 servings",
"A fast flavorful Vietnamese dish featuring juicy chicken thighs braised in a rich caramel-ginger glaze. Only 5 core ingredients 12-minute braise no marinating required.",
["1 kg / 2 lb boneless chicken thighs cut into large 5cm pieces","1/4 cup brown sugar packed","3 tbsp fish sauce","1/3 cup ginger finely julienned","1 bird's eye chili (optional)","2 eschalots (optional)","3 tbsp vegetable oil","1/2 cup boiling water"],
["Toss chicken with fish sauce and chili.","In large non-stick pan heat oil + sugar over medium-high until melted.","Remove from heat add chicken ginger eschalots. Toss briefly.","Cook until chicken turns pink to white. Add water bring to rapid simmer.","Braise 10-12 min until liquid reduces to sticky glaze. Serve with jasmine rice."],
["Pan size is crucial: >=30cm to avoid overcrowding","If sauce won't reduce remove chicken reduce liquid alone then recombine"],
"Calories: 370 kcal | Protein: 39g | Fat: 17g | Carbs: 14g | Sodium: 1032mg")
link(f,"vietnamese","main","stovetop"); recipes_meta.append(("Vietnamese Caramel Ginger Chicken","https://www.recipetineats.com/vietnamese-caramel-ginger-chicken/","vietnamese","main","stovetop",f))

# 8
f = write_md("Chicken Marsala","https://www.recipetineats.com/chicken-marsala/","italian","main","stovetop","10 mins","15 mins","25 mins","4 servings",
"A beloved Italian-American classic featuring golden crispy chicken cutlets smothered in a rich creamy Marsala wine and mushroom sauce.",
["2 large chicken breasts split horizontally into 4 thin steaks or 4 boneless thighs","Dry Marsala wine (not sweet/dessert version)","Heavy/thickened cream","Chicken stock mushrooms eschalots garlic","Butter olive oil flour salt pepper parsley"],
["Pound breast halves to 1 cm thickness. Season with salt pepper then flour.","Heat half butter + oil over medium-high. Cook chicken 3-4 min per side until golden.","Sauté eschalots + garlic 1 min. Add mushrooms cook 3-5 min.","Pour in Marsala boil 3 min until reduced by half.","Add stock cream salt pepper. Simmer 3-5 min. Return chicken to sauce reheat."],
["Use dry Marsala - it's the soul of the dish","Don't reduce sauce too much - thickens as it cools","Always reheat chicken in the sauce"],
"Calories: 524 kcal | Protein: 36g | Fat: 28g | Carbs: 16g | Sodium: 638mg")
link(f,"italian","main","stovetop"); recipes_meta.append(("Chicken Marsala","https://www.recipetineats.com/chicken-marsala/","italian","main","stovetop",f))

# 9
f = write_md("One Pot Baked Greek Chicken Orzo Risoni","https://www.recipetineats.com/one-pot-baked-greek-chicken-orzo-risoni/","greek","main","one-pot","15 mins","35 mins","50 mins","4-5 servings",
"A complete flavorful dinner made in one pot. Tender chicken al dente risoni (orzo) and vibrant Greek-inspired flavors: lemon garlic oregano and feta.",
["1 lb (500g) boneless skinless chicken thighs cut into 2 cm pieces","2 garlic 1 tbsp dried oregano 1 tbsp olive oil 1/2 tbsp lemon juice 1 tsp lemon zest salt pepper","2 tbsp olive oil 2 garlic 1 small onion 2 medium zucchini 1 red bell pepper","1 tbsp dried oregano 2 1/2 cups chicken broth 14 oz crushed tomatoes 1 tbsp tomato paste","1 1/2 cups orzo/risoni 1 1/2 cups cherry tomatoes salt pepper","2 tbsp lemon juice 1/2 cup Greek feta fresh oregano"],
["Marinate chicken 20 min or overnight. Preheat oven to 180C/350F.","Brown chicken in ovenproof skillet 2-3 min. Remove.","Sauté garlic onion 1 min. Add zucchini and capsicum cook 2 min.","Add risoni oregano broth crushed tomatoes tomato paste salt pepper.","Top with chicken and cherry tomatoes. Bake 15 min uncovered.","Drizzle with lemon juice crumble feta garnish with oregano."],
["Feta is non-negotiable","Transfer to oven as soon as liquid simmers","Leftovers keep 3 days reheat with splash of water"],
"Calories: 575 kcal | Protein: 29g | Fat: 29g | Carbs: 53g | Sodium: 1174mg")
link(f,"greek","main","one-pot"); recipes_meta.append(("One Pot Baked Greek Chicken Orzo Risoni","https://www.recipetineats.com/one-pot-baked-greek-chicken-orzo-risoni/","greek","main","one-pot",f))

# 10
f = write_md("Thai Red Curry Pot Roast Chicken","https://www.recipetineats.com/thai-red-curry-pot-roast-chicken/","thai","main","baked","10 mins","1 hr 15 mins","2 hrs 35 mins","5-6 servings",
"A showstopping one-pot roast chicken infused with rich Thai red curry flavors. Ultra-juicy chicken with outrageously flavorful red curry sauce.",
["Whole chicken (1.8 kg / 3.6 lb)","Thai red curry paste (Maesri brand recommended)","Fresh garlic ginger lemongrass","Coconut cream (not milk)","Kaffir lime leaves fish sauce white sugar","Small whole potatoes green beans","Thai basil coriander"],
["Remove chicken from fridge 1 hour ahead. Pat dry sprinkle with 1 tsp salt.","Preheat oven to 200C/400F. Sauté curry paste + garlic ginger lemongrass 2 min.","Add 1 cup chicken stock reduce by half. Stir in coconut cream kaffir lime leaves sugar fish sauce.","Add chicken and potatoes. Spoon sauce over. Bake covered 40 min.","Remove lid increase to 220C/425F. Bake uncovered 30 min basting every 10 min.","Add green beans in final 10 min. Rest 10 min. Stir Thai basil into sauce. Serve with jasmine rice."],
["Maesri brand red curry paste is strongly recommended","Coconut cream (not milk) is essential","Pot-roasting keeps meat juicy even if slightly overcooked"],
"Calories: 766 kcal | Protein: 37g | Fat: 65g | Carbs: 12g | Sodium: 794mg")
link(f,"thai","main","baked"); recipes_meta.append(("Thai Red Curry Pot Roast Chicken","https://www.recipetineats.com/thai-red-curry-pot-roast-chicken/","thai","main","baked",f))

# 11
f = write_md("Chicken in Creamy Mustard Sauce","https://www.recipetineats.com/chicken-in-creamy-mustard-sauce/","french","main","stovetop","5 mins","10 mins","15 mins","4 servings",
"A fast elegant dish featuring pan-seared chicken in a rich creamy mustard sauce made with just 4 base ingredients: chicken cream Dijon mustard and wholegrain mustard.",
["700g / 1.4 lb boneless skinless thighs (preferred) or breasts","1/2 cup thickened/heavy cream","1 tbsp Dijon mustard","1 tbsp wholegrain mustard","Optional: fresh tarragon parsley","Salt and pepper"],
["Thighs: no prep. Breasts: split horizontally pound to 1 cm thickness.","Season with salt and pepper. Use a non-non-stick pan to develop fond.","Thighs: medium-high heat 4 min first side 3-4 min second side.","Breasts: high heat 2 min per side. Rest chicken on plate.","Scrape out loose burnt bits. Return pan to medium heat.","Add cream + both mustards. Stir until mustard dissolves. Heat until hot.","Stir in herbs if using. Plate chicken spoon over sauce."],
["Pan choice matters: fond = umami-rich sauce. Cast iron ideal.","Tarragon gives this sauce a restaurant-like vibe","Dijon acts as thickener - no reduction needed"],
"Calories: 364 kcal | Protein: 35g | Fat: 24g | Carbs: 2g")
link(f,"french","main","stovetop"); recipes_meta.append(("Chicken in Creamy Mustard Sauce","https://www.recipetineats.com/chicken-in-creamy-mustard-sauce/","french","main","stovetop",f))

# 12
f = write_md("Chicken Shawarma (Middle Eastern)","https://www.recipetineats.com/chicken-sharwama-middle-eastern/","middle-eastern","main","grilled","10 mins","10 mins","20 mins + marinating","4-6 servings",
"A beloved Middle Eastern street food made with everyday spices. Cardamom is the key ingredient that distinguishes Shawarma from other spice blends.",
["Boneless skinless thighs preferred (juicier)","Lemon juice (fresh only) olive oil","Shawarma Marinade: ground coriander cumin cardamom (essential!) smoked paprika cayenne salt black pepper","Lemon Yogurt Sauce or Tahini Sauce"],
["Mix marinade in ziplock bag. Add chicken seal massage to coat. Marinate 12-24 hours min 3 hours.","Make yogurt sauce rest >= 20 mins.","Cook on stovetop or BBQ: medium-high heat 4-5 mins per side until charred.","Rest 3-5 min before slicing. Serve family-style with platter."],
["Cardamom is the key distinguishing ingredient","Freeze raw chicken in marinade - it marinates as it defrosts","Serve as wraps or plates with Mejadra hummus or Greek Salad"],
"Calories: 275 kcal | Protein: 32.9g | Fat: 16.2g | Carbs: 1.1g")
link(f,"middle-eastern","main","grilled"); recipes_meta.append(("Chicken Shawarma (Middle Eastern)","https://www.recipetineats.com/chicken-sharwama-middle-eastern/","middle-eastern","main","grilled",f))

# 13
f = write_md("Coq au Vin","https://www.recipetineats.com/coq-au-vin/","french","main","baked","20 mins","1 hr 25 mins","1 hr 45 mins + marinating","4-5 servings",
"A classic French dish of bone-in skin-on chicken braised in red wine with bacon mushrooms onions and herbs. Best when made 1-2 days ahead.",
["4 bone-in skin-on thighs + 4 drumsticks","750ml Pinot Noir (or any dry red)","16 pearl onions 1 bay leaf 3 thyme sprigs","750ml low-sodium beef stock","150g slab bacon cut into chunky lardons","400g white button mushrooms","60g butter 3 garlic cloves 2 tbsp tomato paste","7 tbsp all-purpose flour"],
["Marinate chicken wine onions bay leaf thyme 12-24 hrs.","Strain marinade. Reserve wine herbs onions. Dry chicken. Reduce wine by half.","Sear chicken until golden. Cook bacon until golden. Sauté mushrooms until golden.","Cook onions until golden. Add butter garlic tomato paste. Add flour cook 2 min.","Slowly whisk in beef stock then reduced wine. Return everything to pot.","Cover and bake at 180C for 45 min. Best made 1-2 days ahead. Serve with mashed potatoes."],
["Don't skip marination - fundamental to flavor","Use beef stock not chicken - darker color richer taste","Cheap wine works fine when cooked long"],
"Calories: ~750 kcal | Protein: 50g | Fat: 40g | Carbs: 20g")
link(f,"french","main","baked"); recipes_meta.append(("Coq au Vin","https://www.recipetineats.com/coq-au-vin/","french","main","baked",f))

# 14
f = write_md("Chicken Piccata","https://www.recipetineats.com/chicken-piccata/","italian","main","stovetop","10 mins","10 mins","20 mins","3 servings",
"A better Chicken Piccata with lemon tang that's just right less fat than most recipes and a Parmesan flour coating that makes this dish a standout.",
["450g / 16oz chicken breast (2 large pieces)","4 tbsp flour 2 1/2 tbsp parmesan finely grated 1/2 tsp salt 1/4 tsp pepper","2 1/2 tbsp olive oil 1 tbsp unsalted butter","2 tbsp unsalted butter cubed 2/3 cup dry white wine","2 tbsp fresh lemon juice 3 tbsp capers in brine drained","1 1/2 tsp parsley chopped"],
["Cut each breast into 3 pieces. Pound to 1/2cm thick.","Drizzle with oil. Mix flour parmesan salt pepper. Press chicken into mixture.","Heat oil + butter over medium-high. Cook 3-4 min first side 1 min second side.","Clean skillet. Add wine simmer rapidly until reduced by half (~3 min).","Add lemon juice simmer 1 min. Reduce heat to low. Add cubed butter and swirl.","Stir in capers and parsley. Pour sauce over chicken."],
["Parmesan in the flour coating is the trick that makes this standout","Wine reduction cooks out alcohol leaving concentrated flavor","Butter must be swirled on low heat - high heat causes sauce to split"],
"Calories: 358 kcal | Protein: 33g | Fat: 19g | Carbs: 5g | Sodium: 800mg")
link(f,"italian","main","stovetop"); recipes_meta.append(("Chicken Piccata","https://www.recipetineats.com/chicken-piccata/","italian","main","stovetop",f))

# 15 - COOKBOOK EXCLUSIVE
f = write_md("Creamy Chicken Mushroom Fettuccine","https://www.recipetineats.com/creamy-chicken-mushroom-fettucine/","italian","main","stovetop","10 mins","20 mins","30 mins","4 servings",
"COOKBOOK EXCLUSIVE - This recipe is only available in Nagi's debut cookbook 'Dinner' (page 170). The Italian secret to perfect pasta is starchy pasta water which gently thickens this creamy sauce.",
["This recipe is exclusive to the Dinner cookbook by Nagi Maehashi.","Purchase the cookbook to access the full recipe.","Scan the QR code in the book for a how-to video."],
["This recipe is exclusive to the Dinner cookbook by Nagi Maehashi.","Visit https://www.recipetineats.com/cookbook/ for more information."],
["This is a cookbook exclusive recipe - not available on the website","The cookbook contains 131 recipe videos accessible via QR codes"],
"Not available - cookbook exclusive recipe.")
link(f,"italian","main","stovetop"); recipes_meta.append(("Creamy Chicken Mushroom Fettuccine","https://www.recipetineats.com/creamy-chicken-mushroom-fettucine/","italian","main","stovetop",f))

# 16 - COOKBOOK EXCLUSIVE
f = write_md("Creamy Tuscan Chicken Pasta Bake","https://www.recipetineats.com/creamy-tuscan-chicken-pasta-bake/","italian","main","baked","15 mins","45 mins","1 hour","4-6 servings",
"COOKBOOK EXCLUSIVE - Everything you want in a creamy pasta bake. Loads of cheesy sauce juicy chunks of chicken and tangy pops of sun-dried tomato. Exclusive to Nagi's debut cookbook 'Dinner'.",
["This recipe is exclusive to the Dinner cookbook by Nagi Maehashi.","Purchase the cookbook to access the full recipe."],
["This recipe is exclusive to the Dinner cookbook by Nagi Maehashi.","Visit https://www.recipetineats.com/cookbook/ for more information."],
["This is a cookbook exclusive recipe","Similar to the Creamy Tuscan Chicken Soup available on the website"],
"Not available - cookbook exclusive recipe.")
link(f,"italian","main","baked"); recipes_meta.append(("Creamy Tuscan Chicken Pasta Bake","https://www.recipetineats.com/creamy-tuscan-chicken-pasta-bake/","italian","main","baked",f))

# 17
f = write_md("Chicken Broccoli Stir Fry","https://www.recipetineats.com/chicken-broccoli-stir-fry/","chinese","main","stir-fry","10 mins","6 mins","16 mins","5-6 servings",
"A quick and easy Chicken Broccoli Stir Fry that uses the minimum ingredients but still delivers a dish that stacks up to Chinese restaurant standard. Extra saucy by design!",
["500g (1 lb) chicken breast thinly sliced (or boneless thighs)","1 1/2 tsp baking soda (for velveting optional)","Sauce: 2 tbsp cornflour 3 tbsp light soy sauce 1 1/2 tbsp Chinese cooking wine or Mirin 3 tbsp oyster sauce 2 tsp toasted sesame oil white pepper","2 tbsp oil 1/2 onion sliced 2 garlic cloves minced","400g (14 oz) broccoli florets (~5 cups)","1 1/4 cups water"],
["Tenderise chicken (optional): toss with baking soda rest 20 min rinse thoroughly.","Cook broccoli: steam or boil until tender. Drain well.","Mix sauce: whisk cornflour + soy sauce until smooth then add remaining ingredients.","Heat oil in large skillet/wok over high heat. Cook garlic + onion ~10 sec.","Add chicken stir 2 min until just cooked through.","Add broccoli sauce and water. Stir 1-2 min until sauce turns glossy. Serve over rice."],
["Velveting is optional but elevates chicken breast to restaurant-style texture","Use all 1 1/4 cups water - reduces saltiness and ensures sauciness","Do not freeze - cornstarch-thinned sauces become watery when thawed"],
"Calories: 239 kcal | Protein: 25g | Fat: 10g | Carbs: 11g | Sodium: 1045mg")
link(f,"chinese","main","stir-fry"); recipes_meta.append(("Chicken Broccoli Stir Fry","https://www.recipetineats.com/chicken-broccoli-stir-fry/","chinese","main","stir-fry",f))

# 18
f = write_md("Thai Chicken Lettuce Cups (Larb Gai / Laab Gai)","https://www.recipetineats.com/thai-chicken-lettuce-cups-larb-gai-laab-gai","thai","main","stir-fry","10 mins","10 mins","20 mins","2-3 servings",
"Thai Lettuce Wraps known as Larb Gai - a fresh flavorful and healthy Thai dish featuring seasoned chicken mince served in crisp lettuce cups. Bold aromatic flavors - sweet savory sour and spicy.",
["2 tsp cornflour/cornstarch + 3 tbsp water","2 1/2 tbsp lime juice 2 tbsp fish sauce 2 tsp brown sugar","2 tbsp peanut oil 1 tbsp fresh ginger 2 large garlic cloves","1 lemongrass stalk (white part finely chopped)","2 Thai or bird's eye chilies (deseeded & chopped)","1 lb (500g) chicken mince","1/2 red onion 1/3 cup coriander 1/3 cup mint","6-8 lettuce leaves crushed peanuts lime wedges"],
["Make sauce slurry: mix water + cornflour then add lime juice fish sauce sugar.","Heat oil in wok over medium-high. Add ginger garlic lemongrass chili. Sauté 45-60 sec.","Increase heat to high. Add chicken mince. Break into small pieces cook 3-4 min.","Pour in sauce mixture. Cook 45-60 sec until thickened.","Remove from heat. Stir in red onion cilantro mint.","Serve in lettuce cups with crushed peanuts and lime wedges."],
["Traditional thickener: toast 2 tbsp rice in dry wok 5 mins until dark golden then grind to powder","Lemongrass: use bottom 7-10 cm of fresh stalk or 1 tbsp paste","Serve with Thai Peanut Satay Sauce for extra flavor"],
"Calories: 351 kcal | Protein: 28g | Fat: 21.4g | Carbs: 13g | Sodium: 559mg")
link(f,"thai","main","stir-fry"); recipes_meta.append(("Thai Chicken Lettuce Cups (Larb Gai / Laab Gai)","https://www.recipetineats.com/thai-chicken-lettuce-cups-larb-gai-laab-gai","thai","main","stir-fry",f))

# 19
f = write_md("Chicken Pad Thai","https://www.recipetineats.com/chicken-pad-thai/","thai","main","stir-fry","20 mins","10 mins","30 mins","2-3 servings",
"Restaurant-quality Pad Thai that truly stacks up to great Thai restaurants yet is totally doable for every home cook. Features slippery rice noodles a sweet-savoury-sour sauce crushed peanuts and fresh lime.",
["125g dried rice sticks (Chang's 'Thai style' recommended)","Sauce: 1 1/2 tbsp tamarind puree 3 tbsp brown sugar 2 tbsp fish sauce 1 1/2 tbsp oyster sauce","2-3 tbsp oil onion garlic 2 eggs","Firm tofu (cut into 3cm batons) bean sprouts garlic chives","Peanuts (finely chopped) lime wedges chili flakes"],
["Soak noodles in boiling water 5 min. Drain rinse with cold water.","Mix sauce in small bowl.","Heat oil in large non-stick pan/wok over high heat.","Cook onion + garlic 30 sec. Add chicken cook 1.5 min until mostly done.","Push chicken to side scramble eggs on other side then combine.","Add bean sprouts tofu noodles then sauce. Toss gently ~1.5 min.","Add garlic chives + half the peanuts. Toss briefly remove from heat.","Serve immediately with remaining peanuts lime wedges optional chili."],
["Tamarind is the heart and soul of Pad Thai sauce","Ketchup substitute available if no tamarind","Have all ingredients prepped before cooking - stir-fries move fast"],
"Calories: ~650 kcal per serving (based on 2 servings)")
link(f,"thai","main","stir-fry"); recipes_meta.append(("Chicken Pad Thai","https://www.recipetineats.com/chicken-pad-thai/","thai","main","stir-fry",f))

# 20
f = write_md("Chicken Chow Mein","https://www.recipetineats.com/chicken-chow-mein/","chinese","main","stir-fry","10 mins","5 mins","15 mins","2-3 servings",
"A great Chow Mein comes down to the sauce. Slippery noodles slick with the savoury sauce is noodle heaven! Ready in 15 minutes - faster than delivery.",
["200g (6 oz) chicken breast or thigh thinly sliced","4 cups green cabbage finely shredded 1 carrot julienned","1 1/2 tbsp peanut oil 2 cloves garlic finely chopped","200g (6 oz) Chow Mein noodles","1 1/2 cups bean sprouts 3 green onions (5cm pieces)","1/4 cup water","Sauce: 2 tsp cornflour 1 1/2 tbsp soy sauce 1 1/2 tbsp oyster sauce 1 1/2 tbsp Chinese cooking wine 2 tsp sugar 1/2 tsp sesame oil white pepper"],
["Make sauce: mix cornflour + soy sauce first then add all other ingredients.","Marinate chicken with 1 tbsp sauce rest 10 mins.","Cook noodles: soak in boiling water 1 min then drain.","Heat oil in wok/skillet over high heat. Add garlic stir-fry 10 sec.","Add chicken cook ~1 min. Add cabbage carrot white parts of green onions stir-fry 1 1/2 min.","Add noodles sauce and water. Toss constantly for 1 min.","Add bean sprouts + green onion tops toss 30 sec. Serve immediately."],
["Chinese cooking wine is essential for authentic takeout flavor","Have everything prepped before cooking - this dish moves fast","Chow Mein noodles are thin dry and crinkly - not oily like Lo Mein"],
"Calories: 554 kcal | Protein: 28g | Fat: 31.2g | Carbs: 46.5g | Sodium: 1089mg")
link(f,"chinese","main","stir-fry"); recipes_meta.append(("Chicken Chow Mein","https://www.recipetineats.com/chicken-chow-mein/","chinese","main","stir-fry",f))

# 21
f = write_md("Thai Basil Chicken Stir Fry","https://www.recipetineats.com/thai-basil-chicken-stir-fry/","thai","main","stir-fry","10 mins","5 mins","15 mins","1-2 servings",
"The gold standard of Thai Chicken stir fries - a fast easy recipe that rivals restaurant quality. Features Thai Basil and significant heat.",
["225g / 7oz chicken thigh fillets (cut into bite-size pieces)","1 green onion (4cm lengths) 1 cup Thai basil leaves","2 garlic cloves (finely chopped) 1 bird's eye chili (deseeded & chopped)","1 1/2 tbsp oil","Sauce: 2 tsp oyster sauce 1 tsp light soy sauce 1 tsp dark soy sauce 1 tsp sugar 2 tbsp water"],
["Mix sauce ingredients in a small bowl.","Heat oil in wok or pan over high heat.","Add garlic and chili cook 10 seconds.","Add white part of green onions and chicken. Fry until cooked (~2 min).","Add sauce cook 1 min until water reduces to a thick glossy sauce.","Toss through green part of green onions and basil leaves. Stir until just wilted.","Serve immediately with steamed jasmine rice."],
["Best substitute for Thai Basil is normal basil","Finely chop garlic (don't mince) to prevent burning","Makes 1 large or 2 reasonable servings"],
"Calories: 360 kcal | Protein: 19g | Fat: 29g | Carbs: 5g | Sodium: 588mg")
link(f,"thai","main","stir-fry"); recipes_meta.append(("Thai Basil Chicken Stir Fry","https://www.recipetineats.com/thai-basil-chicken-stir-fry/","thai","main","stir-fry",f))

# 22
f = write_md("Chicken with Creamy Sun Dried Tomato Sauce","https://www.recipetineats.com/chicken-with-creamy-sun-dried-tomato-sauce","italian","main","stovetop","10 mins","10 mins","20 mins","4-5 servings",
"A quick flavorful 1980s-inspired dish featuring chicken in a rich creamy sun-dried tomato sauce. Uses the oil from the sun-dried tomato jar to cook the chicken - free flavor!",
["750g / 1.5 lb chicken thighs or breast","1/2 cup sun-dried tomatoes (in oil drained; reserve oil)","2 tbsp oil from sun-dried tomato jar","2 garlic cloves minced 1/2 cup white wine","3/4 cup low-sodium chicken broth 3/4 cup heavy cream","1/3 cup finely shredded Parmesan 2 tsp Dijon mustard","1 cup packed fresh basil leaves salt and pepper"],
["If using breast slice horizontally into thin steaks. Season with salt and pepper.","Heat sun-dried tomato oil in large skillet over high heat.","Cook chicken: thighs ~6 min total breast ~4 min total. Remove and keep warm.","Sauté garlic for 15 sec. Deglaze with wine simmer 1 min.","Add mustard broth cream Parmesan and sun-dried tomatoes. Simmer 2-3 min.","Stir in basil return chicken to pan spoon sauce over. Serve immediately."],
["Use oil-packed sun-dried tomatoes for best flavor","Parmesan must be finely grated - avoid sandy pre-grated versions","Many readers recommend doubling the sauce - it's ridiculously addictive"],
"Calories: 529 kcal | Protein: 42g | Fat: 33g | Carbs: 11g | Sodium: 831mg")
link(f,"italian","main","stovetop"); recipes_meta.append(("Chicken with Creamy Sun Dried Tomato Sauce","https://www.recipetineats.com/chicken-with-creamy-sun-dried-tomato-sauce","italian","main","stovetop",f))

# 23
f = write_md("Pad Kee Mao (Thai Drunken Noodles)","https://www.recipetineats.com/pad-kee-mao-thai-drunken-noodles","thai","main","stir-fry","10 mins","6 mins","16 mins","2-3 servings",
"Drunken Noodles - spicy and savory featuring Thai Basil and significant heat. Unlike Pad Thai (nutty/sweet) or Pad See Ew (dark/sweet) Pad Kee Mao is spicy and savory with Thai Basil.",
["7 oz / 200g dried wide rice noodles","2 tbsp oil 3 large garlic cloves minced 2 bird's eye chillies deseeded & chopped","1/2 onion sliced 200g / 7oz chicken thighs (bite-size pieces)","2 tsp fish sauce 2 green onions (3cm pieces) 1 cup Thai Basil leaves","Sauce: 3 tbsp oyster sauce 1 1/2 tbsp light soy sauce 1 1/2 tbsp dark soy sauce 2 tsp sugar 1 tbsp water"],
["Prepare noodles per packet directions. Mix sauce ingredients.","Heat oil in wok over high heat. Add garlic and chili cook 10 sec.","Add onion cook 1 min. Add chicken and fish sauce fry until cooked (~2 min).","Add green onion noodles and sauce. Cook 1 min until sauce reduces and coats noodles.","Remove from heat add basil toss until just wilted. Serve immediately."],
["Have everything prepped and ready - entire cook time is only ~6 min","Regular basil is the best substitute for Thai Basil","Common additions: broccolini Chinese broccoli bell peppers baby corn spinach"],
"Calories: 454 kcal | Protein: 22.9g | Fat: 14.8g | Carbs: 58.6g | Sodium: 223mg")
link(f,"thai","main","stir-fry"); recipes_meta.append(("Pad Kee Mao (Thai Drunken Noodles)","https://www.recipetineats.com/pad-kee-mao-thai-drunken-noodles","thai","main","stir-fry",f))

# 24
f = write_md("Jambalaya Recipe","https://www.recipetineats.com/jambalaya-recipe/","american","main","one-pot","20 mins","50 mins","1 hour 10 mins","5 servings",
"One of New Orleans' most iconic and beloved dishes! A Creole-style Jambalaya featuring shrimp smoked sausage chicken bacon and rice cooked in a spiced tomato broth with the holy trinity of onion celery and bell pepper.",
["180g smoked bacon 200g andouille or smoked sausage 300g chicken thigh 12 large raw prawns/shrimp","1 large onion 2 celery ribs 2 green bell peppers 4 garlic cloves 1 cup sliced green onions","1.25 cups long grain white rice 2.5 cups chicken broth 200g crushed canned tomato 2 tbsp tomato paste","Creole Seasoning: 2 tsp thyme 4 tsp sweet paprika 1 tsp garlic powder 1 tsp onion powder 1/2 tsp cayenne 1/2 tsp black pepper 1/2 tsp salt"],
["Preheat oven to 180C (350F). Sear meats in large oven-safe pot.","Sauté vegetables: garlic onion celery bell pepper cook 3-4 min.","Add rice and liquids: broth tomato paste crushed tomatoes seasoning. Return meats.","Bake covered 20 min. Check rice - should be soft but still hold shape.","Add prawns and green onions. Cover and bake 3 min more.","Rest off heat fluff gently garnish with extra green onions."],
["BAKE IT! Skip the mushy rice - oven baking is stress-free Jambalaya perfection","Andouille substitute: smoked European sausages (kielbasa) or kransky/chorizo + smoked bacon + smoked paprika","Use only regular white rice (not brown risotto paella or wild)"],
"Calories: 707 kcal | Protein: 31g | Fat: 41g | Carbs: 51g | Sodium: 1563mg")
link(f,"american","main","one-pot"); recipes_meta.append(("Jambalaya Recipe","https://www.recipetineats.com/jambalaya-recipe/","american","main","one-pot",f))

# 25
f = write_md("Chicken Pasta Recipe","https://www.recipetineats.com/chicken-pasta-recipe/","italian","main","stovetop","5 mins","15 mins","20 mins","4 servings",
"A rich creamy Chicken Alfredo Pasta loaded with sun-dried tomatoes spinach and bacon. The pasta you make when you've had a bad day and need a pick me up!",
["300g / 10 oz fettuccine (dried)","2 chicken breasts (butterflied) 70g / 2.5oz baby spinach","100g / 3oz sun-dried tomato strips 120g / 4oz cooked crumbled bacon","30g / 2 tbsp butter 1 1/4 cups heavy cream 3/4 cup finely shredded Parmesan","1/2 cup dry white wine 1/2 cup low-sodium chicken stock"],
["Cook fettuccine 1.5 min less than package time. Reserve 1 cup pasta water.","Season chicken cook in butter over high heat 2 min per side. Shred with forks.","Make Alfredo sauce: sauté garlic add wine simmer. Add broth cream Parmesan sun-dried tomatoes.","Simmer 3-5 min until thickened. Add spinach shredded chicken and cooked pasta.","Toss 1.5-2 min until sauce coats pasta. Adjust with pasta water if needed.","Serve topped with bacon extra Parmesan and parsley."],
["Wine adds depth and a restaurant edge","Parmesan must be freshly grated or finely shredded - not powdery pre-grated","Reserve pasta water - starchy water helps adjust sauce consistency"],
"Calories: 887 kcal | Protein: 44g | Fat: 50g | Carbs: 72g | Sodium: 961mg")
link(f,"italian","main","stovetop"); recipes_meta.append(("Chicken Pasta Recipe","https://www.recipetineats.com/chicken-pasta-recipe/","italian","main","stovetop",f))

# 26
f = write_md("Chinese Cashew Chicken","https://www.recipetineats.com/chinese-cashew-chicken/","chinese","main","stir-fry","15 mins","6 mins","21 mins","4 servings",
"A saucy chicken stir fry with cashews that rivals your favorite Chinese restaurant takeout. Faster than delivery healthier (less greasy) and highly customizable with vegetables.",
["Sauce: 1 tbsp cornstarch 3 tbsp soy sauce 1 1/2 tbsp Chinese cooking wine 3 tbsp oyster sauce 2 tsp sesame oil white pepper","500g / 1 lb chicken thigh (cut into 2.5cm pieces)","2 tbsp peanut oil 2 garlic cloves 1/2 onion 1 green capsicum","6 tbsp water 3/4 cup roasted cashews (unsalted)"],
["Mix cornstarch and soy sauce until no lumps. Add remaining sauce ingredients.","Transfer 2 tbsp sauce to chicken mix to coat. Set aside 10+ min.","Heat oil over high heat. Add garlic and onion cook 1 min.","Add chicken cook 2 min. Add capsicum cook 1 min.","Add sauce and water. Simmer 1 min until sauce thickens.","Stir through cashews. Serve immediately with rice."],
["Chinese Cooking Wine (Shaoxing) is the secret ingredient for authentic takeout flavor","Chicken thigh preferred; breast works with velveting technique","Plenty of sauce - no sad plain rice left behind"],
"Calories: 559 kcal | Protein: 32g | Fat: 28g | Carbs: 22g | Sodium: 1089mg")
link(f,"chinese","main","stir-fry"); recipes_meta.append(("Chinese Cashew Chicken","https://www.recipetineats.com/chinese-cashew-chicken/","chinese","main","stir-fry",f))

# 27
f = write_md("Chicken Pot Pie","https://www.recipetineats.com/chicken-pot-pie/","american","main","baked","15 mins","1 hour","1 hour 15 mins","4-6 servings",
"A comforting freezer-friendly Chicken Pot Pie with a creamy herb-infused filling and golden puff pastry lids. Designed for individual pots to maximize pastry-to-filling ratio.",
["600g / 1.2 lb chicken breast 2 cups milk 1 cup chicken broth","2 tsp chicken or vegetable stock powder 2 sprigs thyme","1 large onion 2 large carrots 3 celery ribs 2 garlic cloves","50g butter 1 tsp dried thyme 1/3 cup white wine 1/3 cup flour","1/2 cup grated Parmesan 1 cup frozen peas 2 sheets puff pastry","1 egg (lightly whisked for egg wash)"],
["Poach chicken in milk + broth + stock powder. Simmer 15 min. Shred chicken reserve liquid.","Make filling: sauté onion garlic carrots celery. Add wine then flour. Gradually add poaching liquid.","Add Parmesan pepper chicken peas. Cook 3 min until thickened.","Cool filling in fridge >= 30 min (critical for puff pastry rise).","Preheat oven to 180C / 350F. Cut puff pastry rounds 2.5cm wider than pot openings.","Brush pot rims with egg wash drape pastry over. Brush tops with egg cut slit.","Bake 35-40 min until deep golden."],
["Thicken filling fully on stove - sauce won't reduce further under pastry","Cool filling completely - hot filling melts butter in pastry reducing puff","Freeze uncooked pies up to 3 months. Thaw overnight before baking."],
"Calories: 588 kcal | Protein: 47g | Fat: 26g | Carbs: 36g | Sodium: 1191mg")
link(f,"american","main","baked"); recipes_meta.append(("Chicken Pot Pie","https://www.recipetineats.com/chicken-pot-pie/","american","main","baked",f))

# 28
f = write_md("Lemon Chicken Salad","https://www.recipetineats.com/lemon-chicken-salad/","american","salad","stovetop","15 mins","8 mins","23 mins","2-4 servings",
"A mouthwatering Lemon Chicken Salad with a bright lemon dressing with a touch of honey that does double duty as a quick marinade for the chicken.",
["Dressing: 2 tsp lemon zest 2 tbsp lemon juice 1 tbsp honey 1 tsp Dijon mustard 3 tbsp olive oil 1 garlic clove salt pepper","1 large chicken breast (halved horizontally) OR 2 boneless skinless thighs","2 tbsp finely chopped dill 8 cups cos/romaine lettuce","1 cup cherry tomatoes 1 medium avocado 1/2 small red onion","3/4 cup corn kernels 120g bacon (optional)"],
["Make dressing: shake all dressing ingredients in a jar.","Marinate chicken with 2 tbsp dressing + 1 tbsp extra lemon juice. Min 20 min.","Cook chicken: breasts 2 min/side thighs 4 min/side. Rest 3 min then slice.","Add dill into remaining dressing. Shake.","Assemble salad: lettuce tomatoes avocado onion corn. Top with chicken.","Drizzle dressing crumble bacon if using. Serve immediately."],
["Lemon zest is essential - lemon juice is just sour all the flavor is in the skin","Both chicken breast and thighs work great","Meal prep: use chicken thigh (juicier reheated)"],
"Calories: 587 kcal per serving (assuming 2 servings)")
link(f,"american","salad","stovetop"); recipes_meta.append(("Lemon Chicken Salad","https://www.recipetineats.com/lemon-chicken-salad/","american","salad","stovetop",f))

# 29
f = write_md("Mexican Chicken Avocado Salad","https://www.recipetineats.com/mexican-chicken-avocado-salad/","mexican","salad","stovetop","15 mins","8 mins","23 mins + 30 min marination","3 servings",
"A vibrant filling Mexican-inspired salad featuring Mexican marinated grilled chicken avocado-tomato-corn salsa and fresh lime-cilantro dressing. A complete meal - not a side salad.",
["Lime Dressing: 2 tbsp lime juice 1 tbsp honey 1/4 cup olive oil 1 garlic clove salt pepper","2 small chicken breasts (400g) 1/2 tsp chipotle powder 1/2 tsp oregano 1/4 tsp cumin","Avocado Salsa: 1 avocado 1 cup cherry tomatoes 3/4 cup corn 1/2 red onion","1/4 cup coriander/cilantro 5 heaped cups cos/romaine lettuce"],
["Make dressing: combine in jar shake well.","Marinate chicken: reserve 2 tbsp dressing + chipotle oregano cumin. Marinate 30 min.","Cook chicken: heat oil cook ~8 min until browned. Rest 5 min slice.","Finish dressing: add 2 tbsp cilantro to remaining dressing.","Make salsa: combine avocado tomatoes corn onion cilantro drizzle of dressing.","Assemble: toss lettuce with dressing top with salsa and chicken."],
["Chipotle powder substitute: 1/4 tsp smoked paprika + pinch each of chilli powder coriander cumin","Triple-duty dressing: salad dressing salsa dressing and chicken marinade","For lunch prep: keep dressing separate until serving"],
"Calories: 487 kcal per serving (3 servings)")
link(f,"mexican","salad","stovetop"); recipes_meta.append(("Mexican Chicken Avocado Salad","https://www.recipetineats.com/mexican-chicken-avocado-salad/","mexican","salad","stovetop",f))

# 30
f = write_md("Oven Baked Chicken and Rice Pilaf (Cranberry Walnut Apple)","https://www.recipetineats.com/oven-baked-chicken-and-rice-pilaf-cranberry-walnut-apple/","american","main","baked","15 mins","1 hour 5 mins","1 hour 20 mins","5 servings",
"A festive-inspired one-pan oven-baked dinner featuring sticky glazed chicken served over fluffy rice pilaf cooked in apple juice broth with cranberries walnuts and fresh apple.",
["5 bone-in skinless chicken thigh fillets (~220g each)","Rice Pilaf: 1 small onion 1 garlic clove 50g butter 1 1/2 cups long-grain white rice","1 1/4 cups apple juice 1 1/2 cups chicken broth 1 cup dried cranberries 1 cup walnuts","1 red apple (small dice) 3/4 tsp dried rosemary 1 tsp dried thyme salt pepper","Sticky Glaze: 1/3 cup apricot jam 2 1/2 tbsp Dijon mustard 1/2 tsp garlic powder 1/2 tsp All Spice 1/4 tsp paprika salt pepper"],
["Preheat oven to 200C (390F). Sauté onion and garlic in butter in baking dish bake 15 min.","Prep chicken: remove skin coat with glaze. Set aside.","Build pilaf: add rice apple juice broth herbs cranberries and walnuts to dish. Stir.","Add chicken on top (partially submerged). Cover with foil. Bake 20 min.","Uncover spoon remaining glaze onto chicken. Bake uncovered 30-35 min.","Rest 5 min. Remove chicken add diced apple fluff rice with fork. Garnish with parsley."],
["Precise liquid-to-rice ratio is essential: 1.5 cups rice : 2.625 cups total liquid","Fresh apple is added after baking to preserve texture","Don't stir rice during baking. Fluff with fork only after resting."],
"Calories: 718 kcal | Protein: 55g | Fat: 35g | Carbs: 45g")
link(f,"american","main","baked"); recipes_meta.append(("Oven Baked Chicken and Rice Pilaf (Cranberry Walnut Apple)","https://www.recipetineats.com/oven-baked-chicken-and-rice-pilaf-cranberry-walnut-apple/","american","main","baked",f))

# 31
f = write_md("Vietnamese Coconut Caramel Chicken","https://www.recipetineats.com/vietnamese-coconut-caramel-chicken","vietnamese","main","stovetop","5 mins","55 mins","1 hour","4-5 servings",
"A magical easy Vietnamese chicken recipe. Slow-cooked in coconut milk with Vietnamese flavorings until it reduces down to a sweet-savoury glaze. The chicken version of the wildly popular Vietnamese Caramel Pork.",
["4 large or 5 small chicken thighs (bone-in skin-on)","1/2 cup (80g) brown sugar 1 tbsp water","400g (14 oz) coconut milk (low-fat) 1 1/2 tbsp fish sauce","2 1/2 tbsp rice vinegar 2 garlic cloves minced","1 eschalot/French onion finely sliced 1/4 tsp white pepper"],
["Make caramel: combine sugar and water in skillet over medium heat. Stir until melted and bubbling.","Add liquids: stir in coconut milk fish sauce vinegar garlic eschallot and pepper.","Add chicken skin side down. Adjust heat to energetic simmer.","After 25 min turn chicken. After another 25 min fat should separate and turn pale brown.","Brown skin: flip skin-side down move chicken to prevent sticking and brown skin.","Serve with jasmine rice garnished with shallots and chili."],
["Bone-in skin-on thigh fillets are recommended","The fat separates at the end - avoid spooning it over rice","Serve with Asian Slaw or steamed veggies"],
"Calories: 555 kcal per serving (5 servings)")
link(f,"vietnamese","main","stovetop"); recipes_meta.append(("Vietnamese Coconut Caramel Chicken","https://www.recipetineats.com/vietnamese-coconut-caramel-chicken","vietnamese","main","stovetop",f))

# 32
f = write_md("Thai Coconut Chicken","https://www.recipetineats.com/thai-coconut-chicken/","thai","main","grilled","10 mins","10 mins","25 mins + 24-48 hrs marinating","5 servings",
"A flavorful Thai-inspired coconut chicken with chicken marinated in a rich aromatic coconut milk-based Thai marinade. Served with a creamy Coconut Peanut Sauce.",
["Marinade: 1 tsp garlic 1 tsp ginger 1 tsp chilli 1 lemongrass stalk 1 1/2 tsp coriander powder 3/4 tsp turmeric 1/2 tsp curry powder 1 tbsp brown sugar 2 1/2 tbsp fish sauce 3/4 cup full-fat coconut milk","750g - 1 kg boneless skinless chicken thighs","Coconut Peanut Sauce: 1/2 cup coconut milk 1 tbsp peanut butter 2 tbsp hoisin sauce 1 1/2 tbsp lime juice 1 garlic clove 1/2 tsp chilli paste"],
["Mix marinade add chicken coat well. Marinate 24-48 hours.","Preheat BBQ or skillet over medium heat.","Cook first side ~5 min until golden. Flip and cook second side ~4 min.","Rest 5 min under foil before serving.","Make Coconut Peanut Sauce: mix all ingredients microwave 30 sec stir until smooth.","Serve with jasmine rice coconut rice or Thai fried rice."],
["Freeze chicken in marinade for later use","Baking: drumsticks/wings 45 min at 180C; bone-in thighs 50 min","Chicken breast: cut in half horizontally cook 3 min per side"],
"Calories: 436 kcal per serving (5 servings)")
link(f,"thai","main","grilled"); recipes_meta.append(("Thai Coconut Chicken","https://www.recipetineats.com/thai-coconut-chicken/","thai","main","grilled",f))

# 33
f = write_md("Oven Baked Chicken Quesadillas","https://www.recipetineats.com/oven-baked-chicken-quesadillas/","mexican","main","baked","15 mins","16 mins","31 mins","4 servings",
"Batch cooking crispy chicken quesadillas in the oven - no need to cook them one-by-one on the stovetop. The filling mirrors Chicken Fajitas.",
["400g chicken (thigh breast or tenderloin) bite-sized pieces","1 tsp cumin 1 tsp garlic powder 1/2 tsp cayenne 1 tsp paprika salt pepper","1 tbsp olive oil 1/2 small onion 1 garlic clove 1 red + 1 green capsicum","4 flour tortillas (20cm / 8\") olive oil spray 1 cup grated melting cheese"],
["Season and cook chicken: toss with spices sauté until browned. Cool completely.","Sauté vegetables: onion garlic capsicums. Combine with chicken; cool.","Preheat oven & tray: 220C/430F (or 200C/390F fan). Spray tray with oil heat in oven.","Assemble: divide filling over half of each tortilla top with cheese fold in half.","Bake on hot tray (should sizzle). Bake 8 min per side flipping once.","Serve immediately for maximum crispiness."],
["Cool filling before assembly - hot filling creates steam and prevents crispiness","Preheat an oiled baking tray for immediate sizzling","Make-ahead: prepare filling hours in advance refrigerate"],
"Calories: 448 kcal | Protein: 35g | Fat: 24.3g | Carbs: 22.8g | Sodium: 561mg")
link(f,"mexican","main","baked"); recipes_meta.append(("Oven Baked Chicken Quesadillas","https://www.recipetineats.com/oven-baked-chicken-quesadillas/","mexican","main","baked",f))

# 34
f = write_md("Creamy Chicken and Bacon Pasta","https://www.recipetineats.com/creamy-chicken-and-bacon-pasta/","italian","main","stovetop","5 mins","15 mins","20 mins","2 generous servings",
"A rich indulgent pasta dish for those days when nothing but a creamy pasta will do. Unapologetically loaded with cream parmesan chicken and bacon.",
["6 oz / 180 g fettuccine 5-7 oz / 150-200g bacon (chopped)","6 oz / 180g chicken breast (butterflied) salt pepper","1 tbsp butter 2 garlic cloves 1/2 small onion","3/4 cup heavy cream 1/2 cup finely shredded parmesan","Fresh parsley extra parmesan for serving"],
["Cook pasta 2 min less than package. Reserve 3/4 cup pasta water.","Cook bacon until golden. Remove keep fat in pan.","Cook chicken in bacon fat (2 mins/side). Slice when cool.","Sauté onion & garlic in butter 3-4 min.","Make sauce: add cream 3/4 cup pasta water parmesan salt pepper. Simmer 2 min.","Toss pasta in sauce over heat ~1.5 min until thickened.","Add bacon + chicken. Serve with parsley & extra parmesan."],
["Reserve pasta water - starch helps emulsify and thicken the sauce","Parmesan: freshly grated melts smoother than pre-grated","Using ham instead of bacon reduces calories significantly"],
"Calories: 946 kcal | Protein: 57.4g | Fat: 54.6g | Carbs: 72g")
link(f,"italian","main","stovetop"); recipes_meta.append(("Creamy Chicken and Bacon Pasta","https://www.recipetineats.com/creamy-chicken-and-bacon-pasta/","italian","main","stovetop",f))

# 35
f = write_md("Chicken and Mushroom Risotto","https://www.recipetineats.com/chicken-and-mushroom-risotto","italian","main","stovetop","10 mins","40 mins","50 mins","4 servings",
"A creamy flavorful Chicken and Mushroom Risotto that defies traditional risotto myths. No constant stirring no gradual broth addition no need to heat the broth.",
["2.5 oz (75g) bacon 12 oz (350g) chicken thigh 13 oz (400g) mushrooms (Swiss brown)","2 tbsp butter 2 garlic cloves 1 onion 1/2 cup white wine","1 1/4 cups (250g) Arborio rice 4 cups (1L) chicken broth","1/2 cup freshly grated Parmesan 1-3 tbsp butter fresh parsley"],
["Cook bacon until golden. Brown chicken in bacon fat. Sauté mushrooms until golden.","Sauté onion & garlic in butter. Toast rice 1 min.","Deglaze with wine. Add 3 cups stock simmer uncovered stir 1-2 times.","Add remaining stock 1/2 cup at a time stirring occasionally until rice is al dente.","Return chicken & mushrooms. Off heat: add splash of broth + butter + Parmesan. Stir vigorously.","Serve immediately with bacon extra Parmesan parsley."],
["Use Arborio rice - high starch content = creamy texture","Don't over-toast rice - max 1 minute","Finish vigorously - stir in butter and parmesan off-heat for silkiness","Serve immediately - risotto thickens as it sits"],
"Calories: 658 kcal | Protein: 41.9g | Fat: 24.8g | Carbs: 59.7g | Sodium: 1274mg")
link(f,"italian","main","stovetop"); recipes_meta.append(("Chicken and Mushroom Risotto","https://www.recipetineats.com/chicken-and-mushroom-risotto","italian","main","stovetop",f))

# 36
f = write_md("Mexican Shredded Chicken","https://www.recipetineats.com/mexican-shredded-chicken/","mexican","main","slow-cooker","10 mins","4 hours (slow cooker)","4 hours 10 mins","5-6 servings",
"Fast-prep big-flavor shredded chicken breast in a smoky mildly spicy chipotle-loaded red sauce. Use for tacos enchiladas burritos quesadillas soups rice bowls and more.",
["1.5 lb (750g) boneless skinless chicken breast","1/2 cup Chipotles in Adobo Sauce (4 chillies + sauce)","14 oz (400g) can crushed tomatoes 2 garlic cloves","1 tsp each: dried oregano cumin powder onion powder 2 tsp sugar","3/4 tsp salt pepper 3 tbsp olive oil 2 tbsp lime juice"],
["Cook chicken: slow cooker 4 hours on low pressure cooker 35 min or stovetop 40-50 min.","Make sauce: remove chicken shred. Add lime juice + 1 tbsp oil to cooking liquid. Puree until smooth.","Brown chicken (optional but recommended): fry in oil until dark golden brown on one side.","Toss chicken in sauce or serve sauce on the side."],
["Chipotles in Adobo Sauce is the key ingredient - like soy sauce for Mexican cooking","Browning the chicken adds caramelized texture and depth","Freezes beautifully - freeze shredded chicken and sauce separately"],
"Calories: 297 kcal | Protein: 41.5g | Fat: 12.1g | Carbs: 6.4g | Sodium: 794mg")
link(f,"mexican","main","slow-cooker"); recipes_meta.append(("Mexican Shredded Chicken","https://www.recipetineats.com/mexican-shredded-chicken/","mexican","main","slow-cooker",f))

# 37
f = write_md("One Pot Chicken Enchilada Rice Casserole","https://www.recipetineats.com/one-pot-chicken-enchilada-rice-casserole/","mexican","main","one-pot","15 mins","25 mins","40 mins","5-6 servings",
"A flavorful easy midweek meal that captures the essence of chicken enchiladas in a one-pot rice casserole. Made entirely on the stovetop with pantry staples.",
["400g (13 oz) chicken breast (thinly sliced) 1 tbsp olive oil","1 small onion 3 garlic cloves 1 red bell pepper 680g tomato passata","3 cups chicken broth 1 1/2 cups frozen corn 1 1/2 cups white rice","Enchilada spices: 1/2 tsp cayenne 1 tbsp oregano 2 tsp cumin 1 1/2 tsp coriander 2 tsp onion powder 1 tbsp brown sugar","1-1 1/2 cups grated cheese cilantro for garnish"],
["Cook chicken in large skillet 2 min per side. Remove.","Sauté onion garlic bell pepper. Add passata broth corn and spices.","Add rice cover cook 15-18 min without stirring until rice is tender.","Shred chicken stir into rice. Top with cheese broil until golden.","Garnish with cilantro."],
["Don't overcook the rice - should be tender but not mushy","Remove while still saucy - rice continues absorbing liquid off-heat","Use only regular white rice (not brown risotto paella or wild)"],
"Calories: 490 kcal per serving (6 servings)")
link(f,"mexican","main","one-pot"); recipes_meta.append(("One Pot Chicken Enchilada Rice Casserole","https://www.recipetineats.com/one-pot-chicken-enchilada-rice-casserole/","mexican","main","one-pot",f))

# 38
f = write_md("One Pot Creamy Parmesan Garlic Risotto with Lemon Pepper Chicken","https://www.recipetineats.com/one-pot-creamy-parmesan-garlic-risotto-with-lemon-pepper-chicken/","italian","main","one-pot","10 mins","50 mins","1 hour","5 servings",
"A one-pot wonder delivering two dishes in one: creamy dreamy Parmesan garlic risotto AND crispy roasted lemon pepper chicken. The chicken roasts directly on top of the rice infusing it with rich concentrated flavor.",
["2 lb / 1 kg bone-in skin-on chicken thighs (5 pieces) 2-3 tbsp Lemon Pepper Seasoning","2 tbsp butter 4 garlic cloves 1 onion 1 1/2 cups risotto rice (arborio)","1/2 cup white wine 4 cups chicken broth 1 cup milk salt pepper","1 cup freshly grated Parmesan 2 tbsp butter 1/2 to 1 cup milk fresh herbs"],
["Preheat oven to 180C/350F. Coat chicken with Lemon Pepper Seasoning.","Sear chicken skin-side down until golden. Remove discard excess oil.","Melt butter sauté garlic and onion 2 min. Add rice stir until translucent.","Add wine cook 1-2 min. Add broth milk salt pepper. Bring to simmer.","Place chicken on top. Cover bake 20 min then 10 min uncovered.","Remove chicken. Stir in Parmesan butter and warm milk. Return chicken on top."],
["Bone-in skin-on thighs are best","Lemon Pepper Seasoning: store-bought blend ~$1.50/packet","Don't skip the simmer before baking to avoid excess liquid"],
"Calories: 626 kcal | Protein: 44.5g | Fat: 22.5g | Carbs: 54.9g | Sodium: 862mg")
link(f,"italian","main","one-pot"); recipes_meta.append(("One Pot Creamy Parmesan Garlic Risotto with Lemon Pepper Chicken","https://www.recipetineats.com/one-pot-creamy-parmesan-garlic-risotto-with-lemon-pepper-chicken/","italian","main","one-pot",f))

# 39
f = write_md("One Pot Greek Chicken Lemon Rice","https://www.recipetineats.com/one-pot-greek-chicken-lemon-rice/","greek","main","one-pot","10 mins","50 mins","1 hour","5 servings",
"People have said this is the best chicken and rice recipe they've ever had. The real star is the RICE - cooked directly beneath the chicken absorbing all its juices like triple strength chicken stock.",
["5 bone-in skin-on chicken thighs (~1 kg / 2 lb)","Zest + 4 tbsp juice from 1-2 lemons 1 tbsp dried oregano 4 garlic cloves 1/2 tsp salt","1 1/2 tbsp olive oil 1 small onion 1 cup (180g) uncooked long-grain white rice","1 1/2 cups chicken broth 3/4 cup water 1 tbsp dried oregano 3/4 tsp salt pepper","Fresh parsley or oregano fresh lemon zest"],
["Marinate chicken with marinade in ziplock bag. Refrigerate >= 20 min preferably overnight.","Preheat oven to 180C / 350F. Sear chicken skin-side down until golden. Remove.","Deglaze pan pour off fat wipe clean. Heat oil sauté onion until translucent.","Add rice broth water oregano salt pepper and reserved marinade. Simmer 30 sec.","Place chicken on top. Cover with lid or foil. Bake 35 min covered then 10 min uncovered.","Rest 5-10 min. Garnish with herbs and lemon zest."],
["Bone-in skin-on thighs are best for flavor","Long-grain white rice recommended (least sticky)","Fresh oregano + lemon zest = absolute must"],
"Calories: 667 kcal | Protein: 75.9g | Fat: 23.4g | Carbs: 34.2g | Sodium: 1408mg")
link(f,"greek","main","one-pot"); recipes_meta.append(("One Pot Greek Chicken Lemon Rice","https://www.recipetineats.com/one-pot-greek-chicken-lemon-rice/","greek","main","one-pot",f))

# 40
f = write_md("Jamaican Jerk Chicken Drumsticks with Caribbean Rice and Beans","https://www.recipetineats.com/jamaican-jerk-chicken-drumsticks-with-caribbean-rice-with-beans","jamaican","main","baked","15 mins","50 mins","1 hour 5 mins","4 servings",
"Big big BIG flavours. Spicy. Punchy. Salty. Sweet. Jamaican Jerk Chicken with Caribbean Rice with Peas (Beans).",
["8 chicken drumsticks (~2.5 lb / 1.2 kg)","Marinade: 2 tbsp olive oil 1 tbsp soy sauce juice of 1 lime 1 onion 1 tbsp ginger 1+ scotch bonnet pepper 6 garlic cloves 2 tsp salt 2 tsp black pepper 3 tbsp brown sugar 1/2 tbsp cinnamon 1/2 tbsp allspice 1/2 tsp nutmeg 1/2 tsp dried thyme","Caribbean Rice: 2 tbsp oil 2 garlic 1/2 onion 1/2 tsp thyme 1 cup long grain rice 14 oz can red kidney beans 1 cup coconut milk 3/4 cup water 1 bay leaf 2 tsp Cajun spice 1/2 tsp paprika salt pepper"],
["Pat chicken dry. Blend marinade in food processor. Marinate 4-24 hours.","Oven: bake at 180C basting with marinade at 25 min and 40 min until dark brown.","Rice: sauté garlic onion thyme. Add rice beans coconut milk water bay leaf spices.","Bring to boil reduce heat cover cook 20 min. Rest 10 min before serving."],
["Scotch bonnet pepper is very hot - use gloves","Air fryer option: 10 min at 400F flip + marinade 8 more min","Freezable marinade - make extra and freeze"],
"Chicken: Calories: 268 kcal | Protein: 26.4g | Fat: 12.4g | Rice: Calories: 236 kcal | Protein: 6.1g | Carbs: 37.6g")
link(f,"jamaican","main","baked"); recipes_meta.append(("Jamaican Jerk Chicken Drumsticks with Caribbean Rice and Beans","https://www.recipetineats.com/jamaican-jerk-chicken-drumsticks-with-caribbean-rice-with-beans","jamaican","main","baked",f))

# 41
f = write_md("One Pan Spanish Chicken Chorizo Tomato Potatoes","https://www.recipetineats.com/one-pan-spanish-chicken-chorizo-tomato-potatoes/","spanish","main","baked","15 mins","50 mins","1 hour 5 mins","4 servings",
"A flavorful one-pan Spanish-inspired dish featuring chicken chorizo potatoes tomatoes and capsicum. The chorizo releases rich spicy juices that form the base of the sauce.",
["4 chicken thigh fillets (bone-in skin-on ~250g each)","8-12 baby potatoes halved 2 chorizo sausages sliced","2 garlic cloves 1 small red capsicum 1 small red onion","1 can (15oz/400g) crushed tomatoes 1 tbsp dried oregano","1/2-1 punnet cherry tomatoes","Rub: 2 tbsp lemon juice 1 1/2 tbsp paprika 1/4-1/2 tsp cayenne 1 1/2 tsp salt pepper"],
["Preheat oven to 350F/180C. Make rub slather over chicken.","Par-cook potatoes. Sear chicken skin-side down until golden. Brown chorizo.","Sauté garlic capsicum onion 2 min. Add crushed tomatoes and oregano.","Add potatoes chicken chorizo cherry tomatoes. Nestle chicken in tomato.","Cover bake 30-40 min until chicken is cooked through and dark brown."],
["Bone-in skin-on thighs preferred","Cured chorizo from deli (not raw)","Stovetop option: simmer instead of baking"],
"Calories: 773 kcal | Protein: 50.7g | Fat: 45.2g | Carbs: 39.4g | Sodium: 1690mg")
link(f,"spanish","main","baked"); recipes_meta.append(("One Pan Spanish Chicken Chorizo Tomato Potatoes","https://www.recipetineats.com/one-pan-spanish-chicken-chorizo-tomato-potatoes/","spanish","main","baked",f))

# 42
f = write_md("Crispy Shredded Chicken Noodle Stir Fry","https://www.recipetineats.com/crispy-shredded-chicken-noodle-stir-fry/","chinese","main","stir-fry","5 mins","5 mins","10 mins","2 servings",
"A 10-minute stir fry using both the meat and braising liquid from Slow Cooker Crispy Chinese Shredded Chicken. Off the charts for effort vs output.",
["5 oz / 150g dried rice stick noodles","2 tbsp oil 2 garlic cloves smashed","1 cup Slow Cooker Crispy Chinese Shredded Chicken","1/2 cup braising liquid (from slow cooker) 1 tbsp Sriracha","3 cups Chinese broccoli (leaves separated stems cut thin)"],
["Cook/soak rice stick noodles per packet. Drain.","Heat oil in wok over high heat. Add smashed garlic stir 30 sec. Remove and discard.","Add Chinese broccoli stems + shredded chicken. Stir fry 1 1/2 min.","Add noodles braising liquid and Sriracha. Toss rapidly ~1 min.","Add Chinese broccoli leaves toss to mix. Remove from heat. Serve immediately."],
["Using smashed garlic prevents burning over high heat","The braising liquid doubles as stir fry sauce - rich complex flavor","Both chicken and braising liquid freeze well for 2-3 months"],
"Calories: 476 kcal | Protein: 27.7g | Fat: 16.3g | Carbs: 56.5g | Sodium: 394mg")
link(f,"chinese","main","stir-fry"); recipes_meta.append(("Crispy Shredded Chicken Noodle Stir Fry","https://www.recipetineats.com/crispy-shredded-chicken-noodle-stir-fry/","chinese","main","stir-fry",f))

# 43
f = write_md("10 Classic Chinese Dishes + Homemade Teriyaki Sauce","https://www.recipetineats.com/10-classic-chinese-dishes-1-amazing-sauce/","chinese","main","stir-fry","15 mins","15 mins","30 mins","Varies",
"10 great stir fry recipes using one AMAZING all-purpose stir fry sauce called 'Charlie'. All on the table in less than 15 minutes. Includes Chicken Chow Mein Cashew Chicken Pad See Ew Beef and Broccoli Shanghai Noodles and more.",
["Charlie All-Purpose Stir Fry Sauce: soy sauce oyster sauce Chinese cooking wine sesame oil sugar white pepper cornstarch","10 recipes include: Chicken Chow Mein Supreme Soy Sauce Chow Mein Hokkien Noodles Stir Fried Chicken with Vegetables Stir Fried Snow Peas with Beef Cashew Chicken Pad See Ew Stir Fried Beef and Broccoli Shanghai Noodles Cantonese Rice Noodles with Beef","Each recipe uses Charlie sauce + water + protein + vegetables + noodles (where applicable)"],
["Make Charlie sauce: mix all sauce ingredients store in fridge for weeks.","For each stir fry: prep all ingredients first (stir-fries move fast).","Heat wok/skillet over high heat. Cook protein then vegetables.","Add Charlie sauce + water. Toss until sauce thickens and coats ingredients.","Serve immediately over rice or noodles."],
["Charlie sauce is not an exact replica of any single recipe but very close to many","Having everything prepped before cooking is essential","Each recipe serves 2-4 people"],
"Varies by recipe - see individual recipes for nutrition details")
link(f,"chinese","main","stir-fry"); recipes_meta.append(("10 Classic Chinese Dishes + Homemade Teriyaki Sauce","https://www.recipetineats.com/10-classic-chinese-dishes-1-amazing-sauce/","chinese","main","stir-fry",f))

# ============================================================================
# REBUILD INDEX
# ============================================================================

# Read existing index to preserve non-RecipeTin recipes
index_path = VAULT / "index.json"
existing_recipes = []
if index_path.exists():
    try:
        old_index = json.loads(index_path.read_text())
        for r in old_index.get("recipes", []):
            # Keep recipes that are NOT from RecipeTin Eats (Mel's Kitchen etc.)
            if "recipetineats.com" not in r.get("url", ""):
                existing_recipes.append(r)
    except:
        pass

# Build new recipe entries
new_recipes = []
cuisines = {}
types = {}
methods = {}

for name, url, cuisine, rtype, method, fname in recipes_meta:
    fpath = RECIPES_DIR / fname
    size = fpath.stat().st_size if fpath.exists() else 0
    has_full = fname not in ("creamy_chicken_mushroom_fettucine.md", "creamy_tuscan_chicken_pasta_bake.md")
    
    new_recipes.append({
        "name": name,
        "file": "recipes/" + fname,
        "cuisines": [cuisine],
        "types": [rtype],
        "methods": [method],
        "has_full_content": has_full,
        "url": url,
        "size": size,
    })
    
    cuisines[cuisine] = cuisines.get(cuisine, 0) + 1
    types[rtype] = types.get(rtype, 0) + 1
    methods[method] = methods.get(method, 0) + 1

# Merge: existing non-RecipeTin recipes + new RecipeTin recipes
all_recipes = existing_recipes + new_recipes

# Recalculate totals
cuisines = {}
types = {}
methods = {}
for r in all_recipes:
    for c in r.get("cuisines", []):
        cuisines[c] = cuisines.get(c, 0) + 1
    for t in r.get("types", []):
        types[t] = types.get(t, 0) + 1
    for m in r.get("methods", []):
        methods[m] = methods.get(m, 0) + 1

index = {
    "generated": datetime.now().isoformat(),
    "total_recipes": len(all_recipes),
    "cuisines": dict(sorted(cuisines.items())),
    "types": dict(sorted(types.items())),
    "methods": dict(sorted(methods.items())),
    "recipes": all_recipes,
}

index_path.write_text(json.dumps(index, indent=2))

print(f"Done! Wrote {len(recipes_meta)} RecipeTin Eats recipes.")
print(f"Total vault size: {len(all_recipes)} recipes")
print(f"Cuisines: {dict(sorted(cuisines.items()))}")
print(f"Types: {dict(sorted(types.items()))}")
print(f"Methods: {dict(sorted(methods.items()))}")
