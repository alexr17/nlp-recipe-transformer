from src.parse import parse_html, format_recipe
from src.transform import to_vegetarian, to_non_vegetarian, to_cuisine, to_healthy, to_non_healthy, to_kosher, to_halal, to_non_halal
from src.lib.debug import test_recipes, test_random_recipe
from src.cli import run_cli
from random import randint
import json
# import statements above here

def run():

    recipe_num = 229119
    recipe = f'https://www.allrecipes.com/recipe/{recipe_num}'
    raw_recipe = parse_html(recipe)
    if not raw_recipe:
        print("Invalid recipe")
        return False
    parsed_recipe = format_recipe(raw_recipe)
    formatted_recipe = to_vegetarian(parsed_recipe)
    # formatted_recipe = to_cuisine(parsed_recipe, 'japanese')
    #print('-------------- Converting to vegetarian: -------------------')
    #formatted_recipe = to_non_healthy(parsed_recipe)
    # print('-------------- Converting to healthy: -------------------')

    formatted_recipe = to_kosher(parsed_recipe)
    print('-------------- Converting to Kosher: -------------------')
    print(json.dumps(formatted_recipe, indent=2))

    formatted_recipe = to_halal(parsed_recipe)
    print('-------------- Converting to Halal: -------------------')
    print(json.dumps(formatted_recipe, indent=2))

    formatted_recipe = to_non_halal(parsed_recipe)
    print('-------------- Converting to Haram (Non-Halal): -------------------')
    print(json.dumps(formatted_recipe, indent=2))
    
    
    return False


if __name__ == '__main__':
     run()
    #run_cli()
    # change this to be any of
    # test_recipes()
    # test_random_recipe()
