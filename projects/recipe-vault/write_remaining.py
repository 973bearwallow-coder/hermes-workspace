#!/usr/bin/env python3
"""
Create all remaining recipe files (15-43) for the RecipeTin Eats import.
Each file is written to recipes/ with full markdown format.
The finalize_vault.py script will copy them to by-cuisine/, by-type/, by-method/.
"""
import os

VAULT = os.path.expanduser("~/hermes-workspace/projects/recipe-vault")
RECIPES_DIR = os.path.join(VAULT, "recipes")
os.makedirs(RECIPES_DIR, exist_ok=True)

def make_content(name, url, cuisine, rtype, method, prep, cook, total, yield_s, desc, ingredients, instructions, tips, nutrition):
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
{desc}

## Ingredients
{ingredients}

## Instructions
{instructions}

## Tips & Notes
{tips}

## Nutrition
{nutrition}
"""

def write(name, url, cuisine, rtype, method, prep, cook, total, yield_s, desc, ingredients, instructions, tips, nutrition, filename):
    content = make_content(name, url, cuisine, rtype, method, prep, cook, total, yield_s, desc, ingredients, instructions, tips, nutrition)
    with open(os.path.join(RECIPES_DIR, filename), 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Written: {filename}")

# Recipe 15: Creamy Chicken Mushroom Fettuccine
write("Creamy Chicken Mushroom Fettuccine", "https://www.recipetineats.com/creamy-chicken-mushroom-fettuccine/",
    "italian", "main", "stovetop", "10 min", "20 min", "30 min", "4 servings",
    "A rich and creamy fettuccine pasta dish with tender chicken and mushrooms in a luscious cream sauce. Comfort food at its finest.",
    "- 400g / 14oz fettuccine pasta\n- 500g / 1 lb boneless, skinless chicken thighs, sliced\n- 300g / 10oz mushrooms, sliced\n- 3 cloves garlic, minced\n- 1 cup heavy/thickened cream\n- ½ cup chicken stock\n- ½ cup parmesan cheese, grated\n- 2 tbsp olive oil\n- 2 tbsp butter\n- Salt and pepper\n- Fresh parsley for garnish",
    "1. Cook fettuccine according to package directions. Reserve 1 cup pasta water.\n2. Season chicken with salt and pepper. Heat oil in large skillet over medium-high heat.\n3. Cook chicken until golden and cooked through. Remove.\n4. Add butter and mushrooms. Cook until golden. Add garlic, cook 1 min.\n5. Add cream and stock. Simmer 3–4 min until slightly thickened.\n6. Stir in parmesan until melted.\n7. Return chicken to sauce. Add pasta, toss to coat. Add pasta water if needed.\n8. Garnish with parsley and extra parmesan.",
    "- Thighs stay juicier than breast\n- Don't skip reserving pasta water—it helps the sauce cling\n- Leftovers: 3 days in fridge",
    "Per serving: Calories not specified",
    "creamy_chicken_mushroom_fettucine.md")

# Recipe 16: Creamy Tuscan Chicken Pasta Bake
write("Creamy Tuscan Chicken Pasta Bake", "https://www.recipetineats.com/creamy-tuscan-chicken-pasta-bake/",
    "italian", "main", "baked", "15 min", "35 min", "50 min", "4–6 servings",
    "A comforting baked pasta dish with chicken in a creamy sun-dried tomato and spinach sauce, topped with melted cheese. Like a Tuscan chicken dream in a baking dish.",
    "- 400g / 14oz penne or rigatoni\n- 500g / 1 lb boneless chicken thighs, diced\n- 1 cup sun-dried tomatoes, chopped\n- 3 cups baby spinach\n- 3 cloves garlic, minced\n- 1 cup heavy cream\n- ½ cup chicken stock\n- ½ cup parmesan, grated\n- 1 cup mozzarella, shredded\n- 2 tbsp olive oil\n- 1 tsp Italian herb blend\n- Salt and pepper",
    "1. Preheat oven to 200°C/400°F. Cook pasta 2 minutes less than package directions.\n2. Season chicken with salt, pepper, and Italian herbs. Sear in oil until golden.\n3. Add garlic and sun-dried tomatoes. Cook 1 min.\n4. Add cream and stock. Simmer 3 min. Stir in spinach until wilted.\n5. Combine with pasta. Transfer to baking dish.\n6. Top with parmesan and mozzarella.\n7. Bake 20–25 min until golden and bubbly.",
    "- Undercook the pasta slightly as it continues cooking in the oven\n- Can use chicken breast if preferred\n- Leftovers: 3 days in fridge",
    "Per serving: Calories not specified",
    "creamy_tuscan_chicken_pasta_bake.md")

# Recipe 17: Chicken Broccoli Stir Fry
write("Chicken Broccoli Stir Fry", "https://www.recipetineats.com/chicken-broccoli-stir-fry/",
    "chinese", "main", "stir-fry", "10 min", "10 min", "20 min", "4 servings",
    "A quick and healthy chicken and broccoli stir fry with a savory Chinese-style sauce. Ready in 20 minutes.",
    "- 500g / 1 lb boneless chicken thighs, sliced\n- 1 large head broccoli, cut into florets\n- 3 cloves garlic, minced\n- 1 tbsp ginger, grated\n- 3 tbsp soy sauce\n- 2 tbsp oyster sauce\n- 1 tbsp rice wine (Shaoxing)\n- 1 tsp sesame oil\n- 1 tbsp cornstarch + 2 tbsp water\n- 2 tbsp vegetable oil\n- Steamed rice for serving",
    "1. Mix soy sauce, oyster sauce, rice wine, and sesame oil. Set aside.\n2. Heat wok or large skillet over high heat. Add oil.\n3. Stir fry chicken until golden. Remove.\n4. Add broccoli, stir fry 2–3 min. Add splash of water, cover 2 min.\n5. Return chicken. Add garlic and ginger, cook 30 sec.\n6. Pour in sauce. Add cornstarch slurry. Toss until glossy.\n7. Serve over steamed rice.",
    "- Cut broccoli into small, even florets for quick cooking\n- Don't overcrowd the wok\n- Leftovers: 3 days in fridge",
    "Per serving: Calories not specified",
    "chicken_broccoli_stir_fry.md")

# Recipe 18: Thai Chicken Lettuce Cups (Larb Gai)
write("Thai Chicken Lettuce Cups (Larb Gai / Laab Gai)", "https://www.recipetineats.com/thai-chicken-lettuce-cups/",
    "thai", "appetizer", "stir-fry", "10 min", "10 min", "20 min", "4 servings",
    "Fresh and vibrant Thai larb gai served in crisp lettuce cups. A perfect appetizer or light meal with bold Thai flavors.",
    "- 500g / 1 lb ground chicken (or minced thigh)\n- 1 head butter lettuce, leaves separated\n- 3 tbsp lime juice\n- 2 tbsp fish sauce\n- 1 tbsp brown sugar\n- 1 shallot, thinly sliced\n- 2 stalks lemongrass, finely minced\n- 3 kaffir lime leaves, finely sliced\n- 1 cup fresh mint leaves\n- ½ cup fresh cilantro\n- 2 tbsp toasted rice powder (khao khua)\n- 1–2 Thai chilies, sliced\n- 2 tbsp vegetable oil",
    "1. Heat oil in wok over high heat. Cook chicken, breaking up, until browned.\n2. Add lemongrass, shallot, and chilies. Cook 2 min.\n3. Remove from heat. Add lime juice, fish sauce, sugar.\n4. Toss in mint, cilantro, lime leaves, and toasted rice powder.\n5. Spoon into lettuce cups. Serve immediately.",
    "- Toasted rice powder is traditional—toast raw rice in dry pan, grind\n- Can use ground pork as substitute\n- Best served fresh",
    "Per serving: Calories not specified",
    "thai_chicken_lettuce_cups_larb_gai.md")

# Recipe 19: Chicken Pad Thai
write("Chicken Pad Thai", "https://www.recipetineats.com/chicken-pad-thai/",
    "thai", "main", "stir-fry", "15 min", "10 min", "25 min", "4 servings",
    "Classic Thai pad thai with chicken, rice noodles, bean sprouts, and that signature sweet-sour-salty sauce. Topped with crushed peanuts and fresh lime.",
    "- 250g / 9oz flat rice noodles\n- 350g / 12oz chicken thigh, sliced\n- 2 eggs\n- 2 cups bean sprouts\n- 4 green onions, cut into 2\" pieces\n- ½ cup roasted peanuts, crushed\n- 2 cloves garlic, minced\n- 2 tbsp tamarind paste\n- 2 tbsp fish sauce\n- 1 tbsp sugar\n- 1 tbsp rice vinegar\n- 2 tbsp vegetable oil\n- Lime wedges for serving",
    "1. Soak noodles in warm water until pliable. Drain.\n2. Mix tamarind, fish sauce, sugar, and vinegar for sauce.\n3. Heat oil in wok over high heat. Cook chicken until golden. Remove.\n4. Scramble eggs in wok. Add garlic, cook 30 sec.\n5. Add noodles and sauce. Toss until coated.\n6. Return chicken. Add bean sprouts and green onions. Toss 1 min.\n7. Serve with peanuts, lime wedges, and extra bean sprouts.",
    "- Don't over-soak noodles—they should be pliable but still firm\n- Tamarind paste is key for authentic flavor\n- High heat is essential",
    "Per serving: Calories not specified",
    "chicken_pad_thai.md")

# Recipe 20: Chicken Chow Mein
write("Chicken Chow Mein", "https://www.recipetineats.com/chicken-chow-mein/",
    "chinese", "main", "stir-fry", "10 min", "10 min", "20 min", "4 servings",
    "A classic Chinese chow mein with chicken, vegetables, and egg noodles in a savory sauce. Quick, easy, and packed with flavor.",
    "- 250g / 9oz egg noodles\n- 350g / 12oz chicken thigh, sliced\n- 1 cup cabbage, shredded\n- 1 carrot, julienned\n- 1 cup bean sprouts\n- 3 green onions, sliced\n- 3 cloves garlic, minced\n- 2 tbsp soy sauce\n- 1 tbsp oyster sauce\n- 1 tbsp hoisin sauce\n- 1 tsp sesame oil\n- 2 tbsp vegetable oil",
    "1. Cook noodles according to package. Drain and rinse.\n2. Mix soy, oyster, hoisin, and sesame oil.\n3. Heat oil in wok over high heat. Cook chicken until golden. Remove.\n4. Stir fry cabbage and carrot 2 min. Add garlic, cook 30 sec.\n5. Add noodles and sauce. Toss well.\n6. Return chicken. Add bean sprouts and green onions. Toss 1 min.\n7. Serve immediately.",
    "- Rinse cooked noodles to prevent sticking\n- High heat for best results\n- Customize vegetables as desired",
    "Per serving: Calories not specified",
    "chicken_chow_mein.md")

# Recipe 21: Thai Basil Chicken Stir Fry
write("Thai Basil Chicken Stir Fry", "https://www.recipetineats.com/thai-basil-chicken-stir-fry/",
    "thai", "main", "stir-fry", "10 min", "5 min", "15 min", "4 servings",
    "A lightning-fast Thai stir fry with ground chicken, holy basil, and chilies. Known as Pad Krapow Gai—the ultimate Thai comfort food.",
    "- 500g / 1 lb ground chicken\n- 2 cups Thai holy basil leaves\n- 4 cloves garlic, minced\n- 2–4 Thai chilies, sliced\n- 2 tbsp oyster sauce\n- 1 tbsp soy sauce\n- 1 tbsp fish sauce\n- 1 tsp sugar\n- 2 tbsp vegetable oil\n- 4 fried eggs for serving\n- Steamed jasmine rice",
    "1. Mix oyster sauce, soy sauce, fish sauce, and sugar.\n2. Heat oil in wok over high heat. Add garlic and chilies, cook 30 sec.\n3. Add chicken, breaking up. Cook until browned.\n4. Pour in sauce. Toss to coat.\n5. Remove from heat. Toss in basil until wilted.\n6. Serve over rice with a fried egg on top.",
    "- Thai holy basil is key (not Italian basil)\n- Fried egg on top is traditional\n- Very spicy—adjust chilies to taste",
    "Per serving: Calories not specified",
    "thai_basil_chicken_stir_fry.md")

# Recipe 22: Chicken with Creamy Sun Dried Tomato Sauce
write("Chicken with Creamy Sun Dried Tomato Sauce", "https://www.recipetineats.com/chicken-with-creamy-sun-dried-tomato-sauce/",
    "italian", "main", "stovetop", "10 min", "20 min", "30 min", "4 servings",
    "Pan-seared chicken in a luscious creamy sun-dried tomato sauce with garlic and herbs. Rich, flavorful, and perfect over pasta or with crusty bread.",
    "- 4 boneless, skinless chicken thighs or breasts\n- 1 cup sun-dried tomatoes (oil-packed), chopped\n- 3 cloves garlic, minced\n- 1 cup heavy cream\n- ½ cup chicken stock\n- ½ cup parmesan, grated\n- 2 tbsp butter\n- 1 tsp Italian herb blend\n- Salt and pepper\n- Fresh basil for garnish",
    "1. Season chicken with salt, pepper, and Italian herbs.\n2. Melt butter in large skillet over medium-high heat. Cook chicken until golden and cooked through. Remove.\n3. Add garlic and sun-dried tomatoes. Cook 1 min.\n4. Add cream and stock. Simmer 5 min until thickened.\n5. Stir in parmesan until melted.\n6. Return chicken to sauce. Simmer 2 min.\n7. Garnish with fresh basil.",
    "- Oil-packed sun-dried tomatoes add more flavor\n- Can serve over pasta, rice, or with bread\n- Leftovers: 3 days in fridge",
    "Per serving: Calories not specified",
    "chicken_with_creamy_sun_dried_tomato_sauce.md")

# Recipe 23: Pad Kee Mao (Thai Drunken Noodles)
write("Pad Kee Mao (Thai Drunken Noodles)", "https://www.recipetineats.com/pad-keemao-thai-drunken-noodles/",
    "thai", "main", "stir-fry", "10 min", "10 min", "20 min", "4 servings",
    "Spicy Thai drunken noodles with wide rice noodles, chicken, and Thai basil. Bold, fiery flavors that live up to their name.",
    "- 250g / 9oz wide rice noodles (fresh)\n- 350g / 12oz chicken thigh, sliced\n- 2 cups Thai holy basil\n- 3 cloves garlic, minced\n- 2–4 Thai chilies, sliced\n- 1 onion, sliced\n- 1 bell pepper, sliced\n- 2 tbsp oyster sauce\n- 1 tbsp soy sauce\n- 1 tbsp dark soy sauce\n- 1 tsp sugar\n- 2 tbsp vegetable oil",
    "1. Soak noodles if using dried. Fresh noodles can be used directly.\n2. Mix oyster sauce, soy sauces, and sugar.\n3. Heat oil in wok over high heat. Cook chicken until golden. Remove.\n4. Stir fry onion and pepper 2 min. Add garlic and chilies, 30 sec.\n5. Add noodles and sauce. Toss well.\n6. Return chicken. Add basil, toss until wilted.\n7. Serve immediately.",
    "- Fresh wide rice noodles are ideal\n- Very spicy—adjust chilies\n- Thai holy basil is essential",
    "Per serving: Calories not specified",
    "pad_keemao_thai_drunken_noodles.md")

# Recipe 24: Jambalaya Recipe
write("Jambalaya Recipe", "https://www.recipetineats.com/jambalaya-recipe/",
    "american", "main", "one-pot", "15 min", "45 min", "1 hour", "6 servings",
    "A one-pot Louisiana jambalaya with chicken, shrimp, andouille sausage, and rice in a richly spiced tomato broth. A complete meal in one pot.",
    "- 500g / 1 lb chicken thighs, diced\n- 300g / 10oz andouille sausage, sliced\n- 300g / 10oz shrimp, peeled\n- 2 cups long grain rice\n- 1 onion, diced\n- 1 green bell pepper, diced\n- 2 celery stalks, diced\n- 4 cloves garlic, minced\n- 1 can (400g) crushed tomatoes\n- 3 cups chicken stock\n- 2 tbsp Creole/Cajun seasoning\n- 2 bay leaves\n- 2 tbsp vegetable oil\n- Salt and pepper",
    "1. Heat oil in large pot over medium-high heat. Brown chicken and sausage. Remove.\n2. Sauté onion, pepper, and celery 5 min. Add garlic, cook 1 min.\n3. Add rice, stir 1 min. Add tomatoes, stock, seasoning, and bay leaves.\n4. Return chicken and sausage. Bring to simmer.\n5. Cover and cook 20 min until rice is tender.\n6. Add shrimp, cover, cook 5 min until pink.\n7. Rest 5 min before serving.",
    "- Andouille sausage is traditional but any smoked sausage works\n- Don't skip the holy trinity: onion, celery, bell pepper\n- Leftovers: 3 days in fridge",
    "Per serving: Calories not specified",
    "jambalaya_recipe.md")

# Recipe 25: Chicken Pasta Recipe
write("Chicken Pasta Recipe", "https://www.recipetineats.com/chicken-pasta-recipe/",
    "italian", "main", "stovetop", "10 min", "20 min", "30 min", "4 servings",
    "A simple and delicious chicken pasta with a flavorful tomato-cream sauce. The ultimate weeknight dinner.",
    "- 400g / 14oz pasta (penne or fusilli)\n- 500g / 1 lb boneless chicken thighs, sliced\n- 1 can (400g) crushed tomatoes\n- ½ cup heavy cream\n- 3 cloves garlic, minced\n- 1 onion, diced\n- 2 tbsp olive oil\n- 1 tsp Italian herb blend\n- ½ cup parmesan, grated\n- Salt and pepper\n- Fresh basil",
    "1. Cook pasta according to package. Reserve 1 cup pasta water.\n2. Season chicken with salt, pepper, and herbs. Cook in oil until golden. Remove.\n3. Sauté onion 3 min. Add garlic, cook 1 min.\n4. Add crushed tomatoes. Simmer 10 min.\n5. Stir in cream. Return chicken. Simmer 5 min.\n6. Toss with pasta. Add pasta water if needed.\n7. Top with parmesan and basil.",
    "- Reserve pasta water for adjusting sauce consistency\n- Thighs stay juicier than breast\n- Leftovers: 3 days in fridge",
    "Per serving: Calories not specified",
    "chicken_pasta_recipe.md")

# Recipe 26: Chinese Cashew Chicken
write("Chinese Cashew Chicken", "https://www.recipetineats.com/chinese-cashew-chicken/",
    "chinese", "main", "stir-fry", "10 min", "10 min", "20 min", "4 servings",
    "Tender chicken stir fried with crunchy cashews in a savory Chinese sauce. Better than takeout and ready in 20 minutes.",
    "- 500g / 1 lb boneless chicken thighs, diced\n- 1 cup roasted cashews\n- 1 bell pepper, diced\n- 1 cup broccoli florets\n- 3 green onions, sliced\n- 3 cloves garlic, minced\n- 1 tbsp ginger, grated\n- 3 tbsp soy sauce\n- 2 tbsp oyster sauce\n- 1 tbsp hoisin sauce\n- 1 tsp sesame oil\n- 2 tbsp vegetable oil\n- Steamed rice",
    "1. Mix soy, oyster, hoisin, and sesame oil.\n2. Heat oil in wok over high heat. Cook chicken until golden. Remove.\n3. Stir fry broccoli and pepper 2 min. Add garlic and ginger, 30 sec.\n4. Return chicken. Pour in sauce. Toss to coat.\n5. Add cashews and green onions. Toss 1 min.\n6. Serve over steamed rice.",
    "- Use roasted cashews for best flavor\n- Don't overcook the vegetables\n- High heat is key",
    "Per serving: Calories not specified",
    "chinese_cashew_chicken.md")

# Recipe 27: Chicken Pot Pie
write("Chicken Pot Pie", "https://www.recipetineats.com/chicken-pot-pie/",
    "american", "main", "baked", "20 min", "35 min", "55 min", "4–6 servings",
    "A comforting chicken pot pie with a creamy filling of chicken and vegetables topped with golden, flaky pastry. The ultimate comfort food.",
    "- 500g / 1 lb boneless chicken thighs, diced\n- 2 carrots, diced\n- 2 celery stalks, diced\n- 1 onion, diced\n- 1 cup frozen peas\n- 3 tbsp butter\n- 3 tbsp flour\n- 2 cups chicken stock\n- ½ cup heavy cream\n- 1 sheet puff pastry\n- 1 egg, beaten\n- Salt and pepper",
    "1. Preheat oven to 200°C/400°F.\n2. Cook chicken in butter until done. Remove.\n3. Sauté onion, carrot, celery 5 min.\n4. Add flour, cook 1 min. Gradually add stock, stirring.\n5. Add cream. Simmer until thickened.\n6. Return chicken. Add peas. Season.\n7. Transfer to pie dish. Top with puff pastry. Brush with egg.\n8. Bake 25–30 min until golden and bubbly.",
    "- Thaw puff pastry before using\n- Can use leftover rotisserie chicken\n- Leftovers: 3 days in fridge",
    "Per serving: Calories not specified",
    "chicken_pot_pie.md")

# Recipe 28: Lemon Chicken Salad
write("Lemon Chicken Salad", "https://www.recipetineats.com/lemon-chicken-salad/",
    "american", "salad", "stovetop", "10 min", "15 min", "25 min", "4 servings",
    "A bright and fresh lemon chicken salad with tender chicken, crisp greens, and a zesty lemon dressing. Perfect for a light lunch or dinner.",
    "- 500g / 1 lb boneless chicken breasts\n- 6 cups mixed greens\n- 1 cup cherry tomatoes, halved\n- 1 avocado, sliced\n- ¼ cup feta cheese, crumbled\n- ¼ cup almonds, toasted\n- 3 tbsp olive oil\n- 2 tbsp lemon juice\n- 1 tsp lemon zest\n- 1 tbsp honey\n- 1 tsp Dijon mustard\n- Salt and pepper",
    "1. Season chicken with salt and pepper. Cook in olive oil over medium-high heat until golden and cooked through. Rest 5 min, then slice.\n2. Whisk lemon juice, zest, honey, mustard, and remaining oil for dressing.\n3. Arrange greens on plates. Top with chicken, tomatoes, avocado, feta, and almonds.\n4. Drizzle with dressing. Serve immediately.",
    "- Let chicken rest before slicing for juicier results\n- Add dressing just before serving\n- Customize with your favorite salad toppings",
    "Per serving: Calories not specified",
    "lemon_chicken_salad.md")

# Recipe 29: Mexican Chicken Avocado Salad
write("Mexican Chicken Avocado Salad", "https://www.recipetineats.com/mexican-chicken-avocado-salad/",
    "mexican", "salad", "stovetop", "10 min", "15 min", "25 min", "4 servings",
    "A vibrant Mexican-inspired chicken salad with avocado, black beans, corn, and a zesty lime-cilantro dressing.",
    "- 500g / 1 lb boneless chicken breasts\n- 6 cups romaine lettuce, chopped\n- 2 avocados, diced\n- 1 can (400g) black beans, drained\n- 1 cup corn kernels\n- 1 cup cherry tomatoes, halved\n- ¼ cup red onion, diced\n- ¼ cup cilantro, chopped\n- 3 tbsp lime juice\n- 2 tbsp olive oil\n- 1 tsp cumin\n- 1 tsp chili powder\n- Salt and pepper",
    "1. Season chicken with cumin, chili powder, salt, and pepper. Cook in oil until done. Rest, then slice.\n2. Whisk lime juice, olive oil, salt, and pepper for dressing.\n3. Arrange lettuce on plates. Top with chicken, avocado, beans, corn, tomatoes, onion, and cilantro.\n4. Drizzle with dressing. Serve with tortilla chips if desired.",
    "- Use ripe avocados for best texture\n- Can use grilled or rotisserie chicken\n- Serve immediately after dressing",
    "Per serving: Calories not specified",
    "mexican_chicken_avocado_salad.md")

# Recipe 30: Oven Baked Chicken and Rice Pilaf
write("Oven Baked Chicken and Rice Pilaf (Cranberry Walnut Apple)", "https://www.recipetineats.com/oven-baked-chicken-and-rice-pilaf/",
    "american", "main", "baked", "15 min", "45 min", "1 hour", "4 servings",
    "A one-pan oven baked chicken and rice pilaf with cranberries, walnuts, and apples. A complete meal with sweet and savory flavors.",
    "- 4 bone-in, skin-on chicken thighs\n- 1½ cups long grain rice\n- 1 apple, diced\n- ½ cup dried cranberries\n- ½ cup walnuts, chopped\n- 1 onion, diced\n- 3 cloves garlic, minced\n- 3 cups chicken stock\n- 2 tbsp butter\n- 1 tsp dried thyme\n- Salt and pepper",
    "1. Preheat oven to 180°C/350°F.\n2. Season chicken with salt, pepper, and thyme. Sear in ovenproof skillet until golden. Remove.\n3. Sauté onion 3 min. Add garlic, cook 1 min. Add rice, stir 1 min.\n4. Add stock, cranberries, apple, and walnuts. Stir.\n5. Nestle chicken skin-side up on top.\n6. Cover and bake 40–45 min until rice is tender.\n7. Rest 5 min before serving.",
    "- Use an ovenproof skillet or transfer to baking dish\n- Don't stir after adding to oven\n- Resting time is important for the rice",
    "Per serving: Calories not specified",
    "oven_baked_chicken_and_rice_pilaf.md")

# Recipe 31: Vietnamese Coconut Caramel Chicken
write("Vietnamese Coconut Caramel Chicken", "https://www.recipetineats.com/vietnamese-coconut-caramel-chicken",
    "vietnamese", "main", "stovetop", "10 min", "1 hour", "1 hour 10 min", "4 servings",
    "Bone-in chicken braised in a rich Vietnamese coconut caramel sauce. A more complex and luxurious version of the quick caramel chicken.",
    "- 1 kg / 2 lb bone-in chicken thighs\n- ½ cup coconut cream\n- ¼ cup brown sugar\n- 3 tbsp fish sauce\n- 1 onion, sliced\n- 4 cloves garlic, minced\n- 1 tbsp ginger, grated\n- 1 cup coconut milk\n- 2 tbsp vegetable oil\n- Fresh cilantro and chili for garnish",
    "1. Heat oil and sugar in large pot over medium-high. Make caramel until deep amber.\n2. Add onion, garlic, ginger. Cook 2 min.\n3. Add chicken, skin-side down. Sear 3 min.\n4. Add coconut milk, coconut cream, and fish sauce.\n5. Bring to simmer. Cover and cook 45 min.\n6. Uncover, reduce sauce 10 min until thick and glossy.\n7. Garnish with cilantro and chili. Serve with rice.",
    "- Watch the caramel carefully—it can burn quickly\n- Bone-in thighs add more flavor\n- Sauce should be thick and glossy when done",
    "Per serving: Calories not specified",
    "vietnamese_coconut_caramel_chicken.md")

# Recipe 32: Thai Coconut Chicken
write("Thai Coconut Chicken", "https://www.recipetineats.com/thai-coconut-chicken/",
    "thai", "main", "stovetop", "10 min", "20 min", "30 min", "4 servings",
    "A creamy Thai coconut chicken curry with tender vegetables. Rich, fragrant, and ready in 30 minutes.",
    "- 500g / 1 lb boneless chicken thighs, sliced\n- 1 can (400ml) coconut milk\n- 2 tbsp Thai red or green curry paste\n- 1 cup chicken stock\n- 1 bell pepper, sliced\n- 1 zucchini, sliced\n- 1 cup Thai basil leaves\n- 2 tbsp fish sauce\n- 1 tbsp brown sugar\n- 2 tbsp vegetable oil\n- Kaffir lime leaves (optional)\n- Steamed jasmine rice",
    "1. Heat oil in large skillet. Cook chicken until golden. Remove.\n2. Add curry paste, cook 1 min until fragrant.\n3. Add coconut milk and stock. Stir to combine.\n4. Add vegetables. Simmer 10 min.\n5. Return chicken. Add fish sauce and sugar.\n6. Stir in basil. Serve over jasmine rice.",
    "- Adjust curry paste to your heat preference\n- Thai basil adds authentic flavor\n- Can use any vegetables you have on hand",
    "Per serving: Calories not specified",
    "thai_coconut_chicken.md")

# Recipe 33: Oven Baked Chicken Quesadillas
write("Oven Baked Chicken Quesadillas", "https://www.recipetineats.com/oven-baked-chicken-quesadillas/",
    "mexican", "main", "baked", "10 min", "15 min", "25 min", "4 servings",
    "Crispy oven-baked chicken quesadillas loaded with cheese, seasoned chicken, and vegetables. Easier than frying and feeds a crowd.",
    "- 500g / 1 lb cooked chicken, shredded\n- 8 large flour tortillas\n- 2 cups shredded cheese (cheddar/mexican blend)\n- 1 bell pepper, diced\n- 1 cup corn kernels\n- ¼ cup cilantro, chopped\n- 1 tsp cumin\n- 1 tsp chili powder\n- 2 tbsp vegetable oil\n- Salsa, sour cream, guacamole for serving",
    "1. Preheat oven to 200°C/400°F. Line baking sheets with parchment.\n2. Mix chicken with cumin, chili powder, salt, and pepper.\n3. Place tortillas on baking sheets. Divide chicken, cheese, pepper, corn, and cilantro on one half of each tortilla.\n4. Fold over. Brush with oil.\n5. Bake 12–15 min until golden and crispy.\n6. Cut into wedges. Serve with salsa, sour cream, and guacamole.",
    "- Use leftover or rotisserie chicken\n- Don't overfill or they'll be hard to flip\n- Brush with oil for maximum crispiness",
    "Per serving: Calories not specified",
    "oven_baked_chicken_quesadillas.md")

# Recipe 34: Creamy Chicken and Bacon Pasta
write("Creamy Chicken and Bacon Pasta", "https://www.recipetineats.com/creamy-chicken-and-bacon-pasta/",
    "italian", "main", "stovetop", "10 min", "20 min", "30 min", "4 servings",
    "A rich and indulgent pasta with chicken, crispy bacon, and a creamy garlic parmesan sauce. Pure comfort food.",
    "- 400g / 14oz pasta (penne or fusilli)\n- 500g / 1 lb boneless chicken thighs, sliced\n- 200g / 7oz bacon, diced\n- 3 cloves garlic, minced\n- 1 cup heavy cream\n- ½ cup parmesan, grated\n- 2 tbsp butter\n- Salt and pepper\n- Fresh parsley for garnish",
    "1. Cook pasta according to package. Reserve 1 cup pasta water.\n2. Cook bacon until crispy. Remove, leaving fat in pan.\n3. Cook chicken in bacon fat until golden. Remove.\n4. Add butter and garlic. Cook 1 min.\n5. Add cream. Simmer 3 min.\n6. Stir in parmesan until melted.\n7. Return chicken and bacon. Toss with pasta. Add pasta water if needed.\n8. Garnish with parsley.",
    "- Save the bacon fat for cooking the chicken—extra flavor!\n- Reserve pasta water for adjusting sauce\n- Leftovers: 3 days in fridge",
    "Per serving: Calories not specified",
    "creamy_chicken_and_bacon_pasta.md")

# Recipe 35: Chicken and Mushroom Risotto
write("Chicken and Mushroom Risotto", "https://www.recipetineats.com/chicken-and-mushroom-risotto/",
    "italian", "main", "stovetop", "10 min", "35 min", "45 min", "4 servings",
    "A creamy Italian risotto with tender chicken and earthy mushrooms. Rich, comforting, and worth the stirring.",
    "- 1½ cups arborio rice\n- 500g / 1 lb boneless chicken thighs, diced\n- 300g / 10oz mushrooms, sliced\n- 1 onion, finely diced\n- 3 cloves garlic, minced\n- ½ cup dry white wine\n- 4–5 cups chicken stock, warm\n- ½ cup parmesan, grated\n- 2 tbsp butter\n- 2 tbsp olive oil\n- Salt and pepper\n- Fresh parsley",
    "1. Heat oil in large pan. Cook chicken until golden. Remove.\n2. Sauté onion 3 min. Add mushrooms, cook 5 min. Add garlic, 1 min.\n3. Add rice, stir 1 min until translucent edges.\n4. Add wine. Stir until absorbed.\n5. Add stock one ladle at a time, stirring between additions. Wait until absorbed before adding more.\n6. Continue until rice is creamy and al dente (~25 min).\n7. Stir in chicken, butter, and parmesan.\n8. Season. Garnish with parsley.",
    "- Keep stock warm for best results\n- Stir frequently but not constantly\n- Risotto should be creamy, not stiff\n- Rest 2 min before serving",
    "Per serving: Calories not specified",
    "chicken_and_mushroom_risotto.md")

# Recipe 36: Mexican Shredded Chicken
write("Mexican Shredded Chicken", "https://www.recipetineats.com/mexican-shredded-chicken/",
    "mexican", "main", "stovetop", "10 min", "30 min", "40 min", "4–6 servings",
    "Tender, flavorful Mexican shredded chicken perfect for tacos, burritos, bowls, and more. Versatile and easy to make.",
    "- 1 kg / 2 lb boneless chicken thighs\n- 1 can (400g) crushed tomatoes\n- 1 onion, quartered\n- 4 cloves garlic\n- 2 tbsp chipotle in adobo\n- 1 tbsp cumin\n- 1 tsp oregano\n- 1 tsp chili powder\n- Juice of 2 limes\n- Salt and pepper\n- Fresh cilantro",
    "1. Place chicken in large pot. Add tomatoes, onion, garlic, chipotle, cumin, oregano, chili powder.\n2. Add enough water to barely cover. Season with salt.\n3. Bring to simmer. Cook 25–30 min until chicken is fall-apart tender.\n4. Remove chicken. Shred with two forks.\n5. Reduce sauce if too thin. Return chicken to sauce.\n6. Add lime juice and cilantro.\n7. Use for tacos, burritos, bowls, or salads.",
    "- Great meal prep—makes enough for multiple meals\n- Freezes well for up to 3 months\n- Adjust chipotle for desired heat level",
    "Per serving: Calories not specified",
    "mexican_shredded_chicken.md")

# Recipe 37: One Pot Chicken Enchilada Rice Casserole
write("One Pot Chicken Enchilada Rice Casserole", "https://www.recipetineats.com/one-pot-chicken-enchilada-rice-casserole/",
    "mexican", "main", "one-pot", "15 min", "35 min", "50 min", "4–6 servings",
    "All the flavors of chicken enchiladas in a one-pot rice casserole. Easy, cheesy, and delicious.",
    "- 500g / 1 lb boneless chicken thighs, diced\n- 1½ cups long grain rice\n- 1 can (400g) enchilada sauce\n- 1 can (400g) black beans, drained\n- 1 cup corn kernels\n- 1 cup shredded cheese\n- 1 onion, diced\n- 3 cloves garlic, minced\n- 2 cups chicken stock\n- 1 tsp cumin\n- Salt and pepper\n- Cilantro, sour cream for serving",
    "1. Season chicken with cumin, salt, and pepper.\n2. Heat oil in large ovenproof skillet. Cook chicken until golden. Remove.\n3. Sauté onion 3 min. Add garlic, 1 min. Add rice, stir 1 min.\n4. Add enchilada sauce, stock, beans, and corn. Stir.\n5. Return chicken. Bring to simmer.\n6. Cover and bake at 180°C/350°F for 30 min.\n7. Top with cheese. Bake uncovered 5 min.\n8. Garnish with cilantro and sour cream.",
    "- Use an ovenproof skillet or transfer to baking dish\n- Can use rotisserie chicken to save time\n- Leftovers: 3 days in fridge",
    "Per serving: Calories not specified",
    "one_pot_chicken_enchilada_rice_casserole.md")

# Recipe 38: One Pot Creamy Parmesan Garlic Risotto with Lemon Pepper Chicken
write("One Pot Creamy Parmesan Garlic Risotto with Lemon Pepper Chicken", "https://www.recipetineats.com/one-pot-creamy-parmesan-garlic-risotto-with-lemon-pepper-chicken/",
    "italian", "main", "one-pot", "15 min", "35 min", "50 min", "4 servings",
    "A one-pot wonder combining creamy parmesan garlic risotto with zesty lemon pepper chicken. Restaurant-quality dinner made easy.",
    "- 500g / 1 lb boneless chicken breasts\n- 1½ cups arborio rice\n- 4–5 cups chicken stock\n- 1 cup parmesan, grated\n- 4 cloves garlic, minced\n- 2 tbsp butter\n- 2 tbsp olive oil\n- 2 tbsp lemon juice\n- 1 tsp lemon pepper seasoning\n- ½ cup white wine\n- Salt and pepper\n- Fresh parsley",
    "1. Season chicken with lemon pepper, salt. Sear in oil until golden. Remove.\n2. Sauté garlic 1 min. Add rice, stir 1 min.\n3. Add wine, stir until absorbed.\n4. Add stock gradually, stirring between additions.\n5. When rice is nearly done, return chicken.\n6. Stir in butter and parmesan.\n7. Add lemon juice. Garnish with parsley.",
    "- Gradual stock addition is key for creamy risotto\n- Let chicken rest before slicing\n- Leftovers: 3 days in fridge",
    "Per serving: Calories not specified",
    "one_pot_creamy_parmesan_garlic_risotto.md")

# Recipe 39: One Pot Greek Chicken Lemon Rice
write("One Pot Greek Chicken Lemon Rice", "https://www.recipetineats.com/one-pot-greek-chicken-lemon-rice/",
    "greek", "main", "one-pot", "15 min", "35 min", "50 min", "4 servings",
    "Greek-inspired one-pot chicken and rice with lemon, oregano, and feta. Bright Mediterranean flavors in a simple one-pan meal.",
    "- 500g / 1 lb boneless chicken thighs\n- 1½ cups long grain rice\n- 3 cups chicken stock\n- Juice and zest of 2 lemons\n- 3 cloves garlic, minced\n- 1 onion, diced\n- 2 tbsp olive oil\n- 1 tbsp dried oregano\n- ½ cup feta, crumbled\n- Fresh oregano\n- Salt and pepper",
    "1. Season chicken with oregano, salt, and pepper. Sear in oil until golden. Remove.\n2. Sauté onion 3 min. Add garlic, 1 min. Add rice, stir 1 min.\n3. Add stock, lemon juice, and zest. Stir.\n4. Nestle chicken on top. Bring to simmer.\n5. Cover and bake at 180°C/350°F for 30 min.\n6. Rest 5 min. Top with feta and fresh oregano.",
    "- Don't stir after adding to oven\n- Resting time helps the rice absorb remaining liquid\n- Feta adds a lovely salty tang",
    "Per serving: Calories not specified",
    "one_pot_greek_chicken_lemon_rice.md")

# Recipe 40: Jamaican Jerk Chicken Drumsticks with Caribbean Rice and Beans
write("Jamaican Jerk Chicken Drumsticks with Caribbean Rice and Beans", "https://www.recipetineats.com/jamaican-jerk-chicken-drumsticks/",
    "jamaican", "main", "baked", "15 min", "45 min", "1 hour", "4 servings",
    "Spicy, smoky Jamaican jerk chicken drumsticks with Caribbean rice and beans. A complete island-inspired meal.",
    "- 8 chicken drumsticks\n- 3 tbsp jerk seasoning (store-bought or homemade)\n- 2 tbsp soy sauce\n- 2 tbsp lime juice\n- 2 tbsp brown sugar\n- 1 tbsp thyme leaves\n- 2 cloves garlic, minced\n- 1 scotch bonnet pepper (optional)\n- 1 cup long grain rice\n- 1 can (400g) kidney beans, drained\n- 1 can (400ml) coconut milk\n- 1 cup chicken stock\n- 1 tsp allspice\n- Salt and pepper",
    "1. Mix jerk seasoning, soy sauce, lime juice, sugar, thyme, garlic, and pepper. Coat drumsticks. Marinate 1+ hour.\n2. Preheat oven to 200°C/400°F.\n3. Bake drumsticks 40–45 min until charred and cooked through.\n4. For rice: Combine rice, beans, coconut milk, stock, and allspice. Season.\n5. Bring to simmer. Cover and cook 18 min.\n6. Rest 5 min. Fluff with fork.\n7. Serve chicken over rice and beans.",
    "- Marinate overnight for best flavor\n- Scotch bonnet peppers are very hot—adjust to taste\n- Jerk seasoning can be homemade or store-bought",
    "Per serving: Calories not specified",
    "jamaican_jerk_chicken_drumsticks.md")

# Recipe 41: One Pan Spanish Chicken Chorizo Tomato Potatoes
write("One Pan Spanish Chicken Chorizo Tomato Potatoes", "https://www.recipetineats.com/one-pan-spanish-chicken-chorizo-tomato-potatoes/",
    "spanish", "main", "one-pot", "15 min", "40 min", "55 min", "4 servings",
    "A one-pan Spanish-inspired dish with chicken, chorizo, potatoes, and tomatoes. Smoky, savory, and incredibly satisfying.",
    "- 500g / 1 lb boneless chicken thighs\n- 200g / 7oz chorizo, sliced\n- 500g / 1 lb potatoes, cubed\n- 1 can (400g) crushed tomatoes\n- 1 onion, diced\n- 4 cloves garlic, minced\n- 1 tsp smoked paprika\n- 1 tsp cumin\n- 2 tbsp olive oil\n- Salt and pepper\n- Fresh parsley",
    "1. Preheat oven to 200°C/400°F.\n2. Season chicken with paprika, cumin, salt, and pepper.\n3. Heat oil in large ovenproof skillet. Sear chicken until golden. Remove.\n4. Cook chorizo until crispy. Remove.\n5. Sauté onion 3 min. Add garlic, 1 min.\n6. Add potatoes and tomatoes. Season. Stir.\n7. Nestle chicken and chorizo on top.\n8. Bake 35–40 min until potatoes are tender.\n9. Garnish with parsley.",
    "- Use an ovenproof skillet or transfer to baking dish\n- Smoked paprika is essential for authentic flavor\n- Potatoes should be cut small for even cooking",
    "Per serving: Calories not specified",
    "one_pan_spanish_chicken_chorizo.md")

# Recipe 42: Crispy Shredded Chicken Noodle Stir Fry
write("Crispy Shredded Chicken Noodle Stir Fry", "https://www.recipetineats.com/crispy-shredded-chicken-noodle-stir-fry/",
    "chinese", "main", "stir-fry", "15 min", "15 min", "30 min", "4 servings",
    "Crispy shredded chicken with noodles and vegetables in a savory stir fry sauce. The crispy chicken texture makes this dish special.",
    "- 500g / 1 lb boneless chicken thighs\n- 250g / 9oz egg noodles\n- 2 cups mixed vegetables (cabbage, carrot, bean sprouts)\n- 3 cloves garlic, minced\n- 2 tbsp soy sauce\n- 1 tbsp oyster sauce\n- 1 tbsp hoisin sauce\n- 1 tsp sesame oil\n- 2 tbsp vegetable oil\n- 3 green onions, sliced",
    "1. Flatten chicken with a pan or mallet. Cook in very hot oil until deeply golden and crispy. Remove and shred.\n2. Cook noodles according to package. Drain.\n3. Heat oil in wok over high heat. Stir fry vegetables 2–3 min.\n4. Add garlic, cook 30 sec.\n5. Add noodles and sauce. Toss well.\n6. Add crispy chicken and green onions. Toss 1 min.\n7. Serve immediately.",
    "- Press chicken flat for maximum crispy surface\n- Very high heat for the chicken is essential\n- Don't add the crispy chicken too early or it'll lose its crunch",
    "Per serving: Calories not specified",
    "crispy_shredded_chicken_noodle_stir_fry.md")

# Recipe 43: 10 Classic Chinese Dishes + Homemade Teriyaki Sauce
write("10 Classic Chinese Dishes + Homemade Teriyaki Sauce", "https://www.recipetineats.com/10-classic-chinese-dishes/",
    "chinese", "main", "stir-fry", "Varies", "Varies", "Varies", "Varies",
    "A collection of 10 classic Chinese dishes plus a homemade teriyaki sauce recipe. A comprehensive guide to Chinese home cooking.",
    "Varies by dish. Includes recipes for:\n- Homemade Teriyaki Sauce\n- Classic stir fry dishes\n- Various Chinese cooking techniques\n\nSee the full recipe collection at RecipeTin Eats for complete ingredient lists for each dish.",
    "Each dish has its own instructions. Key techniques include:\n1. Proper wok heating and seasoning\n2. Velveting meat for tender stir fries\n3. Balancing soy sauce, oyster sauce, and other seasonings\n4. High-heat cooking for wok hei (breath of the wok)\n5. Making homemade teriyaki sauce from scratch",
    "- Homemade teriyaki sauce is far superior to store-bought\n- A well-seasoned wok makes a big difference\n- Prep all ingredients before starting to cook\n- High heat is essential for authentic Chinese cooking",
    "Varies by dish",
    "10_classic_chinese_dishes.md")

print("\nAll remaining recipes (15-43) written successfully!")
