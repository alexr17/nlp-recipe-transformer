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

    primary_protein_dict = protein_json['primary']

    vegetarian_swap = json.load(open('./src/lib/transformations/vegetarian.json'))
    meat_descriptors = set([line.strip() for line in open('./src/lib/transformations/meat_descriptors.txt')])

    swapped_words = {}
    for protein in primary_protein:
        matched_word = protein['matched_word']


        if matched_word in primary_protein_dict:
            if primary_protein_dict[matched_word] == "meat":
                if matched_word in vegetarian_swap:
                    protein['ingredient'] = vegetarian_swap[matched_word]
                    swapped_words[matched_word] = vegetarian_swap[matched_word]
        new_raw_ingredient = []
        raw_ingredient = protein['raw_ingredient'].split(" ")
        for x in protein['raw_ingredient'].split(" "):
            #print(x)
            if x in swapped_words:
                new_raw_ingredient.append(swapped_words[x])
            elif x in meat_descriptors:
                #print(x)
                new_raw_ingredient.append("")
            else:
                new_raw_ingredient.append(x)

        protein['raw_ingredient'] = " ".join(new_raw_ingredient)

    # Convert directions to vegetarian
    for step in recipe['steps']:
        step_ingredients = step['ingredients']
        step['ingredients'] = [swapped_words[x] if x in swapped_words else x for x in step_ingredients]

        raw_step = step['raw_step']
        splitted_step = nltk.word_tokenize(raw_step)
        splitted_step = [swapped_words[x] if x in swapped_words else x for x in splitted_step]
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
    

def to_cuisine(recipe, cuisine):
    '''
    Converts a parsed recipe to a given cuisine
    '''
    return False
