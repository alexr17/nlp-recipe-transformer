import fileinput
import json
from random import randint
from fractions import Fraction
from src.parse import parse_html, format_recipe
from src.lib.debug import test_random_recipe
from src.transform import to_cuisine, to_healthy, to_non_healthy, to_non_vegetarian, to_vegetarian


def print_cli_information():
    '''
    Prints the CLI info (what keys to press)
    '''
    info = """
Welcome to Alex and Itay's recipe transformer!
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
    """
    print(info)


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
                print(json.dumps(recipe, indent=2))
            elif line[2] in {'--readable', '-r'}:
                pretty_print(recipe)
        else:
            print("You need a valid recipe")

def pretty_print(recipe):
    print("\nTitle: " + recipe['title'].title())
    ingredients = []
    for food_type in recipe['ingredients']:
        for ing in recipe['ingredients'][food_type]:
            s = '\n' + (str(Fraction(ing['quantity'])) + ' ' if ing['quantity'] else '') + (ing['measurement'] + ' ' if ing['measurement'] else '') + ing['ingredient'].title()
            if len(ing['descriptors']):
                s += "\nWith additional descriptors: " + ' '.join(ing['descriptors'])
            ingredients.append(s)
    print("\nThe ingredients that will be used are as follows:\n" + '\n'.join(ingredients))

    steps = []
    for step in recipe['steps']:
        steps.append('\n' + step['raw_step'])
    
    print("\nThe steps that will be used are as follows (this does not work for transformations):\n" + '\n'.join(steps))

def cli_transform(line, parsed_recipe):
    if not parsed_recipe:
        print("You need to load a recipe before you transform it.")
    elif len(line) < 2:
        print("You need to pass more arguments")
    elif line[1] in {'--cuisine', '-c'} and len(line) > 2:
        if line[2] in {'--mediterranean', '-m'}:
            print("Mediterranean transformation not implemented yet")
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
    else:
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
