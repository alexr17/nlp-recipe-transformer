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
    recipe = copy.deepcopy(recipe)

    # Convert ingredients to vegetarian
    ingredients = recipe['ingredients']

    primary_protein = ingredients['primary_protein']
    secondary_protein = ingredients['secondary_protein']
    proteins = primary_protein + secondary_protein
    tertiary_protein = ingredients['tertiary_protein']

    primary_protein_dict = protein_json['primary']
    secondary_protein_dict = protein_json['secondary']
    protein_dict = {**primary_protein_dict, **secondary_protein_dict}

    vegetarian_swap = json.load(open('./src/lib/transformations/to_vegetarian.json'))
    meat_descriptors = set([line.strip() for line in open('./src/lib/transformations/meat_descriptors.txt')])
    swapped_words = {'meat': 'vegetarian concoction'}

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


    # Transform steps
    for step in recipe['steps']:
        new_step_ingredients = []
        for ingredient in step['ingredients']:
            if ingredient in swapped_words:
                new_step_ingredients.append(swapped_words[ingredient])
            else:
                new_step_ingredients.append(ingredient)
        step['ingredients'] = new_step_ingredients
        for ing in swapped_words:
            if ing in step['raw_step']:
                step['raw_step'] = step['raw_step'].replace(ing, swapped_words[ing])
            if ing in meat_descriptors:
                step['raw_step'] = step['raw_step'].replace(ing, "")
        step['raw_step'] = " ".join(step['raw_step'].split())


    # Transform title
    for ing in swapped_words:
        if ing in recipe['title']:
            recipe['title'] = recipe['title'].replace(ing, swapped_words[ing])

    return recipe

def to_non_vegetarian(recipe):
    '''
    Converts a parsed vegetarian recipe to one with meat
    '''
    recipe = copy.deepcopy(recipe)


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

    # Transform steps
    for step in recipe['steps']:
        new_step_ingredients = []
        for ingredient in step['ingredients']:
            if ingredient in swapped_words:
                new_step_ingredients.append(swapped_words[ingredient])
            else:
                new_step_ingredients.append(ingredient)
        step['ingredients'] = new_step_ingredients
        for ing in swapped_words:
            if ing in step['raw_step']:
                step['raw_step'] = step['raw_step'].replace(ing, swapped_words[ing])

    # Transform title
    for ing in swapped_words:
        if ing in recipe['title']:
            recipe['title'] = recipe['title'].replace(ing, swapped_words[ing])

    if not flag:
        recipe['title'] = 'chicken ' + recipe['title']


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
            "raw_step": "spray cooking spray on pan. grill chicken at 165 degrees for 7 minutes (or until golden). slice chicken when done."

        })
    return recipe


def to_healthy(recipe):
    '''
    Converts a parsed recipe to a healthier version
    '''
    to_healthy_swap = json.load(open('./src/lib/transformations/healthy.json'))
    swapped_words_to_healthy = {}
    #swapping ingredients
    ingredient = recipe['ingredients']

    binder = ingredient['binder']
    carb = ingredient['carb']
    condiment = ingredient['condiment']
    for ing in binder:
        matched_word_to_healthy = ing['matched_word']
        if matched_word_to_healthy in to_healthy_swap:
            if ing['ingredient']=='butter':
                ing['ingredient']=to_healthy_swap[matched_word_to_healthy]
                ing['quantity']=ing['quantity']*(.75)
                swapped_words_to_healthy[matched_word_to_healthy]=to_healthy_swap[matched_word_to_healthy]
            else:
                ing['ingredient']=to_healthy_swap[matched_word_to_healthy]
                swapped_words_to_healthy[matched_word_to_healthy]=to_healthy_swap[matched_word_to_healthy]
    for ing in carb:
        matched_word_to_healthy = ing['matched_word']
        if matched_word_to_healthy in to_healthy_swap:
            ing['ingredient']=to_healthy_swap[matched_word_to_healthy]
            swapped_words_to_healthy[matched_word_to_healthy]=to_healthy_swap[matched_word_to_healthy]
    for ing in condiment:
        matched_word_to_healthy = ing['matched_word']
        if matched_word_to_healthy in to_healthy_swap:
            ing['ingredient']=to_healthy_swap[matched_word_to_healthy]
            swapped_words_to_healthy[matched_word_to_healthy]=to_healthy_swap[matched_word_to_healthy]
    #changing diretions
    for step in recipe['steps']:
        #replace frying with baking
        if "fry" in step['methods']:
            fry_time = step['times']
            #baking takes 4 times as long as frying
            fry_time_array = fry_time[0].split(" ")
            #print(fry_time_array)
            orig_time=fry_time_array[0]
            fry_time_array[0] = str(eval(fry_time_array[0])*4)
            step['times'][0]=" ".join(fry_time_array)
            swapped_words_to_healthy[orig_time]=fry_time_array[0]
            if "fry" in recipe['methods']['primary_methods']:
                for i in range(len(recipe['methods']['primary_methods'])):
                    if recipe['methods']['primary_methods'][i] == "fry":
                        print(recipe['methods']['primary_methods'][i])
                        recipe['methods']['primary_methods'][i]="bake"
                        print(recipe['methods']['primary_methods'][i])
            for i in range(len(step['methods'])):
                if step['methods'][i] == "fry":
                    #print("swap")
                    #print(step['methods'])
                    step['methods'][i] = "bake"
                    #print(method)
                    swapped_words_to_healthy["fry"]="bake"
                    #print(step['methods'])
        #print(step['methods'])
        step_ingredients_th = step['ingredients']
        #print(swapped_words_to_healthy)
        step['ingredients'] = [swapped_words_to_healthy[x] if x in swapped_words_to_healthy else x for x in step_ingredients_th]
        raw_step = step['raw_step']
        splitted_step = nltk.word_tokenize(raw_step)
        splitted_step = [swapped_words_to_healthy[x] if x in swapped_words_to_healthy else x for x in splitted_step]
        step['raw_step'] = " ".join(splitted_step)
    return recipe


