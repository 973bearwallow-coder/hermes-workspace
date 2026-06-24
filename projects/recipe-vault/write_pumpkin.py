import os

VAULT = os.path.expanduser('~/hermes-workspace/projects/recipe-vault')

# Write Amazing Crustless Pumpkin Pie Cupcakes
content = """# Amazing Crustless Pumpkin Pie Cupcakes
**Source:** [Mel's Kitchen Cafe](https://www.melskitchencafe.com/amazing-crustless-pumpkin-pie-cupcakes/)
**Cuisine:** american
**Type:** dessert
**Method:** baked
**Prep Time:** 1 hr 20 mins
**Cook Time:** 20 minutes
**Total Time:** 1 hr 40 mins
**Yield:** 12 cupcakes

## Description
Crustless pumpkin pie cupcakes that are creamy, rich, and silky - a hybrid between pumpkin pie and cupcakes. All the flavor of traditional pumpkin pie without the crust.

## Ingredients

### Cupcake Batter
- 1 (15 oz) can pumpkin puree
- 1/2 cup granulated sugar
- 1/4 cup lightly packed brown sugar
- 2 large eggs + 1 egg yolk
- 1 tsp vanilla extract
- 1/2 cup heavy whipping cream
- 1/4 cup milk (1% or higher)
- 2/3 cup all-purpose flour
- 2 tsp pumpkin pie spice
- 1/4 tsp salt
- 1/4 tsp baking soda
- 1/4 tsp baking powder

### Sweetened Whipped Cream
- 1 1/2 cups heavy whipping cream
- 2-3 tbsp powdered sugar
- 1 tbsp sour cream (optional)
- 1/4 tsp vanilla extract

## Instructions
1. Preheat oven to 350 F. Line a 12-cup muffin tin with paper liners; lightly grease liners.
2. Whisk pumpkin, sugars, eggs, yolk, vanilla, cream, and milk until smooth.
3. Mix flour, pumpkin pie spice, salt, baking soda, and baking powder.
4. Combine wet and dry; whisk gently until just blended.
5. Divide evenly into muffin cups. Bake 20 minutes.
6. Cool in pan 20-30 mins (they will fall slightly - this is normal).
7. Refrigerate at least 1 hour before serving.
8. Whip cream ingredients until thick. Dollop on each cupcake.

## Tips & Notes
- Expect a custard-like, not cakey, texture.
- They sink after cooling - this is normal.
- Use 3/4 cup half-and-half instead of cream + milk if preferred.
- Can be made 1-2 days ahead. Freezes well for several weeks.
- Gluten-free flour works as 1:1 substitute.

## Nutrition (per cupcake)
- Calories: 251 kcal | Carbs: 24g | Protein: 3g | Fat: 16g
- Saturated Fat: 10g | Cholesterol: 99mg | Sodium: 113mg
"""

path = os.path.join(VAULT, 'recipes', 'amazing_crustless_pumpkin_pie_cupcakes.md')
with open(path, 'w') as f:
    f.write(content)
print(f"Written: {path} ({len(content)} bytes)")
