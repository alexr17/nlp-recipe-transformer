from random import randint
import fileinput
import json
from src.parse import parse_html, format_recipe

def test_random_recipe():
    min_recipe = 6664
    raw_recipe = False
    recipe = f'https://www.allrecipes.com/recipe/{str(min_recipe + randint(0, 250000))}'
    while not raw_recipe or raw_recipe['title'] in {'johnsonville® three cheese italian style chicken sausage skillet pizza'}:
        recipe = f'https://www.allrecipes.com/recipe/{str(min_recipe + randint(0, 250000))}'
        raw_recipe = parse_html(recipe)
    print(f"Now parsing recipe: {recipe}")
    parsed_recipe = format_recipe(recipe)
    print(json.dumps(parsed_recipe, indent=2))
    return parsed_recipe

def test_recipes():    
    print("Now randomly testing the recipe parser. [stop, exit, s, e] to exit.\nPress [enter] to parse a new recipe.\n[again, same, a] to parse same recipe")
    for line in fileinput.input():
        line = line.rstrip()
        if line.lower() in ['stop', 'exit', 's', 'e']:
            print("Exiting...")
            break
        test_random_recipe()