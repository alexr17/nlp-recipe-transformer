import json
import nltk
import copy
from os import listdir
from os.path import isfile, join
from src.transform_cuisine import transform_cuisine_ingredients, transform_cuisine_steps
# import statements above here

fruits_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/fruits.txt')])
herbs_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/herbs.txt')])
vegetables_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/vegetables.txt')])
condiments_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/condiments.txt')])
carbs_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/carbs.txt')])
binders_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/binders.txt')])
protein_json = json.load(open('./src/lib/categories/food_groups/protein.json'))
primary_protein_kw = set(protein_json['primary'].keys())
secondary_protein_kw = set(protein_json['secondary'].keys())

def to_vegetarian(recipe):
    '''
    Converts a recipe to a vegetarian version
    '''

    # Convert ingredients to vegetarian
    ingredients = recipe['ingredients']

    primary_protein = ingredients['primary_protein']
    secondary_protein = ingredients['secondary_protein']
    tertiary_protein = ingredients['tertiary_protein']

    primary_protein_dict = protein_json['primary']

    vegetarian_swap = json.load(open('./src/lib/transformations/vegetarian.json'))
    meat_descriptors = set([line.strip() for line in open('./src/lib/transformations/meat_descriptors.txt')])

    swapped_words = {}
    for protein in primary_protein:
        matched_word = protein['matched_word']

        if matched_word in primary_protein_dict:
            if primary_protein_dict[matched_word]['type'] in {"meat", "poultry", "fish", "shellfish", "soup"}:
                if matched_word in vegetarian_swap:
                    protein['ingredient'] = vegetarian_swap[matched_word]
                    swapped_words[matched_word] = vegetarian_swap[matched_word]
        new_raw_ingredient = []
        raw_ingredient = protein['raw_ingredient'].split(" ")
        for x in protein['raw_ingredient'].split(" "):
            print(x)
            if x in swapped_words:
                new_raw_ingredient.append(swapped_words[x])
            elif x in meat_descriptors:
                print(x)
                new_raw_ingredient.append("")
            else:
                new_raw_ingredient.append(x)

        protein['raw_ingredient'] = " ".join(new_raw_ingredient)

    # Convert directions to vegetarian
    for step in recipe['steps']:
        step_ingredients = step['ingredients']
        step['ingredients'] = [swapped_words[x]
                               if x in swapped_words else x for x in step_ingredients]

        raw_step = step['raw_step']
        splitted_step = nltk.word_tokenize(raw_step)
        splitted_step = [swapped_words[x]
                         if x in swapped_words else x for x in splitted_step]
        step['raw_step'] = " ".join(splitted_step)

    return recipe


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
    path = './src/lib/transformations/cuisines/'
    cuisine_files = [f for f in listdir(path) if isfile(join(path, f))]
    cuisine_file = False
    for f in cuisine_files:
        if f.replace('.json', '') == cuisine.lower():
            cuisine_file = f
            break
    if not cuisine_file:
        print("There is no transformation for the cuisine you provided")
        return False

    # need to make a deep copy of the recipe
    recipe = copy.deepcopy(recipe)
    cuisine = json.load(open(path + cuisine_file))

    transform_cuisine_ingredients(recipe, cuisine)
    transform_cuisine_steps(recipe, cuisine)
    return recipe