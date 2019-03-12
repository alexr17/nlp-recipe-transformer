import json
import nltk
import copy
from os import listdir
from os.path import isfile, join
import re
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
    recipe = copy.deepcopy(recipe)

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
            if len(fry_time) != 0:
                for i in range(len(fry_time)):
                    #baking takes 4 times as long as frying
                    fry_time_array = fry_time[i].split(" ")
                    #print(fry_time_array)
                    orig_time=fry_time_array[0]
                    fry_time_array[0] = str(eval(fry_time_array[0])*4)
                    step['times'][i]=" ".join(fry_time_array)
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
            for i in range(len(step['tools'])):
                if step['tools'][i]=='pan':
                    step['tools'][i]='pan'
                    swapped_words_to_healthy['pan']='oven'
        step_ingredients_th = step['ingredients']
        #print(swapped_words_to_healthy)
        step['ingredients'] = [swapped_words_to_healthy[x] if x in swapped_words_to_healthy else x for x in step_ingredients_th]
        for ing in swapped_words_to_healthy:
            if ing in step['raw_step']:
                step['raw_step'] = step['raw_step'].replace(ing, swapped_words_to_healthy[ing])
        '''
        raw_step = step['raw_step']
        splitted_step = nltk.word_tokenize(raw_step)
        splitted_step = [swapped_words_to_healthy[x] if x in swapped_words_to_healthy else x for x in splitted_step]
        step['raw_step'] = " ".join(splitted_step)
        re.sub(r'\s+([?.!"])', r'\1', step['raw_step'])
        '''
        splitted_title = recipe['title'].split(" ")
        splitted_title = [swapped_words_to_healthy[x] if x in swapped_words_to_healthy else x for x in splitted_title]
        recipe['title'] = " ".join(splitted_title)
    return recipe


def to_non_healthy(recipe):
    '''
    Converts a recipe into a unhealthy version
    '''
    recipe = copy.deepcopy(recipe)

    non_healthy_swap = json.load(open('./src/lib/transformations/unhealthy.json'))
    protein_dict = protein_json['primary']
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
        matched_word_non_healthy = ing['matched_word']
        if matched_word_non_healthy in protein_dict:
            if protein_dict[matched_word_non_healthy]['category'] in {'meat','poultry','fish'}:
                ing['ingredient']='SPAM'
        swapped_words_not_healthy[matched_word_non_healthy]="SPAM"
    #change steps
    for step in recipe['steps']:
        #replace frying with baking
        if "bake" in step['methods']:
            fry_time = step['times']
            if len(fry_time)!= 0:
                for i in range(len(fry_time)):
            #baking takes 4 times as long as frying
                    fry_time_array = fry_time[i].split(" ")
            #print(fry_time_array)
                    orig_time=fry_time_array[0]
                    fry_time_array[0] = str(eval(fry_time_array[0])*.25)
                    step['times'][i]=" ".join(fry_time_array)
                    swapped_words_not_healthy[orig_time]=fry_time_array[0]
            if "bake" in recipe['methods']['primary_methods']:
                for i in range(len(recipe['methods']['primary_methods'])):
                    if recipe['methods']['primary_methods'][i] == "bake":
                        #print(recipe['methods']['primary_methods'][i])
                        recipe['methods']['primary_methods'][i]="fry"
                        #print(recipe['methods']['primary_methods'][i])
                if 'oven' in recipe['tools']:
                    for i in range(len(recipe['tools'])):
                        if recipe['tools'][i]=='oven':
                            recipe['tools'][i]='frying pan'
            for i in range(len(step['methods'])):
                if step['methods'][i] == "bake":
                    #print("swap")
                    #print(step['methods'])
                    step['methods'][i] = "fry"
                    #print(method)
                    swapped_words_not_healthy["bake"]="fry"
                    #print(step['methods'])
            for i in range(len(step['tools'])):
                if step['tools'][i]=='oven':
                    step['tools'][i]='frying pan'
                    swapped_words_not_healthy['oven']='frying pan'
        #print(step['methods'])
        step_ingredients_th = step['ingredients']
        #print(swapped_words_to_healthy)
        step['ingredients'] = [swapped_words_not_healthy[x] if x in swapped_words_not_healthy else x for x in step_ingredients_th]
        for ing in swapped_words_not_healthy:
            if ing in step['raw_step']:
                step['raw_step'] = step['raw_step'].replace(ing, swapped_words_not_healthy[ing])
        '''
        raw_step = step['raw_step']
        splitted_step = nltk.word_tokenize(raw_step)
        splitted_step = [swapped_words_not_healthy[x] if x in swapped_words_not_healthy else x for x in splitted_step]
        step['raw_step'] = " ".join(splitted_step)
        re.sub(r'\s+([?.!"])', r'\1', step['raw_step'])
        step['raw_step']=" ".join(step['raw_step'].split())
        '''
        splitted_title = recipe['title'].split(" ")
        splitted_title = [swapped_words_not_healthy[x] if x in swapped_words_not_healthy else x for x in splitted_title]
        recipe['title'] = " ".join(splitted_title)
    if not swapped_words_not_healthy:
        recipe['steps'].append(
            {
                "ingredients": ["bacon"],
                "tools": ["skillet"],
                "methods": [],
                "times": [],
                "temperature": [],
                "raw_step": "put bacon in skillet and fry, once bacon is cooked crumple and add"
            }
        )
        recipe['ingredients']['primary_protein'].append("bacon")
        recipe['title']=recipe['title']+'with bacon'
    return recipe


