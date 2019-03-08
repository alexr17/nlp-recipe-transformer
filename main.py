from src.parse import parse_html, format_recipe
from src.transform import to_vegetarian
from src.lib.debug import test_recipes, test_random_recipe
from src.cli import run_cli
from random import randint
import json
# import statements above here

def run():

    recipe_num = 25678
    recipe = f'https://www.allrecipes.com/recipe/{recipe_num}'
    raw_recipe = parse_html(recipe)
    parsed_recipe = format_recipe(raw_recipe)
    formatted_recipe = to_vegetarian(parsed_recipe)
    print('-------------- Converting to vegetarian: -------------------')
    #print(json.dumps(formatted_recipe, indent=2))
    return False


if __name__ == '__main__':
    run()
    # change this to be any of
    # test_recipes()
    # test_random_recipe()
    # run_cli()
