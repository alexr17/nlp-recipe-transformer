from src.parse import parse_html, format_recipe
from src.transform import to_vegetarian
from src.lib.debug import test_recipes, test_random_recipe
from random import randint
import json
# import statements above here

def run():

    recipe_num = 25678
    recipe = f'https://www.allrecipes.com/recipe/{recipe_num}'
    print('-------------- Converting to vegetarian: -------------------')
    parsed_recipe = format_recipe(recipe)
    formatted_recipe = to_vegetarian(parsed_recipe)
    print(json.dumps(formatted_recipe, indent=2))
    return False


if __name__ == '__main__':
    run()
    # change this to be any of
    # test_recipes()
    # test_random_recipe()
