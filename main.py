from src.parse import parse_html, parse_ingredients, categorize_ingredient
import json
# import statements above here

def run():
    # recipe_num = 260813 # any number greater than or equal to 6664
    for recipe_num in range(6665, 6670):
        raw_recipe = parse_html(f'https://www.allrecipes.com/recipe/{str(recipe_num)}')
        if raw_recipe:
            raw_recipe['ingredients'] = parse_ingredients(raw_recipe['ingredients'])
            # print(json.dumps(raw_recipe, indent=4))
            for ingredient_obj in raw_recipe['ingredients']:
                ingredient_type = categorize_ingredient(ingredient_obj['ingredient'])
                if ingredient_type:
                    print(f"Found ingredient type {ingredient_type} for ingredient: {ingredient_obj['ingredient']}")
    # parsed_ingredients = parse_ingredients(raw_recipe['ingredients'])
    return False

if __name__ == '__main__':
    run()
