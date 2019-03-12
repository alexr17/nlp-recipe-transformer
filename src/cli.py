import fileinput
import json
import copy
from random import randint
from fractions import Fraction
from src.parse import parse_html, format_recipe
from src.lib.debug import test_random_recipe
from src.transform import to_cuisine, to_healthy, to_non_healthy, to_non_vegetarian, to_vegetarian, cooking_method

debug = False

def print_cli_information():
    '''
    Prints the CLI info (what keys to press)
    '''
    info = """
Welcome to Alex, Itay, and Tony's recipe transformer!
The general outline of this CLI is as follows:
There are several options for you:
    load (l) - load a recipe into our program
        [--random | -r]
        [--url | -u] [<allrecipes-url>]
        [--num | -n] [<recipe-#>]
    transform (t) - transform a recipe
        [--veg | -v]
        [--meat | -m]
        [--healthy | -h]
        [--unhealthy | -u]
        [--cuisine | -c]
            [--mediterranean | -m] 
            [--japanese | -j]
        [--cooking-methods | -cm]
            [-f | -s | -g | -b]
                [-f | -s | -g | -b]
            [--fry | --steam | --bake | --grill]
                [--fry | --steam | --bake | --grill]
    print (p) - display the recipe
        [--parsed | -p]
            [--json | -j]
            [--readable | -r]
        [--transformed | -t]
            [--json | -j]
            [--readable | -r]
    help (h) - print out this message
    quit (q) - quit
Here are a few examples:
    l -r (loads a random recipe)
    p -p -j (prints the loaded recipe in json format)
    p -p -r (prints the loaded recipe in readable format)
    t -v (transforms the loaded recipe to vegetarian)
    p -t -r (prints the transformed recipe (now veg) in readable format)
    t -c -j (transforms the loaded recipe to japanese)
    p -t -r (prints the transformed recipe (now japanese) in readable format)
    t -cm -b -f (transforms the loaded recipe from baked to fried)
    p -t -r (prints the transformed recipe from baked to fried in readable format)
    """
    print(info)

cooking_method_map = {
    "f": "fry",
    "b": "bake",
    "g": "grill",
    "s": "steam"
}

def run_cli():
    '''
    Main program to be called by main.py
    '''
    print_cli_information()
    parsed_recipe = False
    transformed_recipe = False
    for line in fileinput.input():
        line = line.rstrip().lower().split(' ')
        if line[0] in {'l', 'load'}:
            parsed_recipe = cli_load(line)
        elif line[0] in {'t', 'transform'}:
            transformed_recipe = cli_transform(line, parsed_recipe)
        elif line[0] in {'p', 'print'}:
            cli_print(line, parsed_recipe, transformed_recipe)
        elif line[0] in {'h', 'help'}:
            print_cli_information()
        elif line[0] in {'q', 'quit'}:
            return False
        else:
            print('You passed an invalid argument. It should be any of [l | t | h | q].')
        print()


def cli_print(line, parsed_recipe, transformed_recipe):
    if len(line) < 3:
        print("You need to pass more arguments")
    else:
        recipe = False
        if line[1] in {'--parsed', '-p'}:
            recipe = parsed_recipe
        elif line[1] in {'--transformed', '-t'}:
            recipe = transformed_recipe
        
        if recipe:
            if line[2] in {'--json', '-j'}:
                print(json.dumps(clean_recipe(copy.deepcopy(recipe)), indent=2))
            elif line[2] in {'--readable', '-r'}:
                pretty_print(recipe)
            else:
                print("You need to pass a valid option")
        else:
            print("You need a valid recipe")

def clean_recipe(recipe):
    if not debug:
        for food_type in recipe['ingredients']:
            for ing in recipe['ingredients'][food_type]:
                del ing['raw_ingredient']
                del ing['matched_word']
        del recipe['recipe_categories']
    return recipe

