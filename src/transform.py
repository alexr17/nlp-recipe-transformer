from src.parse import parse_html, parse_ingredients, split_ingredients
from src.parse_steps import parse_tools, parse_methods, split_steps
import json
import nltk
### import statements above here

fruits_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/fruits.txt')])
herbs_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/herbs.txt')])
vegetables_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/vegetables.txt')])
condiments_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/condiments.txt')])
carbs_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/carbs.txt')])
binders_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/binders.txt')])
protein_json = json.load(open('./src/lib/categories/food_groups/protein.json'))
primary_protein_kw = set(protein_json['primary'].keys())
secondary_protein_kw = set(protein_json['secondary'].keys())

def format_recipe(recipe):
    '''
    Takes a recipe url and runs the parsing methods, returning a parsed recipe
    '''
    raw_recipe = parse_html(recipe)
    raw_recipe['ingredients'] = parse_ingredients(raw_recipe['ingredients'])

    ingredients = [ingredient['ingredient'] for ingredient in raw_recipe['ingredients']]
    raw_recipe['ingredients'] = split_ingredients(raw_recipe['ingredients'])

    tools = parse_tools(raw_recipe['steps'])
    raw_recipe['tools'] = tools

    methods = parse_methods(raw_recipe['steps'])
    raw_recipe['methods'] = methods

    steps = split_steps(raw_recipe['steps'], ingredients, tools, methods)
    raw_recipe['steps'] = steps

    return raw_recipe

def to_vegetarian(recipe):
    recipe = format_recipe(recipe)

    # Convert ingredients to vegetarian
    ingredients = recipe['ingredients']

    primary_protein = ingredients['primary_protein']
    secondary_protein = ingredients['secondary_protein']

    primary_protein_dict = protein_json['primary']

    vegetarian_swap = json.load(open('./src/lib/transformations/vegetarian.json'))

    swapped_words = {}
    for protein in primary_protein:
        matched_word = protein['matched_word']


        if matched_word in primary_protein_dict:
            if primary_protein_dict[matched_word] == "meat":
                if matched_word in vegetarian_swap:
                    protein['ingredient'] = vegetarian_swap[matched_word]
                    swapped_words[matched_word] = vegetarian_swap[matched_word]

    # Convert directions to vegetarian
    for step in recipe['steps']:
        step_ingredients = step['ingredients']
        step['ingredients'] = [swapped_words[x] if x in swapped_words else x for x in step_ingredients]

        raw_step = step['raw_step']
        splitted_step = nltk.word_tokenize(raw_step)
        splitted_step = [swapped_words[x] if x in swapped_words else x for x in splitted_step]
        step['raw_step'] = " ".join(splitted_step)



    print(json.dumps(recipe, indent=2))

def to_non_vegetarian(recipe, meat_type='random'):
    '''
    Converts a parsed vegetarian recipe to one with meat
    '''
    return False

def to_healthy(recipe):
    '''
    Converts a parsed recipe to a healthier version
    '''
    return False

def to_non_healthy(recipe):
    '''
    Converts a recipe into a unhealthy version
    '''
    return False

def to_cuisine(recipe, cuisine):
    '''
    Converts a parsed recipe to a given cuisine
    '''
    recipe = format_recipe(recipe)
    return False