def to_cuisine(recipe, cuisine):
    '''
    Converts a parsed recipe to a given cuisine
    '''
    recipe = copy.deepcopy(recipe)

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


def cooking_method(recipe,convert_from,convert_to):
    '''
    Converts a parsed recipe from the convert_from to the convert_to
    Options are bake, fry, grill and steam 
    '''
    recipe = copy.deepcopy(recipe)

    swapped_words_cook = {}
    time_coeff = {}
    temp_coeff = {}
    time_coeff['bake']=1
    time_coeff['fry']=4
    time_coeff['grill']=5
    time_coeff['steam']=4
    temp_coeff['bake']=0
    temp_coeff['fry']= -50
    temp_coeff['grill']= 100
    for step in recipe['steps']:
        #bake temp 0 ,time 0
        #fry temp -50, time /4
        #grill temp +100, time /5
        #steam temp none, time /4
        if convert_from in step['methods'] or convert_from in step['tools'] or 'cook' in step['methods']:
            new_time = step['times']
            #change cook time based on coeff
            if len(new_time)!=0:
                for i in range(len(new_time)):
                    new_time_array = new_time[i].split(" ")
                    orig_time=new_time_array[0]
                    new_time_array[0] = str(eval(new_time_array[0])*(time_coeff[convert_from]/time_coeff[convert_to]))
                    step['times'][i]=" ".join(new_time_array)
                    swapped_words_cook[orig_time]=new_time_array[0]
        #change temp based on coeff
        #if converting to steam remove temp
        if convert_to =='steam':
            step['temperature']= None
        else:
            #if converting from steam set a defalt temp
            #print('reached1')
            #print(step['methods'])
            #print(step['tools'])
            if ((convert_from =='steam') and (('steam' in step['methods'])or ('cook' in step['methods'])) or (((('grill' in step['methods'])or('fry'in step['methods']) or ('bake' in step['methods'])) or ('grill' in step['tools'])) and (len(step['temperature'])) == 0)):
                #print('reached2')
                if convert_to=='bake':
                    step['temperature']=['425 degrees']
                if convert_to=='fry':
                    step['temperature']=['375 degrees']
                if convert_to=='grill':
                    step['temperature']=['525 degrees']
            else:
                new_temp = step['temperature']
                #print(new_temp)
                if len(new_temp)!=0:
                    new_temp_array = new_temp[0].split(" ")
                    orig_temp=new_temp_array[0]
                    new_temp_array[0] = str(eval(new_temp_array[0])*(temp_coeff[convert_from]+temp_coeff[convert_to]))
                    step['temperature'][0]=" ".join(new_temp_array)
                    swapped_words_cook[orig_temp]=new_temp_array[0]
        #change primary methods in recipe
        for i in range(len(step['methods'])):
            if step['methods'][i] == convert_from or step['methods'][i]=='cook':
                #print("swap")
                #print(step['methods'])
                step['methods'][i] = convert_to
                #print(method)
                if step['methods'][i]== convert_from:
                    swapped_words_cook[convert_from]=convert_to
                else:
                    swapped_words_cook['cook']=convert_to
                #print(step['methods'])
        if convert_from in step['tools']:
            step['tools'].remove(convert_from)
            step['methods'].append(convert_to)
            swapped_words_cook[convert_from]=convert_to
        if convert_from in recipe['tools']:
            recipe['tools'].remove(convert_from)
            recipe['methods']['primary_methods'].append(convert_to)
        if convert_from in recipe['methods']['primary_methods'] or 'cook' in recipe['methods']['primary_methods']:
            for i in range(len(recipe['methods']['primary_methods'])):
                if recipe['methods']['primary_methods'][i] == convert_from or recipe['methods']['primary_methods'][i]=='cook':
                    #print(recipe['methods']['primary_methods'][i])
                    recipe['methods']['primary_methods'][i]=convert_to
                    #print(recipe['methods']['primary_methods'][i])   
        step['ingredients'] = [swapped_words_cook[x] if x in swapped_words_cook else x for x in step['ingredients']]
        for ing in swapped_words_cook:
            if ing in step['raw_step']:
                step['raw_step'] = step['raw_step'].replace(ing, swapped_words_cook[ing])
        '''
        raw_step = step['raw_step']
        splitted_step = nltk.word_tokenize(raw_step)
        splitted_step = [swapped_words_cook[x] if x in swapped_words_cook else x for x in splitted_step]
        step['raw_step'] = " ".join(splitted_step)
        '''
    return recipe