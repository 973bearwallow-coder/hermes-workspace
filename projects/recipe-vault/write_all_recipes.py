import os, json
from datetime import datetime
from collections import Counter

VAULT = os.path.expanduser('~/hermes-workspace/projects/recipe-vault')
RECIPES_DIR = os.path.join(VAULT, 'recipes')

# Recipe content for all 33 stub files
RECIPE_DATA = {
"amazing_key_lime_cheesecake.md": """# Amazing Key Lime Cheesecake
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/amazing-key-lime-cheesecake/)
**Cuisine:** american
**Type:** dessert
**Method:** baked
**Prep Time:** 12 hrs 25 mins
**Cook Time:** 1 hr 10 mins
**Total Time:** 13 hrs 35 mins
**Yield:** 12 slices

## Description
An ultra-creamy key lime cheesecake designed to prevent cracking without using a traditional water bath. Uses a revolutionary steaming technique for perfect results.

## Ingredients

### Crust
- 1 1/2 cups graham cracker crumbs (~14 crackers)
- 2 tbsp granulated sugar
- 6 tbsp salted butter, melted

### Filling
- 3 packages (8 oz each) cream cheese, softened
- 1 cup granulated sugar
- 1 tbsp cornstarch
- Zest from 1 lime (1-2 tsp)
- 1/2 cup key lime juice OR 2 tbsp fresh lemon juice + 6 tbsp fresh lime juice
- 3 large eggs

### Topping
- 1 cup heavy whipping cream
- 1/4 cup powdered sugar
- 1/2 tsp vanilla extract
- Lime slices or zest for garnish

## Instructions
1. Preheat oven to 300 F. Grease a 9-inch springform pan.
2. Mix crust ingredients. Press into pan bottom and 1/2-inch up sides. Bake 15 min; cool.
3. Beat cream cheese, sugar, cornstarch, and lime zest until smooth. Add lime juice; mix. Add eggs; mix until just combined.
4. Place a 9x13-inch metal pan with 2-3 cups boiling water on bottom rack. Bake cheesecake on upper rack for 50-65 minutes.
5. Turn off oven, prop door open 4 inches, leave cheesecake inside for 30 minutes.
6. Cool completely. Chill overnight.
7. Whip cream, powdered sugar, and vanilla. Top cheesecake and garnish with lime.

## Tips & Notes
- Avoid overmixing after adding eggs to prevent cracking.
- Fresh juice is strongly preferred over bottled.
- Chilling overnight is essential for texture.
- Freezes well.

## Nutrition (per slice)
- Calories: 460 kcal | Carbs: 35g | Protein: 6g | Fat: 34g
- Saturated Fat: 19g | Cholesterol: 137mg | Sodium: 343mg
""",

"amish-style_apple_and_cinnamon_baked_oatmeal.md": """# Amish-Style Apple and Cinnamon Baked Oatmeal
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/amish-style-apple-and-cinnamon-baked-oatmeal/)
**Cuisine:** american
**Type:** breakfast
**Method:** baked
**Prep Time:** 20 minutes
**Cook Time:** 40 minutes
**Total Time:** 1 hour
**Yield:** 8 servings

## Description
A hearty, make-ahead baked oatmeal featuring apples and cinnamon. Can be prepared the night before and baked in the morning.

## Ingredients
- 3 cups old-fashioned rolled oats
- 1 1/2 tsp baking powder
- 2 tsp ground cinnamon
- 1/4 tsp ground nutmeg
- 3/4 tsp salt
- 1/2 cup lightly packed brown sugar
- 2 1/2 cups milk
- 2 large eggs
- 1 tsp vanilla extract
- 4 tbsp butter or coconut oil, melted
- 2-3 large tart-sweet apples (Honey Crisp or Gala), peeled, cored, diced

## Instructions
1. Lightly grease an 8x12-inch or 9x13-inch baking pan. Preheat oven to 325 F.
2. Whisk oats, baking powder, cinnamon, nutmeg, salt, and brown sugar.
3. In separate container, combine milk, eggs, and vanilla.
4. Pour wet mix over dry; add melted butter. Stir well.
5. Spread diced apples evenly in pan; pour oat mixture over top.
6. Optional: Cover and refrigerate overnight.
7. Bake 35-45 minutes until top is golden and set.
8. Serve warm with milk poured over top if desired.

## Tips & Notes
- Add nuts or raisins if desired.
- Apples may rise and brown slightly when refrigerated overnight.
- Leftovers refrigerate well and reheat easily.
- Baked oatmeal freezes well after cooking.
- Dairy-free: use almond/oat milk, vegan butter, flax eggs.

## Nutrition (per serving)
- Calories: 305 kcal | Carbs: 48g | Protein: 8g | Fat: 10g
- Saturated Fat: 5g | Cholesterol: 65mg | Sodium: 404mg
""",

"cheesy_funeral_potatoes_au_gratin_potatoes.md": """# Cheesy Funeral Potatoes {Au Gratin Potatoes}
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/cheesy-au-gratin-potatoes-2/)
**Cuisine:** american
**Type:** side
**Method:** baked
**Prep Time:** 20 minutes
**Cook Time:** 55 minutes
**Total Time:** 1 hour 15 minutes
**Yield:** 8 servings

## Description
A beloved American casserole traditionally served at post-funeral luncheons with ham. This version skips canned soup in favor of a homemade cheesy sauce.

## Ingredients

### Potato Base
- 3 tbsp salted butter
- 1/2 cup diced onion
- 1/4 cup all-purpose flour
- 1 1/2 cups low-sodium chicken broth
- 1 cup milk
- 1 1/2 tsp salt
- 1/2 tsp pepper
- 1/4 tsp dried thyme
- 2 cups shredded sharp cheddar
- 5-6 medium russet/Yukon Gold potatoes (~3 lbs), peeled, cooked, cooled, shredded
- 1/2 cup sour cream

### Topping
- 3 cups cornflakes, lightly crushed
- 2 tbsp melted butter

## Instructions
1. Preheat oven to 350 F. Grease a 9x13-inch baking dish.
2. Saute onion in butter until soft (5-6 min).
3. Whisk in flour, cook 1 min.
4. Slowly add broth + milk, whisking constantly. Add salt, pepper, thyme.
5. Simmer until slightly thickened (5-6 min).
6. Off heat, stir in cheese until melted. Add sour cream.
7. Fold in shredded potatoes until evenly coated.
8. Spread into dish. Top with buttered cornflakes.
9. Bake 40-45 min until bubbly.
10. Rest 10 min before serving.

## Tips & Notes
- Use cooled, chilled cooked potatoes to avoid mushy texture.
- Freshly grated cheddar is best.
- Frozen hash browns work great - thaw first.
- Assemble up to 2 days ahead. Slow cooker compatible.

## Nutrition (per serving)
- Calories: 393 kcal | Carbs: 40g | Protein: 13g | Fat: 21g
- Saturated Fat: 13g | Cholesterol: 59mg | Sodium: 796mg
""",

"chopped_greek_chicken_salad_with_pita_croutons_and_tzatziki_.md": """# Chopped Greek Chicken Salad with Pita Croutons and Tzatziki Dressing
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/chopped-greek-chicken-salad/)
**Cuisine:** greek
**Type:** salad
**Method:** grilled
**Prep Time:** 15 minutes
**Cook Time:** 15 minutes
**Total Time:** 13 hrs 15 min (mostly marinating)
**Yield:** 6 servings

## Description
A fresh, flavorful Mediterranean-inspired chopped salad featuring marinated grilled chicken, toasted pita croutons, crisp vegetables, and creamy tzatziki dressing.

## Ingredients

### Tzatziki Dressing
- 1 cup Greek yogurt
- 1/4 cup mayonnaise
- 1 cucumber, salted and drained
- 2 cloves garlic
- 2 tbsp fresh lemon juice
- 1 tbsp red wine vinegar
- 2 tbsp fresh parsley
- Salt and pepper to taste

### Greek Chicken Marinade
- 1/4 cup olive oil
- 3 tbsp fresh lemon juice
- 1/4 cup buttermilk
- 3 cloves garlic, minced
- 1 tbsp dried oregano
- 1 tsp salt
- 1/2 tsp pepper
- 1 1/2 lbs chicken breasts

### Pita Croutons
- 3 pita breads, cut into 1/4-inch squares
- 2 tbsp olive oil
- 1/2 tsp garlic powder

### Salad
- 6 cups chopped romaine
- 1 cucumber, diced
- 1 bell pepper, diced
- 1 cup cherry tomatoes, halved
- 1/2 cup kalamata olives
- 1/4 cup red onion, diced
- 1/2 cup crumbled feta cheese

## Instructions
1. Marinate chicken in marinade ingredients for 8-12 hours.
2. Grill chicken until 165 F internal. Rest 10 min, then slice.
3. Toast pita squares at 375 F for 15-20 min until golden.
4. Blend tzatziki ingredients until smooth.
5. Assemble salad with romaine base, vegetables, chicken, feta, croutons, and dressing.

## Tips & Notes
- Every component can be prepped days in advance.
- Store everything separately and assemble just before serving.
- Buttermilk in marinade ensures juicy, tender chicken.
- Serve buffet-style for customizable meals.

## Nutrition (per serving)
- Calories: 441 kcal | Protein: 33g | Carbs: 33g | Fat: 19g
- Sodium: 1570mg | Fiber: 4g | Sugar: 6g
""",

"creamy_cilantro_lime_dressing.md": """# Creamy Cilantro Lime Dressing
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/creamy-cilantro-lime-dressing/)
**Cuisine:** american, mexican
**Type:** side
**Method:** no-cook
**Prep Time:** 15 minutes
**Total Time:** 15 minutes
**Yield:** 12 servings (2-3 cups)

## Description
A versatile, flavorful condiment with serious Cafe Rio vibes - creamy, ranchy, and packed with cilantro flavor. Works on salads, tacos, burritos, rice bowls, and as a dip.

## Ingredients
- 1/2 cup buttermilk
- 1/2 cup mayonnaise
- 1/2 cup sour cream
- 1/4 cup salsa verde or green enchilada sauce
- 1 tablespoon fresh lime juice
- 1 teaspoon garlic powder
- 1 teaspoon dried parsley
- 1/2 tsp onion powder
- Pinch of dried dill
- Pinch of salt and black pepper
- 1/2 cup coarsely chopped cilantro
- 1 green onion (white and green parts)

## Instructions
1. Combine all ingredients in a blender and process until smooth.
2. Thin with additional buttermilk, milk, or lime juice if desired.
3. Refrigerate until ready to serve - flavor improves over time.

## Tips & Notes
- Keeps well for 7-10 days in the refrigerator.
- Can be made up to a week in advance.
- For cilantro haters: substitute with fresh parsley.
- Add Tajin for extra zing.
- Dairy-free: use almond milk + lemon, dairy-free sour cream, and all mayo.

## Nutrition (per serving)
- Calories: 46 kcal | Carbs: 3g | Protein: 1g | Fat: 4g
- Saturated Fat: 1g | Cholesterol: 6mg | Sodium: 121mg
""",

"creamy_garlic_alfredo_sauce_my_go-to_dinner_saver.md": """# Creamy Garlic Alfredo Sauce {My Go-To Dinner Saver!}
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/creamy-garlic-alfredo-sauce-my-go-to-dinner-saver/)
**Cuisine:** american, italian
**Type:** main
**Method:** stovetop
**Prep Time:** 5 minutes
**Cook Time:** 10 minutes
**Total Time:** 15 minutes
**Yield:** 2 cups sauce

## Description
A family-favorite, quick dinner sauce that's healthier than traditional butter-and-cream versions. Ready in under 15 minutes. Universally loved by kids and adults alike.

## Ingredients
- 2 tablespoons butter
- 3 cloves garlic, finely minced or pressed
- 4 oz cream cheese, softened and cut into 6 pieces
- 1 cup milk (1% or 2% recommended)
- 1 1/2 cups freshly grated Parmesan cheese
- 1/2 teaspoon salt, plus more to taste
- 1/4 teaspoon pepper

## Instructions
1. Melt butter in a medium pot over medium heat.
2. Cook garlic for ~2 minutes, stirring constantly.
3. Add cream cheese and let it sit until warm and melty (2-3 min). Whisk until smooth.
4. Gradually add milk, 1/4 cup at a time, whisking constantly.
5. Stir in Parmesan, salt, and pepper until cheese is fully melted.
6. Cook 2-3 minutes for thicker sauce, or remove immediately for thinner consistency.
7. Serve immediately over hot pasta.

## Tips & Notes
- Freshly grated Parmesan is essential for smooth melting.
- One batch coats 8-12 oz dried pasta generously.
- Stores well for several days; reheats smoothly.
- Not recommended for freezing.
- Add sauteed mushrooms, onions, peas, grilled shrimp, chicken, or bacon.

## Nutrition (per 1/4 cup serving)
- Calories: ~120 kcal | Carbs: 3g | Protein: 7g | Fat: 9g
""",

"dark_chocolate_sea_salt_caramel_pretzel_bark_snappers_knock_.md": """# Dark Chocolate Sea Salt Caramel Pretzel Bark {Snappers Knock Off}
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/dark-chocolate-sea-salt-caramel-pretzel-bark-snappers-knock-off/)
**Cuisine:** american
**Type:** dessert
**Method:** stovetop
**Prep Time:** 15 minutes
**Cook Time:** 45 minutes
**Total Time:** 1 hour
**Yield:** 20 servings (3 pounds)

## Description
A homemade version of the popular Snappers candy - layers of dark chocolate, buttery caramel, pretzels, and sea salt. Salty, sweet, chewy, and rich.

## Ingredients

### Caramel
- 6 tablespoons salted butter
- 1/4 teaspoon salt
- 1/2 cup light corn syrup
- 1 cup granulated sugar
- 1 cup cream, divided
- 1/2 tsp pure vanilla extract

### Other
- 8 ounces pretzel twists (half of a 16-oz bag)
- 12 ounces chocolate chips or chopped baking chocolate, divided
- Sea salt for sprinkling

## Instructions
1. Combine butter, salt, corn syrup, sugar, and 1/2 cup cream in saucepan. Melt over medium-low.
2. Bring to simmer. Cook without stirring until 236 F.
3. Pour in remaining 1/2 cup cream. Continue cooking to 245-248 F.
4. Remove from heat, swirl in vanilla. Rest 10-15 minutes.
5. Line baking sheet with parchment. Melt 8 oz chocolate. Spread evenly.
6. Sprinkle pretzels over wet chocolate. Press gently.
7. Drizzle caramel over pretzels.
8. Sprinkle remaining 4 oz chocolate chips over warm caramel. Let melt and spread.
9. Sprinkle with sea salt. Let harden.
10. Tear or cut into pieces.

## Tips & Notes
- Use Ghirardelli chocolate for best results.
- Use salted pretzels.
- Don't rush the melting step; don't stir during cooking.
- Pretzels may soften after ~2 days.

## Nutrition (per serving)
- Calories: 219 kcal | Carbs: 31g | Protein: 1g | Fat: 11g
- Saturated Fat: 6g | Cholesterol: 28mg | Sodium: 216mg
""",

"decadent_chocolate_cheesecake.md": """# Decadent Chocolate Cheesecake
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/decadent-chocolate-cheesecake/)
**Cuisine:** american
**Type:** dessert
**Method:** baked
**Prep Time:** 13 hrs 35 mins
**Cook Time:** 1 hr 10 mins
**Total Time:** 14 hrs 45 mins
**Yield:** 12 slices

## Description
A rich, multi-layered chocolate cheesecake for the ultimate chocolate lover. Features a buttery chocolate cookie crust, creamy dark chocolate filling, and silky ganache topping.

## Ingredients

### Crust
- 1 (9 oz) package chocolate cookies
- 1 tbsp sugar
- 6 tbsp melted butter

### Filling
- 10 oz semisweet or bittersweet chocolate, chopped
- 4 packages (8 oz each) cream cheese, room temperature
- 1 1/4 cups + 2 tbsp granulated sugar
- 1/4 cup unsweetened cocoa powder (natural, not Dutch-process)
- 4 large eggs

### Topping
- 3/4 cup whipping cream
- 6 oz semisweet or bittersweet chocolate, chopped
- 1 tbsp sugar
- Chocolate curls for garnish

## Instructions
1. Preheat oven to 350 F. Butter a 9-inch springform pan.
2. Crush cookies; mix with sugar and butter. Press on bottom of pan. Bake 5 min. Cool.
3. Melt 10 oz chocolate; cool until lukewarm.
4. Blend cream cheese, sugar, and cocoa until smooth. Add eggs one at a time. Mix in melted chocolate.
5. Pour over crust. Bake ~1 hour until center is just set.
6. Cool 10 min. Run knife around edges. Cool completely. Chill overnight.
7. Heat cream, 6 oz chocolate, and sugar over low heat until smooth. Pour over cheesecake.
8. Chill 1 hour. Release springform. Top with chocolate curls.
9. Let stand at room temperature 1-2 hours before serving.

## Tips & Notes
- Must chill overnight.
- Can be fully assembled and refrigerated up to 3 days before serving.
- Use chopped baking chocolate, not chocolate chips.
- Use natural unsweetened cocoa, not Dutch-process.
- Freezes well - individual slices can be frozen and thawed.

## Nutrition (per slice)
- Calories: 787 kcal | Carbs: 63g | Protein: 11g | Fat: 56g
- Saturated Fat: 32g | Cholesterol: 183mg | Sodium: 473mg
""",

"easy_cowboy_caviar_dip_aka_shrapnel_dip.md": """# Easy Cowboy Caviar Dip {a.k.a. Shrapnel Dip}
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/amazing-shrapnel-dip/)
**Cuisine:** american, mexican
**Type:** appetizer
**Method:** no-cook
**Prep Time:** 20 minutes
**Total Time:** 20 minutes
**Yield:** 8 servings

## Description
A no-bake, 20-minute dip combining beans, corn, fresh vegetables, and avocado in a zesty Italian dressing. Perfect for BBQs, potlucks, and summer gatherings.

## Ingredients
- 1 (15 oz) can white beans (navy or Great Northern)
- 1 (15 oz) can black beans
- 1 (11 oz) can corn (Green Giant blend recommended) or thawed frozen corn
- 1-2 avocados, diced (add last if making ahead)
- 1 medium red bell pepper, diced (~1/2 cup)
- 1-2 Roma tomatoes, diced
- 2 tbsp finely chopped red onion
- 2-3 tbsp chopped cilantro
- 1/3 cup Italian dressing
- Squeeze of fresh lime (~1/2 tbsp)
- Salt and pepper to taste
- Tortilla chips for serving

## Instructions
1. Drain and dry beans and corn thoroughly.
2. Combine in a bowl with avocado, bell pepper, tomatoes, onion, and cilantro.
3. Pour dressing over mixture and fold gently.
4. Add lime juice, salt, and pepper; mix lightly.
5. Serve immediately with chips.

## Tips & Notes
- Good quality canned corn is key - Green Giant blend recommended.
- If prepping ahead, add avocados just before serving.
- Add cooked, chopped shrimp for an upgrade.
- Add jalapeno for heat.
- Make 1-2 days ahead (without avocado) to let flavors meld.

## Nutrition (per serving)
- Calories: 239 kcal | Carbs: 37g | Protein: 10g | Fat: 7g
- Fiber: 10g | Sugar: 5g | Sodium: 104mg
""",

"easy_homemade_french_bread.md": """# Easy Homemade French Bread
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/french-bread/)
**Cuisine:** french
**Type:** bread
**Method:** baked
**Prep Time:** 3 hrs 15 mins
**Cook Time:** 25 minutes
**Total Time:** 3 hrs 40 mins
**Yield:** 24 slices (2 loaves)

## Description
A beginner-friendly, foolproof French bread recipe that produces light, fluffy loaves rivaling bakery quality. With over 2,500+ 5-star reviews.

## Ingredients
- 2 1/4 cups warm water (110-115 F)
- 2 tbsp granulated sugar
- 1 tbsp instant or active dry yeast
- 2 1/4 tsp salt
- 2 tbsp olive, canola, vegetable, or avocado oil
- 5 1/2-6 cups all-purpose or bread flour

## Instructions
1. Combine water, sugar, and yeast. Let foam 3-5 min (if active dry).
2. Add salt, oil, and 3 cups flour; mix.
3. Gradually add remaining flour until dough clears bowl sides.
4. Knead 2-3 minutes until smooth.
5. Rest 10 min, stir down. Repeat 6 cycles total (or rise 1 hour traditionally).
6. Divide in half. Pat each into ~9x13" rectangle. Roll from long edge.
7. Place seam-side down on parchment-lined baking sheet.
8. Score diagonal gashes on top.
9. Let rise until puffy.
10. Toss 3-4 ice cubes onto oven floor just before baking.
11. Bake at 375 F for 25-30 min until golden.
12. Optional: brush hot loaves with melted butter.

## Tips & Notes
- Judge dough by texture, not exact flour measurements.
- Aim for soft, slightly tacky dough.
- Score before rising to avoid deflating.
- For whole wheat: use white whole wheat flour for half the flour.
- Freezes well after baking.

## Nutrition (per slice)
- Calories: ~85 kcal | Carbs: 17g | Protein: 2g | Fat: 1g
""",

"easy_rustic_crusty_bread_with_tutorial_no_mixer_no_kneading.md": """# Easy Rustic Crusty Bread with Tutorial {No Mixer, No Kneading}
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/rustic-crusty-bread-a-simple-how-to/)
**Cuisine:** american
**Type:** bread
**Method:** baked
**Prep Time:** 2-3 hours
**Cook Time:** 24-28 minutes
**Total Time:** 2-3 hours
**Yield:** 2-4 loaves

## Description
A no-knead, no-mixer-required artisan-style bread with a golden, thin, crunchy crust and a tender, soft crumb. Ready to bake in 2-3 hours from start to finish.

## Ingredients
- 3 cups warm water (~100 F)
- 1 1/2 tablespoons instant yeast
- 1 tablespoon coarse/kosher salt
- 6 1/2 cups unbleached all-purpose flour, plus more for dusting

## Instructions
1. Combine water, yeast, and salt in a large bowl. Stir.
2. Add flour and mix until no dry patches remain. Dough will be loose and shaggy.
3. Cover lightly with a kitchen towel. Let rise at room temperature for 2 hours.
4. Optional: Refrigerate covered dough for up to 2 weeks.
5. Grease hands well. Split dough into 2-4 pieces.
6. Turn edges underneath to create a relatively tight, smooth loaf.
7. Place on parchment paper. Dust with flour.
8. Slash top 3-4 times, about 1/2-inch deep.
9. Cover and let rise until puffy (40 min for room temp, 1.5 hrs for refrigerated).
10. Preheat oven to 450 F with baking stone for 20-30 minutes.
11. Place broiler pan on bottom rack.
12. Slide parchment with loaf onto preheated baking stone.
13. Add 1-2 cups hot water to broiler pan. Close door quickly.
14. Bake 24-28 minutes until well browned and golden.
15. Cool completely before slicing.

## Tips & Notes
- Dough is supposed to be sticky and shaggy - this is normal.
- Slash before the second rise to prevent deflation.
- Store cooled bread in a bread bag at room temperature or freeze.
- Do not refrigerate - it stales faster.
- Half whole wheat flour works well.

## Nutrition (per slice)
- Calories: ~90 kcal | Carbs: 19g | Protein: 3g | Fat: 0.5g
""",

"honey_lime_fruit_salad.md": """# Honey Lime Fruit Salad
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/honey-lime-fruit-salad/)
**Cuisine:** american
**Type:** salad
**Method:** no-cook
**Prep Time:** 20 minutes
**Total Time:** 20 minutes
**Yield:** 6 servings

## Description
A decade-tested fruit salad elevated with a simple honey-lime dressing. The hint of fresh lime and touch of honey take this fruit salad from basic to absolutely extraordinary.

## Ingredients
- 1 (20-oz) can pineapple chunks, drained (or 1.5-2 cups fresh pineapple)
- 1 (15-oz) can mandarin oranges, drained
- 2-3 ripe kiwi, peeled and chopped
- 1 cup red or green grapes, halved
- 1 cup strawberries, hulled and quartered
- Zest of 1 lime (~1/2 tablespoon)
- 1-2 tablespoons honey
- 1/2-1 teaspoon poppy seeds (optional, but recommended)

## Instructions
1. Combine all fruit in a serving bowl.
2. Add lime zest and toss.
3. Drizzle honey over fruit; gently mix until evenly coated.
4. Sprinkle with poppy seeds (if using) and toss again.
5. Serve immediately or refrigerate for no more than 1-2 hours.

## Tips & Notes
- Lime zest (not juice) adds bright flavor without sogginess.
- Best served immediately.
- Avoid soft/watery fruits like raspberries and watermelon.
- Golden kiwis are a delicious upgrade.
- Add fresh mint or basil for extra freshness.

## Nutrition (per serving)
- Calories: 126 kcal | Carbs: 32g | Sugar: 28g
- Fiber: 3g | Protein: 1g | Fat: 0.4g | Sodium: 5mg
""",

"hot_fudge_pudding_cake.md": """# Hot Fudge Pudding Cake
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/hot-fudge-pudding-cake/)
**Cuisine:** american
**Type:** dessert
**Method:** baked
**Prep Time:** 10 minutes
**Cook Time:** 24 minutes
**Total Time:** 34 minutes
**Yield:** 6 servings

## Description
A rich, self-saucing chocolate dessert that forms its own fudge pudding layer during baking. Made with pantry staples and minimal effort.

## Ingredients
- 1 cup sugar
- 1/2 cup cocoa powder
- 1 cup all-purpose flour
- 2 tsp baking powder
- 1/4 tsp salt
- 1/2 cup milk
- 4 tbsp butter, melted
- 1 large egg yolk
- 2 tsp vanilla extract
- 1/2 cup semisweet chocolate chips
- 1 cup boiling water

## Instructions
1. Preheat oven to 350 F. Spray an 8-inch square baking pan.
2. Whisk 1/2 cup sugar + 1/4 cup cocoa powder; set aside.
3. Whisk flour, remaining 1/2 cup sugar, remaining 1/4 cup cocoa, baking powder, and salt.
4. Whisk milk, melted butter, egg yolk, and vanilla until smooth.
5. Stir wet into dry until just combined. Fold in chocolate chips.
6. Scatter batter into pan and spread evenly.
7. Sprinkle reserved cocoa-sugar mixture over top.
8. Gently pour 1 cup boiling water over the top - do NOT stir.
9. Bake 22-24 minutes until top is cracked and sauce bubbles.
10. Cool 10 minutes. Serve warm with vanilla ice cream.

## Tips & Notes
- Do not stir after adding boiling water - this creates the pudding layer.
- The stiff batter is normal; it spreads during baking.
- Double recipe for 9x13-inch pan.
- Both Dutch-process and natural cocoa work well.
- Serve with vanilla ice cream, espresso ice cream, or whipped cream.

## Nutrition (per serving)
- Calories: 397 kcal | Carbs: 63g | Protein: 6g | Fat: 15g
- Saturated Fat: 9g | Cholesterol: 53mg | Sodium: 321mg
""",

"lemon_blueberry_cake_with_whipped_lemon_cream_frosting.md": """# Lemon Blueberry Cake with Whipped Lemon Cream Frosting
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/lemon-blueberry-cake-with-whipped-lemon-cream-frosting/)
**Cuisine:** american
**Type:** dessert
**Method:** baked
**Prep Time:** 3 hr 45 mins
**Cook Time:** 40 minutes
**Total Time:** 4 hr 25 mins
**Yield:** 15 servings

## Description
A showstopping layer cake featuring soft, fluffy lemon cake with fresh blueberries and a whipped lemon cream cheese frosting. One of the best cakes in the history of ever.

## Ingredients

### Cake
- 1 cup butter, softened
- 1 3/4 cups granulated sugar
- 1 tablespoon fresh lemon zest
- 4 large eggs, room temp
- 2 teaspoons vanilla extract
- 2 1/2 cups all-purpose flour
- 2 teaspoons baking powder
- 1/4 teaspoon baking soda
- 1/2 teaspoon salt
- 1 cup buttermilk
- 1/2 cup fresh lemon juice
- 2 cups blueberries (fresh or frozen)
- 2 tablespoons flour (for tossing berries)

### Whipped Lemon Cream Cheese Frosting
- 8 oz cream cheese, softened (full fat)
- 1/2 cup butter, softened
- 4 1/2 cups powdered sugar
- 1-2 teaspoons fresh lemon zest
- 1 tablespoon fresh lemon juice

## Instructions
1. Preheat oven to 350 F. Line two 9-inch round cake pans with parchment.
2. Cream butter, sugar, and lemon zest until light and fluffy (3-4 minutes).
3. Add eggs and vanilla; mix until combined.
4. Whisk flour, baking powder, soda, and salt. Add to wet until partly combined.
5. Add buttermilk and lemon juice; stir by hand until just combined.
6. Toss blueberries with 2 tbsp flour; fold into batter.
7. Bake 25-35 minutes until toothpick comes out clean.
8. Cool 5-10 minutes in pans, then turn onto cooling rack.
9. Whip cream cheese and butter until fluffy. Add powdered sugar, zest, and juice.
10. Frost between layers and on top/sides. Garnish with blueberries and lemon slices.

## Tips & Notes
- Fresh or frozen blueberries both work - do NOT thaw frozen.
- Zest lemons before juicing - need about 4-5 lemons total.
- Buttermilk substitute: half sour cream + half milk.
- Do not use neufchatel or light cream cheese for frosting.
- Cake layers freeze well. Frosted cake lasts several days refrigerated.

## Nutrition (per slice)
- Calories: 550 kcal | Carbs: 81g | Protein: 4g | Fat: 25g
- Saturated Fat: 15g | Cholesterol: 66mg | Sodium: 364mg
""",

"little_lemonies_yummy_lemon_brownies.md": """# Little Lemonies {Yummy Lemon Brownies}
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/lemonies/)
**Cuisine:** american
**Type:** dessert
**Method:** baked
**Prep Time:** 1 hr 20 mins
**Cook Time:** 20 minutes
**Total Time:** 1 hr 40 mins
**Yield:** 24 small squares

## Description
Soft, chewy lemon bars with a brownie-like texture - no chocolate involved! Features a tender lemon base topped with a bright, sweet-tart glaze. Best served chilled.

## Ingredients

### Lemon Batter
- 1 cup all-purpose flour
- 3/4 cup granulated sugar
- 1 tbsp lemon zest (from ~1 large lemon)
- 1/4 tsp baking powder
- 1/4 tsp salt
- 1/2 cup salted butter, melted and cooled
- 2 large eggs + 1 egg yolk
- 3 tbsp fresh lemon juice
- 1 tsp vanilla extract

### Lemon Glaze
- 3/4 cup powdered sugar
- 1 tbsp fresh lemon juice
- 1/2 tsp lemon zest

## Instructions
1. Preheat oven to 355 F. Line an 8x8-inch pan with parchment; grease lightly.
2. Whisk dry ingredients (flour, sugar, zest, baking powder, salt).
3. In another bowl, whisk wet ingredients (butter, eggs, yolk, lemon juice, vanilla).
4. Combine wet into dry; mix until just blended.
5. Spread batter evenly in pan.
6. Bake 18-20 min until top springs back when touched.
7. Cool completely in pan.
8. Whisk glaze ingredients; spread thinly over cooled bars.
9. Refrigerate 1-2 hours to set glaze.
10. Lift out using parchment; cut into 1-inch squares.

## Tips & Notes
- Need 2-3 large lemons total for juice and zest.
- Chill 1-2 hours after glazing for best flavor and clean cuts.
- Gluten-free: Bob's Red Mill 1:1 GF flour works perfectly.
- Dairy-free: Avocado oil replaces butter successfully.
- Delicious at room temp, but chilled is superior.

## Nutrition (per 1 square)
- Calories: 100 kcal | Carbs: 14g | Sugar: 10g
- Protein: 1g | Fat: 4g (Saturated: 3g)
- Cholesterol: 32mg | Sodium: 68mg
""",

"my_favorite_cherry_pie_in_the_history_of_ever.md": """# My Favorite Cherry Pie in the History of Ever
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/my-favorite-cherry-pie-in-the-history-of-ever/)
**Cuisine:** american
**Type:** dessert
**Method:** baked
**Prep Time:** 4 hrs 30 mins
**Cook Time:** 1 hr 5 mins
**Total Time:** 5 hrs 35 mins
**Yield:** 8 slices (9-inch pie)

## Description
A classic cherry pie recipe using sweet dark cherries with a lattice crust. The definitive, perfected version after years of testing. The tapioca flour + cornstarch combination creates a perfectly set filling.

## Ingredients

### Filling
- 5 cups pitted sweet, dark cherries (~2 lbs whole fruit)
- 2 tablespoons fresh lemon juice
- 1/4 teaspoon almond extract (essential!)
- 3/4 cup granulated sugar
- 1/2 teaspoon coarse kosher salt
- 1/3 cup tapioca starch/flour
- 1 tablespoon cornstarch
- 1 tablespoon butter

### Egg Wash
- 1 egg yolk
- 2 teaspoons water
- 2 teaspoons cream or milk

### Crust
- Double crust 9-inch pie dough

## Instructions
1. Keep everything cold at every stage.
2. Roll bottom crust to ~12-inch diameter. Place in 9-inch pie plate. Refrigerate.
3. Combine cherries, lemon juice, almond extract, sugar, salt, tapioca starch, and cornstarch.
4. Roll top crust to 10-inch diameter; cut into 10-12 strips for lattice.
5. Scoop filling into bottom crust. Dot with butter.
6. Weave lattice crust over filling. Trim and flute edges.
7. Refrigerate 30-60 minutes.
8. Preheat oven to 400 F. Brush with egg wash.
9. Place pie on parchment or foil-lined baking sheet.
10. Bake 50-60 minutes until crust is golden and filling is bubbly.
11. Cool 2-3 hours before serving. Filling sets as it cools.

## Tips & Notes
- Tapioca flour + cornstarch is the critical thickener combo.
- Almond extract (1/4 tsp) is essential despite the author normally disliking almond flavor.
- Keep dough cold at every stage.
- Bake long enough - underbaking = permanently soupy filling.
- For sour cherries: decrease lemon juice to 1 tsp, increase sugar to 1 cup.
- Frozen cherries: thaw and drain very well.

## Nutrition (per slice)
- Calories: ~450 kcal | Carbs: 65g | Protein: 5g | Fat: 18g
""",

"my_mom8217s_famous_caramels.md": """# My Mom's Famous Caramels
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/sugar-rush-11-my-moms-famous-caramels/)
**Cuisine:** american
**Type:** dessert
**Method:** stovetop
**Prep Time:** 10 minutes
**Cook Time:** 45 minutes
**Total Time:** 55 minutes
**Yield:** 4-6 dozen caramels (9x13-inch pan)

## Description
A beloved family recipe made for over 30 years as a holiday tradition. These creamy, soft caramels are the best ever and a staple Christmas candy.

## Ingredients
- 2 cups sugar
- 1 1/2 cups light corn syrup
- 1 can sweetened condensed milk (add only 1/2 initially)
- 1/4 teaspoon salt
- 1 cup butter
- 2 teaspoons vanilla
- 1 1/2 cups chopped toasted pecans (optional)

## Instructions
1. Butter a 9x13-inch metal baking pan.
2. Combine sugar, corn syrup, 1/2 can sweetened condensed milk, salt, and butter in heavy saucepan.
3. Heat over medium-low, stir constantly until sugar dissolves and mixture boils.
4. Add remaining condensed milk once boiling begins.
5. Insert candy thermometer.
6. Stop stirring once mixture returns to a boil.
7. Boil without stirring to soft ball stage (234 F) for very soft caramels.
8. Remove from heat immediately at target temperature.
9. Stir in vanilla and pecans (if using).
10. Pour carefully into prepared pan - do not scrape pan residue.
11. Cool completely, then cut into squares and wrap in waxed paper.

## Tips & Notes
- Calibrate your candy thermometer before each use.
- Do NOT stir after adding the second half of sweetened condensed milk.
- Cook over medium-low heat to avoid scorching.
- When pouring, do not scrape the bottom or sides of the saucepan.
- For firmer caramels, cook up to 248 F (firm ball stage).

## Nutrition (per caramel)
- Calories: ~65 kcal | Carbs: 10g | Protein: 0.5g | Fat: 2.5g
""",

"orange_sweet_rolls.md": """# Orange Sweet Rolls
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/orange-sweet-rolls/)
**Cuisine:** american
**Type:** bread
**Method:** baked
**Prep Time:** 3 hrs 25 mins
**Cook Time:** 25 minutes
**Total Time:** 3 hrs 50 mins
**Yield:** 12-14 rolls

## Description
A beloved homemade sweet roll recipe featuring a tender, buttermilk-enriched yeast dough filled with a rich, citrusy orange-butter-sugar mixture and finished with a light orange glaze.

## Ingredients

### Dough
- 3/4 cup warm buttermilk
- 6 tbsp melted and cooled butter
- 3 large eggs
- 4 1/4 cups flour
- 1/4 cup sugar
- 2 1/4 tsp instant yeast
- 1 1/4 tsp salt

### Orange Filling
- 1/2 cup softened butter
- 1 cup sugar
- 2 tbsp freshly squeezed orange juice
- Zest from 2 large oranges

### Orange Glaze
- 1 1/2 cups powdered sugar
- 3 tbsp orange juice
- 1/2 tsp reserved orange zest

## Instructions
1. Whisk warm buttermilk and melted butter. Add flour, sugar, yeast, salt, and eggs. Mix until combined.
2. Knead on medium for 10 min until smooth and elastic.
3. Rise in greased bowl until doubled (2-2.5 hours).
4. Mix filling ingredients.
5. Roll dough into 16" x 12" rectangle. Spread filling evenly.
6. Roll tightly from long edge. Slice into 12 even rolls.
7. Optional: stretch each roll and twist into figure-8.
8. Place on greased pan. Let rise until doubled (1-1.5 hours).
9. Bake at 350 F for 22-25 minutes until lightly golden.
10. Drizzle glaze over warm rolls.

## Tips & Notes
- Judge dough by texture, not exact flour amount.
- Twisted rolls taste better than traditional spirals.
- Chill shaped rolls before baking if filling leaks.
- Prepare dough, shape rolls, and refrigerate overnight for make-ahead.
- Add 1 tsp nutmeg to filling for orange-nutmeg twist.

## Nutrition (per roll)
- Calories: 456 kcal | Carbs: 72g | Protein: 8g | Fat: 16g
- Sugar: 37g | Fiber: 2g | Sodium: 396mg
""",

"orange_zested_cranberry_white_chocolate_bliss_bars.md": """# Orange Zested Cranberry White Chocolate Bliss Bars
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/orange-zested-cranberry-white-chocolate-bliss-bars-a-slightly-lighter-version/)
**Cuisine:** american
**Type:** dessert
**Method:** baked
**Prep Time:** 20 minutes
**Cook Time:** 22 minutes
**Total Time:** 42 minutes
**Yield:** 24 bars (9x13-inch pan)

## Description
A lighter, homemade version of Starbucks' popular Cranberry Bliss Bars featuring a chewy blondie base with dried cranberries and white chocolate, cream cheese frosting with orange zest, and white chocolate drizzle.

## Ingredients

### Blondies
- 1/2 cup salted butter
- 1 1/3 cups packed light brown sugar
- 2 large eggs
- 1/2 tsp vanilla extract
- 1 tsp freshly grated orange zest
- 2 1/8 cups all-purpose flour
- 1 1/2 tsp baking powder
- 1/4 tsp salt
- 1/8 tsp ground cinnamon
- 1/2 cup dried cranberries, coarsely chopped
- 4 oz white baking chocolate, chopped

### Frosting and Topping
- 8 oz light cream cheese, softened
- 3/4 cup powdered sugar
- 1/4 tsp vanilla extract
- 2 tsp freshly grated orange zest
- 4 oz white baking chocolate, melted
- 1/2 cup dried cranberries, coarsely chopped

## Instructions
1. Preheat oven to 350 F. Grease a 9x13-inch pan.
2. Melt butter; stir in brown sugar. Whisk in eggs, vanilla, and orange zest.
3. Mix in flour, baking powder, salt, and cinnamon. Fold in cranberries and white chocolate.
4. Spread batter evenly. Bake 18-22 minutes until toothpick comes out clean.
5. Cool completely in pan.
6. Beat cream cheese and powdered sugar until fluffy. Add vanilla, orange zest, and half the melted white chocolate.
7. Spread frosting on cooled bars. Sprinkle with cranberries; drizzle remaining chocolate.
8. Refrigerate until chocolate sets. Best served chilled.

## Tips & Notes
- Use white baking bars (not chips) for smoother melting.
- Orange zest in both batter and frosting for depth.
- Chop cranberries coarsely for even distribution.
- Unfrosted bars freeze well.
- Gluten-free flour works as substitute.

## Nutrition (per bar)
- Calories: 227 kcal | Carbs: 35g | Protein: 3g | Fat: 9g
""",

"oreo_cheesecake_bites.md": """# Oreo Cheesecake Bites
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/oreo-cheesecake-bites/)
**Cuisine:** american
**Type:** dessert
**Method:** baked
**Prep Time:** 2 hrs 15 mins
**Cook Time:** 40 minutes
**Total Time:** 2 hrs 55 mins
**Yield:** 36 bites

## Description
Creamy cheesecake with crushed Oreos, baked in a 9x13 pan, cut into bite-sized pieces and drizzled with white and dark chocolate. Cheesecake and Oreo bliss in bite-size form.

## Ingredients
- 36 Oreo cookies, divided
- 1/4 cup butter
- 4 packages (8 oz each) cream cheese, softened
- 1 cup granulated sugar
- 1 cup sour cream
- 1 tsp vanilla extract
- 4 large eggs
- 4 oz semisweet chocolate
- 4 oz white chocolate

## Instructions
1. Preheat oven to 325 F.
2. Line a 9x13-inch pan with foil. Finely crush 24 Oreos; mix with melted butter. Press into pan.
3. Beat cream cheese and sugar until smooth. Add sour cream and vanilla. Add eggs one at a time.
4. Chop remaining 12 Oreos; fold into batter. Pour over crust.
5. Bake 35-40 minutes until sides are set and center almost set.
6. Cool completely. Refrigerate at least 2 hours.
7. Lift out using foil; cut into bite-sized squares.
8. Melt chocolates separately. Drizzle over bites.
9. Chill until serving. Freezer-friendly up to 1 month.

## Tips & Notes
- Use whole Oreos (filling included) for crust.
- Look for puffed edges and minimal center jiggle for doneness.
- Glass pans may require 45-60 minutes.
- Flavors improve overnight.
- Try Mini Eggs, Thin Mints, or candy bars instead of Oreos.

## Nutrition (per bite)
- Calories: 231 kcal | Carbs: 27g | Protein: 4g | Fat: 13g
- Saturated Fat: 7g | Cholesterol: 52mg | Sodium: 189mg
""",

"overnight_cinnamon_and_sugar_sweet_rolls.md": """# Overnight Cinnamon and Sugar Sweet Rolls
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/overnight-cinnamon-and-sugar-twists/)
**Cuisine:** american
**Type:** bread
**Method:** baked, overnight
**Prep Time:** 9 hrs 30 mins
**Cook Time:** 14 minutes
**Total Time:** 9 hrs 44 mins
**Yield:** 24 rolls

## Description
Cinnamon and sugar sweet rolls made easy with an overnight refrigerator method. No kneading, no mixer required. The unique twisted shape creates flaky, buttery layers.

## Ingredients

### Dough
- 4 1/2 cups all-purpose flour
- 2 tbsp instant yeast
- 1/3 cup granulated sugar
- 1 1/2 tsp salt
- 4 large eggs
- 1 1/4 cup hot water
- 8 tbsp salted butter, melted

### Filling
- 4 tbsp salted butter, melted
- 1/2 cup granulated sugar
- 1 1/2 tsp ground cinnamon

### Glaze
- 1 cup powdered sugar
- 1 tbsp melted butter
- 2 tbsp milk (+ more as needed)
- Splash of vanilla extract

## Instructions
1. Mix dry ingredients in a large bowl; create a well.
2. Add wet ingredients into the well. Stir until soft, lumpy dough forms - it should be very wet.
3. Cover and refrigerate overnight (8-10 hrs).
4. Next morning: Roll dough into ~24"x7" rectangle on floured surface.
5. Spread filling: melted butter then cinnamon-sugar mix.
6. Fold dough in half lengthwise; cut into 1" strips.
7. Twist each strip several times, then coil into a circle.
8. Place on parchment-lined baking sheet (~12 per tray).
9. Let rise 1 hour until puffy.
10. Bake at 375 F for 12-14 min - just barely golden.
11. Drizzle glaze over slightly cooled rolls.

## Tips & Notes
- Dough texture is intentionally wet - this is normal.
- Don't overbake - rolls dry out quickly.
- Shape rolls the night before for extra make-ahead convenience.
- Orange rolls variation: replace water with orange juice + zest.
- Freeze unglazed rolls; reheat and glaze before serving.

## Nutrition (per roll)
- Calories: 198 kcal | Carbs: 30g | Protein: 4g | Fat: 7g
""",

"overnight_strawberry_cream_cheese_sweet_rolls.md": """# Overnight Strawberry Cream Cheese Sweet Rolls
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/overnight-strawberry-cream-cheese-sweet-rolls/)
**Cuisine:** american
**Type:** bread
**Method:** baked, overnight
**Prep Time:** 10 hrs 30 mins
**Cook Time:** 14 minutes
**Total Time:** 10 hrs 44 mins
**Yield:** 24 sweet rolls

## Description
Make-ahead breakfast pastry featuring flaky, tender dough filled with creamy lemon-zest cream cheese and tart strawberry jam. Perfect for holidays like Easter.

## Ingredients

### Dough
- 4 1/2 cups all-purpose flour
- 2 tablespoons instant yeast
- 1/3 cup granulated sugar
- 1 1/2 teaspoons salt
- 4 large eggs
- 1 1/4 cups hot water (90-100 F)
- 8 tablespoons salted butter, melted

### Filling
- 8 oz cream cheese, softened
- 3/4 cup powdered sugar
- Zest of 1 lemon (~1 tsp)
- 1-2 cups strawberry jam

### Glaze
- 1 cup powdered sugar
- 1 tablespoon melted butter
- 2 tablespoons milk (+ more as needed)
- Splash of vanilla extract

## Instructions
1. Whisk dry ingredients. Add eggs, hot water, and melted butter. Mix into soft, wet dough.
2. Cover and refrigerate 8-10 hours (or overnight).
3. Blend cream cheese, powdered sugar, and lemon zest until smooth.
4. Roll dough into 24" x 7-8" rectangle. Spread cream cheese mixture, then dollop jam.
5. Fold dough in half lengthwise. Cut into 1" strips. Twist each strip and coil into a circle.
6. Place on parchment-lined baking sheets (~12 per tray).
7. Cover with greased plastic wrap; let rise 1 hour until puffy.
8. Bake at 375 F for 12-14 minutes until just golden. Do not overbake.
9. Drizzle glaze over slightly cooled rolls.

## Tips & Notes
- Use jam with strawberries as the first ingredient (not sugar or corn syrup).
- Messy filling is normal! Pat it back in if it oozes out.
- Shape rolls the night before, cover, and refrigerate for extra early prep.
- Refrigerate baked rolls for 4-5 days. Baked rolls can also be frozen.
- Raspberry jam is a highly recommended substitute.

## Nutrition (per roll)
- Calories: 273 kcal | Carbs: 45g | Protein: 4g | Fat: 9g
- Saturated Fat: 5g | Cholesterol: 53mg | Sodium: 234mg
""",

"peanut_butter_cup_cheesecake_with_chocolate_cookie_crust.md": """# Peanut Butter Cup Cheesecake with Chocolate Cookie Crust
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/peanut-butter-cup-cheesecake-with-chocolate-cookie-crust/)
**Cuisine:** american
**Type:** dessert
**Method:** baked
**Prep Time:** 12 hrs 30 mins
**Cook Time:** 1 hr 40 mins
**Total Time:** 14 hrs 10 mins
**Yield:** 15 slices

## Description
A rich, make-ahead dessert combining chocolate cookie crust, peanut butter cheesecake filling, chopped peanut butter cups, chocolate ganache, and peanut butter whipped cream.

## Ingredients

### Crust
- 20-22 Oreo cookies
- 2 tbsp brown sugar
- 1/2 cup roasted, salted peanuts
- 6 tbsp melted butter

### Filling
- 3 x 8-oz packages cream cheese, softened
- 1 cup granulated sugar
- 1 tbsp cornstarch
- 1/2 cup sour cream
- 3/4 cup creamy peanut butter
- 1 tsp vanilla extract
- 3 large eggs
- 10 regular-sized peanut butter cups, chopped

### Ganache Topping
- 1/4 cup heavy cream
- 1/2 cup semisweet/bittersweet chocolate chips
- 1/4 tsp vanilla extract

### Peanut Butter Whipped Cream
- 1 cup heavy cream
- 1/4 cup powdered sugar
- 1/4 tsp vanilla extract
- 1/4 cup creamy peanut butter

## Instructions
1. Preheat oven to 300 F. Grease a 9" or 10" springform pan.
2. Blend Oreos, brown sugar, and peanuts into crumbs. Add butter. Press into pan. Bake 8 min. Cool.
3. Beat cream cheese, sugar, cornstarch, sour cream, peanut butter, and vanilla until smooth.
4. Add eggs; mix just until combined (do not overmix). Fold in chopped peanut butter cups.
5. Place a 9x13" pan with 2-3 cups boiling water on bottom rack. Bake cheesecake on upper rack 50-65 min.
6. Turn off oven, prop door open, rest inside 30 min. Cool completely.
7. Heat cream until simmering. Stir in chocolate and vanilla until smooth. Spread over cheesecake. Refrigerate overnight.
8. Whip cream ingredients until thick. Top cheesecake before serving.

## Tips & Notes
- Avoid overmixing after adding eggs to prevent cracking.
- Use creamy commercial peanut butter (like Skippy).
- Ganache hides cracks - so it's forgiving.
- Use true heavy cream (35%+ milk fat).
- Must be made ahead - ideal for stress-free entertaining.

## Nutrition (per slice)
- Calories: 656 kcal | Carbs: 45g | Protein: 12g | Fat: 50g
- Saturated Fat: 23g | Cholesterol: 127mg | Sodium: 407mg
""",

"penne_with_roasted_asparagus_and_balsamic_butter.md": """# Penne with Roasted Asparagus and Balsamic Butter
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/penne-with-roasted-asparagus-and-balsamic-butter/)
**Cuisine:** american, italian
**Type:** main
**Method:** stovetop
**Prep Time:** 20 minutes
**Cook Time:** 20 minutes
**Total Time:** 40 minutes
**Yield:** 6 servings

## Description
A beloved, simple pasta dish featuring roasted asparagus, balsamic reduction, butter, and penne pasta. Perfect for spring when asparagus is in season.

## Ingredients

### Roasted Asparagus
- 1 1/2-2 lbs fresh asparagus, cut into 1-inch pieces
- 1 tbsp olive oil
- 1/4 tsp coarse kosher salt
- 1/4 tsp freshly ground black pepper

### Balsamic Reduction
- 1/2 cup balsamic vinegar
- 1 tsp light or dark brown sugar (optional)
- Pinch of black pepper
- 1/2 tsp coarse kosher salt

### Pasta
- 1 lb penne pasta
- 4 tbsp butter (can be browned for enhanced flavor)
- 1/3-1/2 cup freshly grated Parmesan cheese

## Instructions
1. Preheat oven to 400 F. Toss asparagus with oil, salt, and pepper. Roast ~10 min until tender.
2. Simmer balsamic vinegar until reduced to ~3 tbsp (5-10 min). Stir in brown sugar, pepper, and salt.
3. Boil penne until al dente. Drain and return to pot.
4. Toss pasta with butter until melted. Add balsamic reduction; toss.
5. Fold in roasted asparagus and Parmesan. Season to taste.
6. Serve warm or at room temperature.

## Tips & Notes
- Browned butter elevates flavor significantly.
- Use broccoli or cauliflower if asparagus is unavailable.
- Balsamic glaze can replace homemade reduction.
- Add grilled chicken, trout, garlic, sugar snap peas, or cherry tomatoes.
- The salty punch of the cheese cuts through the rich balsamic - don't skip it!

## Nutrition (per serving)
- Calories: 424 kcal | Carbs: 65g | Protein: 15g | Fat: 11g
- Fiber: 5g | Sugar: 8g | Sodium: 458mg
""",

"soft_and_chewy_caramel_popcorn.md": """# Soft and Chewy Caramel Popcorn
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/soft-and-chewy-caramel-popcorn/)
**Cuisine:** american
**Type:** snack
**Method:** stovetop
**Prep Time:** 30 minutes
**Cook Time:** 5 minutes
**Total Time:** 35 minutes
**Yield:** 12 cups

## Description
Best ever soft and chewy caramel popcorn! This easy recipe is a tried-and-true favorite. Not crunchy - soft and chewy, and highly customizable.

## Ingredients
- 10-12 cups plain popcorn (~1/3 cup kernels, popped)
- 1 cup packed light or dark brown sugar
- 1/2 cup salted butter
- 1/4 cup corn syrup
- Pinch of coarse kosher salt
- 1/2 teaspoon baking soda
- 1 teaspoon vanilla extract

## Instructions
1. Place popcorn in a large bowl (extra room needed for tossing).
2. Combine brown sugar, butter, corn syrup, and salt in saucepan.
3. Heat over medium-low until melted and combined.
4. Increase heat to medium; bring to a simmer, stirring often.
5. Cook 3-4 minutes, stirring frequently.
6. Remove from heat. Quickly whisk in baking soda and vanilla (mixture will foam).
7. Immediately drizzle caramel over popcorn while tossing to coat evenly.
8. Serve immediately or within a couple of hours.

## Tips & Notes
- Work quickly - caramel hardens as it cools.
- For more caramel-soaked: use less popcorn (8-10 cups).
- Add 8-10 large marshmallows after simmering for ultra-gooey texture.
- Replace vanilla with 1/2 tsp maple extract for maple twist.
- Best eaten the day it's made. Does not store well long-term.
- High altitude: reduce simmering time by ~1 minute.

## Nutrition (per 1-cup serving)
- Calories: 194 kcal | Carbs: 31g | Protein: 1g | Fat: 8g
- Saturated Fat: 5g | Cholesterol: 20mg | Sodium: 123mg
""",

"spaghetti_pie.md": """# Spaghetti Pie
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/spaghetti-pie-my-familys-favorite-dinner/)
**Cuisine:** american, italian
**Type:** main
**Method:** baked
**Prep Time:** 15 minutes
**Cook Time:** 45 minutes
**Total Time:** 1 hour
**Yield:** 6 servings

## Description
A comforting, baked pasta dish combining tender spaghetti with creamy cheeses and rich red sauce, pressed into a pie plate and baked until golden. Delicious, tender noodles in creamy and red sauces.

## Ingredients

### Pasta and Protein
- 12 oz thin spaghetti or vermicelli
- 1 lb lean ground beef or ground turkey
- 1 small white or yellow onion, diced
- 1 clove garlic, finely minced
- 1 tsp salt
- 1/2 tsp black pepper

### Sauce
- 1 (28 oz) can crushed tomatoes
- 1 (16 oz) can tomato sauce
- 1 tsp dried basil
- 1/2 tsp dried oregano

### Cheese Mixture
- 4 oz light cream cheese, softened
- 1/2 cup lowfat cottage cheese
- 3/4 cup Parmesan cheese, divided
- 3/4 cup mozzarella cheese, divided

## Instructions
1. Preheat oven to 400 F. Coat a deep 9-10 inch pie plate with cooking spray.
2. Cook spaghetti al dente. Brown meat with onion, garlic, salt, and pepper.
3. Stir in crushed tomatoes, tomato sauce, basil, and oregano. Simmer 10 minutes.
4. Drain hot pasta; toss with cream cheese until melted.
5. Add cottage cheese, 1/2 cup Parmesan, and 1/2 cup mozzarella. Toss.
6. Stir in 2 cups of the red sauce.
7. Press noodle mixture firmly into pie plate.
8. Top with remaining 1/4 cup Parmesan and 1/4 cup mozzarella.
9. Bake 20-22 minutes until bubbly and golden.
10. Let rest 10 minutes before slicing. Serve with extra red sauce.

## Tips & Notes
- Cottage cheese substitute: ricotta or sour cream.
- Must use deep-dish pie plate.
- Make-ahead/freezer friendly: assemble, freeze unbaked.
- Customizable: omit meat or use Italian sausage.
- Part-skim mozzarella from block (not fresh soft mozzarella).

## Nutrition (per serving)
- Calories: 524 kcal | Carbs: 55g | Protein: 25g | Fat: 22g
""",

"sweet_baked_ham.md": """# Sweet Baked Ham
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/sweet-baked-ham-the-most-unique-and-delicious-ham-ive-ever-had/)
**Cuisine:** american
**Type:** main
**Method:** baked
**Prep Time:** 10 minutes
**Cook Time:** 4 hours
**Total Time:** 4 hrs 10 mins
**Yield:** 10 servings

## Description
A unique, two-step method for baking ham that uses a vinegar-water boil to achieve fall-apart tenderness, followed by a sweet brown sugar-mustard bake. The best ham ever!

## Ingredients
- 5-7 lb precooked bone-in ham (not spiral-sliced)
- White distilled vinegar
- Water
- 1 cup brown sugar
- 1 1/2 tablespoons ground dry mustard

## Instructions
1. Place ham in a large pot. Cover with 2 parts water : 1 part vinegar (at least 1-2 inches above ham).
2. Bring to a boil, then reduce to medium and simmer vigorously for 2-3 hours until meat falls off the bone.
3. Remove ham to a rimmed sheet pan. Cool slightly, then pull meat off bone and shred.
4. Mix 1 cup brown sugar + 1 1/2 tbsp dry mustard.
5. Layer half the shredded ham in a 9x9-inch baking dish. Sprinkle half the sugar-mustard mix. Repeat layers.
6. Cover tightly with foil. Bake at 325 F for 1 hour.
7. Serve warm or at room temperature.

## Tips & Notes
- DO NOT use spiral-sliced ham - it will be dry.
- Bone-in is strongly preferred for maximum tenderness.
- The vinegar-water boil is the secret to ultra-tender meat.
- Boil and shred up to several days ahead.
- Freezes well. Instant Pot option available.

## Nutrition (per serving)
- Calories: 427 kcal | Protein: 35g | Carbs: 14g | Fat: 24g
""",

"the_best_and_only_pie_crust_recipe_038_tutorial_you8217ll_ev.md": """# The Best and Only Pie Crust Recipe {& Tutorial} You'll Ever Need
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/the-only-pie-crust-recipe-tutorial-youll-ever-need/)
**Cuisine:** american
**Type:** bread
**Method:** baked
**Prep Time:** 20 minutes
**Total Time:** 20 minutes + chilling
**Yield:** 1 single 9-inch pie crust

## Description
The best and only pie crust recipe you will ever need! Uses sour cream instead of ice water for an incredibly flaky, buttery, easy-to-work-with dough.

## Ingredients
- 1 1/2 cups unbleached all-purpose flour (spoon-and-sweep method)
- 1/4 teaspoon salt
- 2 teaspoons granulated sugar
- 10 tablespoons salted butter, frozen
- 1/2 cup full-fat sour cream, plus extra 1-3 tsp if needed

## Instructions
1. Whisk flour, salt, and sugar in a medium bowl.
2. Grate frozen butter using the large holes of a box grater. Toss into flour with a fork.
3. Add sour cream; press and mash with a fork. Finish by pressing dough together with hands quickly and firmly.
4. If too dry, add sour cream 1 tsp at a time until dough holds together.
5. Shape into a flat disc, wrap in plastic. Refrigerate 1-2 days or freeze up to 1 month.
6. Roll from center outward on a lightly floured surface, turning dough frequently.
7. Transfer to pie plate. Gently lift edges and settle - do not press or stretch.
8. Trim edges to 1/4-inch overhang. Fold under and crimp.
9. Refrigerate 30 minutes before baking.
10. For blind baking: line with foil, fill with pie weights. Bake at 350 F for 20-25 min. Remove weights; bake 10-12 min more.

## Tips & Notes
- Measure flour lightly using spoon-and-sweep method.
- Keep butter cold at all times.
- Minimal handling is key - overworking = tough crust.
- Double the recipe for a double-crust pie.
- Works for sweet and savory pies, quiches, tarts.
- Food processor option: pulse butter into flour, then pulse in sour cream.

## Nutrition (per serving, 8 servings)
- Calories: ~215 kcal | Carbs: 18g | Protein: 3g | Fat: 14g
- Saturated Fat: 9g | Cholesterol: 38mg | Sodium: 210mg
""",

"the_best_carrot_cake_with_whipped_cream_cheese_frosting.md": """# The Best Carrot Cake with Whipped Cream Cheese Frosting
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/unbelievable-carrot-cake/)
**Cuisine:** american
**Type:** dessert
**Method:** baked
**Prep Time:** 20 minutes
**Cook Time:** 45-50 minutes
**Total Time:** 1 hr 10 mins
**Yield:** 15 servings

## Description
Hands-down the best carrot cake ever! Simple and straightforward, ultra moist, fluffy, and incredibly delicious. One-bowl, no mixer required.

## Ingredients

### Cake
- 1 lb medium carrots (6-7 large), ends trimmed
- 1 1/2 cups granulated sugar
- 1/2 cup packed light brown sugar
- 4 large eggs
- 1 cup neutral oil
- 1/2 cup unsweetened applesauce
- 2 1/2 cups all-purpose flour
- 1 1/4 tsp baking powder
- 1 1/4 tsp ground cinnamon
- 1 tsp baking soda
- 1/2 tsp table salt
- 1/2 tsp ground nutmeg
- 1/8 tsp ground cloves

### Cream Cheese Frosting
- 8 oz cream cheese, softened
- 5 tbsp butter, softened
- 1 tbsp sour cream
- 1/2 tsp vanilla extract
- 1 1/4 cups powdered sugar
- Toasted chopped pecans (optional)

## Instructions
1. Preheat oven to 350 F. Grease pan(s); line with parchment if using round pans.
2. Shred carrots finely (~3 cups).
3. Whisk sugars + eggs. Add oil + applesauce. Mix until emulsified.
4. Add dry ingredients. Mix until just combined. Fold in carrots. Do not overmix.
5. Bake: 9x13" pan 45-50 min, two 9" rounds 32-35 min, cupcakes 17-20 min.
6. Cool completely.
7. Beat cream cheese, butter, sour cream, vanilla. Add powdered sugar. Mix until creamy.
8. Frost cake. Top with pecans. Serve room temp or chilled.

## Tips & Notes
- Mix batter just until incorporated. Overmixing = denser cake.
- Chilled carrot cake is heavenly.
- Frost and refrigerate up to 24 hours in advance.
- Zucchini can replace carrots 1:1 for allergies.
- Pineapple (drained) can replace applesauce.
- Double frosting for layer cake or cupcakes.

## Nutrition (per serving)
- Calories: 348 kcal | Carbs: 59g | Protein: 5g | Fat: 11g
- Saturated Fat: 6g | Cholesterol: 71mg | Sodium: 317mg
""",

"the_best_lemon_bars.md": """# The Best Lemon Bars
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/perfect-lemon-bars/)
**Cuisine:** american
**Type:** dessert
**Method:** baked
**Prep Time:** 20 minutes
**Cook Time:** 40 minutes
**Total Time:** 1 hour
**Yield:** 24 bars (9x13-inch pan)

## Description
The best lemon bars on the planet with the perfect ratio of crust to delicious, creamy, ultra-lemony filling and a healthy sprinkle of powdered sugar.

## Ingredients

### Crust
- 1 3/4 cups all-purpose flour
- 2/3 cup powdered sugar (+ extra for topping)
- 1/4 cup cornstarch
- 1/2 teaspoon salt
- 12 tablespoons butter, cool room temperature, cut into 1-inch pieces

### Filling
- 4 large eggs
- 1 1/3 cups granulated sugar
- 3 tablespoons all-purpose flour
- 2 teaspoons grated lemon zest
- 2/3 cup freshly squeezed lemon juice (from 3-4 large lemons)
- 1/3 cup milk
- Pinch of salt

## Instructions
1. Preheat oven to 350 F. Line a 9x13-inch pan with foil/parchment; lightly grease.
2. Whisk dry crust ingredients. Cut in butter until mixture resembles coarse meal. Press into pan. Refrigerate 15-30 min.
3. Bake crust 15-20 min until edges are lightly golden.
4. Whisk eggs, sugar, salt, and flour. Stir in lemon zest, juice, and milk.
5. Pour filling over warm crust. Reduce oven to 325 F. Bake 18-20 min until filling is slightly firm.
6. Cool completely. Dust with powdered sugar before cutting.

## Tips & Notes
- Fresh lemon juice is essential - bottled juice results in flat flavor.
- Zest lemons before juicing.
- For easier mixing, soften or slightly melt butter and combine with electric mixer.
- Best served at room temperature after cooling.

## Nutrition (per bar)
- Calories: 163 kcal | Carbs: 24g | Protein: 2g | Fat: 7g
- Saturated Fat: 4g | Cholesterol: 46mg | Sodium: 112mg
""",

"the_best_monkey_bread.md": """# The Best Monkey Bread
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/the-best-monkey-bread/)
**Cuisine:** american
**Type:** bread
**Method:** baked
**Prep Time:** 3 hrs 45 mins
**Cook Time:** 35 minutes
**Total Time:** 4 hrs 20 mins
**Yield:** 8-10 servings

## Description
Homemade pull-apart monkey bread featuring from-scratch yeast dough, buttery cinnamon-sugar coating, and a sweet glaze. Like a pull-apart cinnamon roll!

## Ingredients

### For the Pan
- 2 tablespoons softened butter

### Dough
- 2 tablespoons melted butter
- 1 cup warm milk (105-110 F)
- 1/3 cup warm water (105-110 F)
- 1/4 cup granulated sugar
- 2 1/4 teaspoons instant yeast
- 3 1/4 cups all-purpose flour
- 2 teaspoons salt

### Brown Sugar Coating
- 1 cup packed light brown sugar
- 2 teaspoons ground cinnamon
- 1/2 cup butter, melted

### Glaze
- 1 cup confectioners' sugar
- 2 tablespoons milk

## Instructions
1. Combine milk, water, melted butter, sugar, and yeast. Add to flour and salt. Knead 5-7 min until smooth.
2. Rise until doubled (1-2 hours).
3. Butter a 12-cup bundt pan thoroughly.
4. Pat dough into ~8-9 inch square, cut into 64 pieces, roll into balls.
5. Dip balls in melted butter, then roll in cinnamon-brown sugar.
6. Place coated balls in bundt pan, staggering layers.
7. Second rise: cover and let rise until puffy (1-2 hours).
8. Bake at 350 F for 30-35 min until golden brown (internal temp 190-200 F).
9. Invert onto platter after no more than 5 minutes.
10. Drizzle with glaze while warm.

## Tips & Notes
- Let rise until very puffy before baking to avoid dense bread.
- Best served warm.
- Can refrigerate assembled bread for 12-18 hours before baking.
- Use 9x13 pan or two loaf pans if no bundt pan.
- Active dry yeast can be used instead of instant.
- Freeze after baking; lightly warm before serving.

## Nutrition (per serving)
- Calories: 500 kcal | Carbs: 90g | Protein: 8g | Fat: 13g
- Saturated Fat: 8g | Cholesterol: 32mg | Sodium: 709mg
""",

"white_chocolate_raspberry_truffle_cheesecake.md": """# White Chocolate Raspberry Truffle Cheesecake
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/white-chocolate-raspberry-truffle-cheesecake/)
**Cuisine:** american
**Type:** dessert
**Method:** baked
**Prep Time:** 4 hrs 45 mins
**Cook Time:** 55 minutes
**Total Time:** 5 hrs 40 mins
**Yield:** 12 slices

## Description
A decadent, egg-free cheesecake with white chocolate ganache, swirled with raspberry jam, and topped with fresh raspberries and white chocolate shavings. Silky, rich, and truffle-like.

## Ingredients

### Crust
- 10 oz chocolate crackers, finely crushed (~2 cups)
- 4 tbsp melted butter
- 1 egg yolk (optional)

### Cheesecake Filling
- 6 oz chopped real white chocolate (not chips)
- 1/4 cup heavy cream
- 3 x 8-oz packages cream cheese, softened
- 1 cup sour cream
- 1 cup granulated sugar
- 2 tbsp cornstarch
- 1 tsp vanilla extract
- 1/2 cup seedless raspberry jam

### Garnish
- Shaved or finely chopped white chocolate
- Fresh raspberries
- Additional raspberry jam or puree

## Instructions
1. Preheat oven to 350 F.
2. Mix crumbs, butter, and egg yolk. Press into springform pan. Bake 8-10 min. Cool.
3. Microwave white chocolate and cream in 30-sec intervals until smooth. Cool.
4. Beat cream cheese until smooth. Add sour cream, sugar, cornstarch, and vanilla. Fold in ganache.
5. Spread half the batter over crust. Dollop raspberry jam; swirl. Top with remaining batter.
6. Bake 40-45 min until edges are set, center slightly jiggly.
7. Cool completely. Refrigerate at least 4 hours (up to 24 hrs).
8. Garnish with white chocolate shavings, raspberries, and raspberry drizzle.

## Tips & Notes
- Use real white chocolate (Ghirardelli bars recommended), not chips or almond bark.
- Seedless jam is recommended for smooth texture.
- The raspberry jam layer helps prevent surface cracks.
- Refrigerator: up to 2-3 days. Freezer: recommended if not serving within 1-2 days.
- Let stand at room temperature 1-2 hours before serving for best texture.

## Nutrition (per slice)
- Calories: 371 kcal | Carbs: 55g | Sugar: 39g
- Protein: 4g | Fat: 16g (Saturated: 9g)
- Cholesterol: 44mg | Sodium: 231mg
""",
}

# Write all files
written = 0
skipped = 0
for filename, content in RECIPE_DATA.items():
    path = os.path.join(RECIPES_DIR, filename)
    # Check if already has content
    if os.path.exists(path) and os.path.getsize(path) > 500:
        print(f"SKIP (has content): {filename}")
        skipped += 1
        continue
    with open(path, 'w') as f:
        f.write(content)
    print(f"WRITTEN: {filename} ({len(content)} bytes)")
    written += 1

print(f"\nWritten: {written}, Skipped: {skipped}")
