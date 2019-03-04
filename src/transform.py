from src.parse import parse_html, parse_ingredients, split_ingredients
import json
### import statements above here

def format_recipe(recipe):
    raw_recipe = parse_html(recipe)
    raw_recipe['ingredients'] = parse_ingredients(raw_recipe['ingredients'])
    raw_recipe['ingredients'] = split_ingredients(raw_recipe['ingredients'])
    return raw_recipe

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
    recipe = format_recipe(recipe)

    # Convert ingredients to vegetarian
    ingredients = recipe['ingredients']

    primary_protein = ingredients['primary_protein']
    secondary_protein = ingredients['secondary_protein']

    primary_protein_dict = protein_json['primary']

    vegetarian_swap = json.load(open('./src/lib/transformations/vegetarian.json'))

    for protein in primary_protein:
        matched_word = protein['matched_word']


        if matched_word in primary_protein_dict:
            if primary_protein_dict[matched_word] == "meat":
                if matched_word in vegetarian_swap:
                    protein['ingredient'] = vegetarian_swap[matched_word]

    #print(json.dumps(recipe, indent=2))







    # Convert directions to vegetarian

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