def to_non_healthy(recipe):
    '''
    Converts a recipe into a unhealthy version
    '''
    non_healthy_swap = json.load(open('./src/lib/transformations/unhealthy.json'))
    swapped_words_not_healthy = {}
    ingredient = recipe['ingredients']
    binder = ingredient['binder']
    carb = ingredient['carb']
    condiment = ingredient['condiment']
    primary_protein = ingredient['primary_protein']
    for ing in binder:
        matched_word_non_healthy = ing['matched_word']
        if matched_word_non_healthy in non_healthy_swap:
            ing['ingredient']=non_healthy_swap[matched_word_non_healthy]
            swapped_words_not_healthy[matched_word_non_healthy]=non_healthy_swap[matched_word_non_healthy]
            #double the lard
            if ing['ingredient']=='lard':
                ing['quantity']=ing['quantity']*(2)
    for ing in carb:
        matched_word_non_healthy = ing['matched_word']
        if matched_word_non_healthy in non_healthy_swap:
            ing['ingredient']=non_healthy_swap[matched_word_non_healthy]
            swapped_words_not_healthy[matched_word_non_healthy]=non_healthy_swap[matched_word_non_healthy]
            #multiply high fructose corn syrup by 1.5
            if ing['ingredient']=='high fructose corn syrup':
                ing['quantity']=ing['quantity']*(1.5)
    for ing in condiment:
        matched_word_non_healthy = ing['matched_word']
        if matched_word_non_healthy in non_healthy_swap:
            ing['ingredient']=non_healthy_swap[matched_word_non_healthy]
            swapped_words_not_healthy[matched_word_non_healthy]=non_healthy_swap[matched_word_non_healthy]
            if ing['ingredient']=='lard':
                ing['quantity']=ing['quantity']*(2)
    #change all primary protein to spam
    for ing in primary_protein:
        matched_word_non_healthy=ing['matched_word']
        ing['ingredient']="SPAM"
        swapped_words_not_healthy[matched_word_non_healthy]="SPAM"
    #change steps
    for step in recipe['steps']:
        #replace frying with baking
        if "bake" in step['methods']:
            fry_time = step['times']
            #baking takes 4 times as long as frying
            fry_time_array = fry_time[0].split(" ")
            #print(fry_time_array)
            orig_time=fry_time_array[0]
            fry_time_array[0] = str(eval(fry_time_array[0])*.25)
            step['times'][0]=" ".join(fry_time_array)
            swapped_words_not_healthy[orig_time]=fry_time_array[0]
            if "bake" in recipe['methods']['primary_methods']:
                for i in range(len(recipe['methods']['primary_methods'])):
                    if recipe['methods']['primary_methods'][i] == "bake":
                        #print(recipe['methods']['primary_methods'][i])
                        recipe['methods']['primary_methods'][i]="fry"
                        #print(recipe['methods']['primary_methods'][i])
            for i in range(len(step['methods'])):
                if step['methods'][i] == "bake":
                    #print("swap")
                    #print(step['methods'])
                    step['methods'][i] = "fry"
                    #print(method)
                    swapped_words_not_healthy["bake"]="fry"
                    #print(step['methods'])
        #print(step['methods'])
        step_ingredients_th = step['ingredients']
        #print(swapped_words_to_healthy)
        step['ingredients'] = [swapped_words_not_healthy[x] if x in swapped_words_not_healthy else x for x in step_ingredients_th]
        raw_step = step['raw_step']
        splitted_step = nltk.word_tokenize(raw_step)
        splitted_step = [swapped_words_not_healthy[x] if x in swapped_words_not_healthy else x for x in splitted_step]
        step['raw_step'] = " ".join(splitted_step)
    if not swapped_words_not_healthy:
        recipe['steps'].append(
            {
                "ingredients": ["bacon"],
                "tools": [],
                "methods": [],
                "times": [],
                "temperature": [],
                "raw_step": "add bacon"
            }
        )
        recipe['ingredients']['primary_protein'].append("bacon")
    return recipe
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
