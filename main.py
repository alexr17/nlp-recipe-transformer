from src.parse import parse_html, parse_ingredients
import json
# import statements above here

def run():
    recipe_num = 26425 # any number greater than or equal to 6664
    raw_recipe = parse_html(f'https://www.allrecipes.com/recipe/{str(recipe_num)}')
    print(json.dumps(raw_recipe, indent=4))
    # parsed_ingredients = parse_ingredients(raw_recipe['ingredients'])
    return False

if __name__ == '__main__':
    run()
