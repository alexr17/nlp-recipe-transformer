from src.parse import parse_html, parse_ingredients, split_ingredients
import json
### import statements above here



def format_recipe(recipe):
    raw_recipe = parse_html(recipe)
    raw_recipe['ingredients'] = parse_ingredients(raw_recipe['ingredients'])
    raw_recipe['ingredients'] = split_ingredients(raw_recipe['ingredients'])
    return raw_recipe


def to_vegetarian(recipe):
    recipe = format_recipe(recipe)



    print(json.dumps(recipe, indent=2))

def from_vegetarian(recipe):
    return False

def to_healthy(recipe):
    return False

def from_healthy(recipe):
    return False

def to_cuisine(recipe, cuisine):
    return False

def from_cuisine(recipe, cuisine):
    return False
