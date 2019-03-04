from src.parse import parse_html, parse_ingredients, split_ingredients
from src.parse_steps import parse_tools, parse_methods
from src.transform import to_vegetarian
import json
# import statements above here

def run():
    #recipe = f'https://www.allrecipes.com/recipe/{26425}'
    #to_vegetarian(recipe)
    recipe_num = 6665 # any number greater than or equal to 6664
    raw_recipe = parse_html(f'https://www.allrecipes.com/recipe/{recipe_num}')
    raw_recipe['ingredients'] = parse_ingredients(raw_recipe['ingredients'])
    raw_recipe['ingredients'] = split_ingredients(raw_recipe['ingredients'])
    raw_recipe['tools'] = parse_tools(raw_recipe['steps'])
    raw_recipe['methods'] = parse_methods(raw_recipe['steps'])
    print(json.dumps(raw_recipe, indent=2))
    return False

if __name__ == '__main__':
    run()