def pretty_print(recipe):
    print("\nTitle: " + recipe['title'].title())
    ingredients = []
    for food_type in recipe['ingredients']:
        for ing in recipe['ingredients'][food_type]:
            ingredients.append(format_ingredient(ing))
    print("\n-------------------- Ingredients --------------------\n" + '\n'.join(ingredients))

    steps = []
    for step in recipe['steps']:
        steps.append('\n' + step['raw_step'])
    
    print("\n------------------------ Steps ------------------------\n" + '\n'.join(steps))

    print("\n--------------- Primary Cooking Methods ---------------\n\n" + '\n'.join(recipe['methods']['primary_methods']))

    print("\n------------------------ Tools ------------------------\n\n" + '\n'.join(recipe['tools']))

def format_ingredient(ing):
    s = '\n' + (str(Fraction(ing['quantity']).limit_denominator()) + ' ' if ing['quantity'] else '') + (ing['measurement'] + ' ' if ing['measurement'] else '')
    adv = ''
    size = ''
    front = []
    back = []
    for desc in ing['descriptors']:
        # adverb
        if desc[-2:] == 'ly' or desc in {'very'}:
            adv = desc + ' '
        # size
        elif desc in {'small', 'medium', 'large', 'lean', 'big'}:
            size = desc
        # back descriptor
        elif desc[-2:] in {'ed', 'en'} or desc in {'juice'}:
            back.append(adv + desc)
            adv = ''
        # front descriptor
        else:
            front.append(adv + desc)
            adv = ''
    s += ' '.join(front) + (' ' + size if size else '') + (' ' if len(front) or size else '') + ing['ingredient'].title() + ' ' + ', '.join(back)
    return s

def cli_transform(line, parsed_recipe):
    if not parsed_recipe:
        print("You need to load a recipe before you transform it.")
    elif len(line) < 2:
        print("You need to pass more arguments")
    elif line[1] in {'--cuisine', '-c'} and len(line) > 2:
        if line[2] in {'--mediterranean', '-m'}:
            print("Recipe transformed to Mediterranean")
            return to_cuisine(parsed_recipe, 'mediterranean')
        elif line[2] in {'--japanese', '-j'}:
            print("Recipe transformed to Japanese")
            return to_cuisine(parsed_recipe, 'japanese')
    elif line[1] in {'--veg', '-v'}:
        print("Recipe transformed to vegetarian")
        return to_vegetarian(parsed_recipe)
    elif line[1] in {'--meat', '-m'}:
        print("Recipe transformed to non vegetarian")
        return to_non_vegetarian(parsed_recipe)
    elif line[1] in {'--healthy', '-h'}:
        print("Recipe transformed to healthy")
        return to_healthy(parsed_recipe)
    elif line[1] in {'--unhealthy', '-u'}:
        print("Recipe transformed to unhealthy")
        return to_non_healthy(parsed_recipe)
    elif line[1] in {'--cooking-methods', '-cm'} and len(line) > 3:
        method1 = line[2].replace('-', '')
        method2 = line[3].replace('-', '')
        if method1 in cooking_method_map:
            method1 = cooking_method_map[method1]
        if method2 in cooking_method_map:
            method2 = cooking_method_map[method2]
        if method1 in cooking_method_map.values() and method2 in cooking_method_map.values() and method1 != method2:
            print(f"Recipe transformed from {method1} to {method2}")
            return cooking_method(parsed_recipe, method1, method2)
        else:
            print("Invalid cooking methods")
            return False
    else:
        print("Invalid transformation try again")
        return False

def cli_load(line):
    if len(line) < 2:
        print("You need to pass more arguments")
    elif line[1] in {'--random', '-r'}:
        return test_random_recipe(False)
    elif len(line) < 3:
        print("You need to pass more arguments")
    else:
        if line[1] in {'--url', '-u'}:
            raw_recipe = parse_html(line[2])
            if raw_recipe:
                print("Recipe loaded")
                return format_recipe(raw_recipe)
            else:
                print("You passed an invalid recipe url")
        elif line[1] in {'--num', '-n'}:
            raw_recipe = parse_html(f'https://www.allrecipes.com/recipe/{line[2]}')
            if raw_recipe:
                print("Recipe loaded")
                return format_recipe(raw_recipe)
            else:
                print("You passed an invalid recipe #")
        else:
            print("You passed an invalid second argument to load")
    return False
