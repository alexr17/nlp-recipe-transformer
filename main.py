from src.parse import parse_html, parse_ingredients, split_ingredients
from src.transform import to_vegetarian
import json
# import statements above here

def run():
    recipe = f'https://www.allrecipes.com/recipe/{6665}'
    to_vegetarian(recipe)
    #recipe_num = 260813 # any number greater than or equal to 6664
    # raw_recipe = parse_html(f'https://www.allrecipes.com/recipe/{6665}')
    # raw_recipe['ingredients'] = parse_ingredients(raw_recipe['ingredients'])
    # print(json.dumps(raw_recipe['ingredients'], indent=2))
    # print('-------------------------------------------------')
    # raw_recipe['ingredients'] = split_ingredients(raw_recipe['ingredients'])
    # print(json.dumps(raw_recipe['ingredients'], indent=2))
    return False

if __name__ == '__main__':
    run()
