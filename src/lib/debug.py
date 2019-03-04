from random import randint
import fileinput
import json
from src.parse import parse_html, parse_ingredients, split_ingredients


def test_recipes():
    min_recipe = 6664
    
    print("Now testing the recipe parser. [stop, exit, s, e] to exit.\nPress [enter] to parse a new recipe.\n[again, same, a] to parse same recipe")
    for line in fileinput.input():
        line = line.rstrip()
        raw_recipe = False
        if line.lower() in ['stop', 'exit', 's', 'e']:
            print("Exiting...")
            break
        elif line.lower() in ['again', 'a', 'same'] and raw_recipe:
            print("Parsing same recipe...")
        recipe = f'https://www.allrecipes.com/recipe/{str(min_recipe + randint(0, 250000))}'
        while not raw_recipe or raw_recipe['title'] in {'johnsonville® three cheese italian style chicken sausage skillet pizza'}:
            recipe = f'https://www.allrecipes.com/recipe/{str(min_recipe + randint(0, 250000))}'
            raw_recipe = parse_html(recipe)
        print(f"Now parsing recipe: {recipe}")
        raw_recipe['ingredients'] = parse_ingredients(raw_recipe['ingredients'])
        raw_recipe['ingredients'] = split_ingredients(raw_recipe['ingredients'])
        print(json.dumps(raw_recipe, indent=2))

        