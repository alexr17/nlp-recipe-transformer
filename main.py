from src.parse import parse_html, parse_ingredients, split_ingredients
from src.parse_steps import parse_tools, parse_methods, split_steps
from src.transform import to_vegetarian
from src.lib.debug import test_recipes
import json
# import statements above here

def run():
    recipe_num = 6665 # any number greater than or equal to 6664
    raw_recipe = parse_html(f'https://www.allrecipes.com/recipe/{recipe_num}')

    raw_recipe['ingredients'] = parse_ingredients(raw_recipe['ingredients'])
    ingredients = [ingredient['ingredient'] for ingredient in raw_recipe['ingredients']]
    raw_recipe['ingredients'] = split_ingredients(raw_recipe['ingredients'])

    tools = parse_tools(raw_recipe['steps'])
    raw_recipe['tools'] = tools

    methods = parse_methods(raw_recipe['steps'])
    raw_recipe['methods'] = methods

    steps = split_steps(raw_recipe['steps'], ingredients, tools, methods)
    raw_recipe['steps'] = steps
    print(json.dumps(raw_recipe, indent=2))
    return False

def debug():
    '''
    Run this to test the recipes
    '''
    test_recipes()

if __name__ == '__main__':
    run()
