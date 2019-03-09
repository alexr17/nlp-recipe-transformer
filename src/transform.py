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

def to_vegetarian(recipe):
    '''
    Converts a recipe to a vegetarian version
    '''

    # Convert ingredients to vegetarian
    ingredients = recipe['ingredients']

    primary_protein = ingredients['primary_protein']
    secondary_protein = ingredients['secondary_protein']
    proteins = primary_protein + secondary_protein

    primary_protein_dict = protein_json['primary']
    secondary_protein_dict = protein_json['secondary']
    protein_dict = {**primary_protein_dict, **secondary_protein_dict}

    vegetarian_swap = json.load(open('./src/lib/transformations/to_vegetarian.json'))
    meat_descriptors = set([line.strip() for line in open('./src/lib/transformations/meat_descriptors.txt')])
    swapped_words = {}

    for protein in proteins:
        matched_word = protein['matched_word']
        if matched_word in protein_dict:
            if protein_dict[matched_word]['type'] in {'meat', 'poultry', 'fish', 'shellfish', 'soup'}:
                    protein['ingredient'] = vegetarian_swap[protein_dict[matched_word]['category']]
                    swapped_words[matched_word] = vegetarian_swap[protein_dict[matched_word]['category']]

        # remove meat_descriptors
        new_descriptors = []
        for descriptor in protein['descriptors']:
            if descriptor not in meat_descriptors:
                new_descriptors.append(descriptor)

        protein['descriptors'] = new_descriptors

    for step in recipe['steps']:
        new_step_ingredients = []
        for ingredient in step['ingredients']:
            if ingredient in swapped_words:
                new_step_ingredients.append(swapped_words[ingredient])
            else:
                new_step_ingredients.append(ingredient)
        step['ingredients'] = new_step_ingredients



        #new_raw_ingredient = []
        #raw_ingredient = protein['raw_ingredient'].split(" ")
        # for x in protein['raw_ingredient'].split(" "):
        #     if x in swapped_words:
        #         new_raw_ingredient.append(swapped_words[x])
        #     elif x in meat_descriptors:
        #         new_raw_ingredient.append("")
        #     else:
        #         new_raw_ingredient.append(x)

        #protein['raw_ingredient'] = " ".join(new_raw_ingredient)

    # Convert directions to vegetarian

        #step['ingredients'] = [swapped_words[x] if x in swapped_words else x for x in step_ingredients]
        # raw_step = step['raw_step']
        # splitted_step = nltk.word_tokenize(raw_step)
        # splitted_step = [swapped_words[x] if x in swapped_words else x for x in splitted_step]
        # step['raw_step'] = " ".join(splitted_step)

    return recipe

def to_non_vegetarian(recipe):
    '''
    Converts a parsed vegetarian recipe to one with meat
    '''
    ingredients = recipe['ingredients']

    primary_protein = ingredients['primary_protein']
    secondary_protein = ingredients['secondary_protein']
    proteins = primary_protein + secondary_protein

    primary_protein_dict = protein_json['primary']
    secondary_protein_dict = protein_json['secondary']
    protein_dict = {**primary_protein_dict, **secondary_protein_dict}

    non_vegetarian_swap = json.load(open('./src/lib/transformations/to_non_vegetarian.json'))
    meat_descriptors = set([line.strip() for line in open('./src/lib/transformations/meat_descriptors.txt')])
    swapped_words = {}

    flag = False
    for protein in proteins:
        matched_word = protein['matched_word']
        if matched_word in protein_dict:
            if protein_dict[matched_word]['category'] in {'bean', 'nuts', 'soy','soup'}:
                    flag = True
                    protein['ingredient'] = non_vegetarian_swap[protein_dict[matched_word]['category']]
                    swapped_words[matched_word] = non_vegetarian_swap[protein_dict[matched_word]['category']]

        # remove meat_descriptors
        # new_descriptors = []
        # for descriptor in protein['descriptors']:
        #     if descriptor not in meat_descriptors:
        #         new_descriptors.append(descriptor)

        # protein['descriptors'] = new_descriptors

    for step in recipe['steps']:
        new_step_ingredients = []
        for ingredient in step['ingredients']:
            if ingredient in swapped_words:
                new_step_ingredients.append(swapped_words[ingredient])
            else:
                new_step_ingredients.append(ingredient)
        step['ingredients'] = new_step_ingredients


    # Add chicken breast if no change in protein
    if not flag:
        recipe['ingredients']['primary_protein'].append({
            "quantity": 2,
            "measurement": "strips",
            "ingredient": "chicken breast",
            "descriptors": ["boneless"],
            "raw_ingredient": "2 strips of boneless chicken breast",
            "matched_word": "chicken breast"

        })
        if not any(i['ingredient'] == "cooking spray" for i in recipe['ingredients']['binder']):
            recipe['ingredients']['binder'].append({
                "quantity": "",
                "measurement": "",
                "ingredient": "cooking spray",
                "descriptors": "",
                "matched_word": "cooking spray"

            })
        recipe['steps'].append({
            "ingredients": ["chicken breast", "cooking spray"],
            "tools": ["pan"],
            "methods": ["grilled", "slice"],
            "times": ["7 minutes"],
            "temperature": ["165 degrees"],

        })
    return recipe

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
    return False
