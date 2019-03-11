import json
from src.lib.helpers import best_match
protein_json = json.load(open('./src/lib/categories/food_groups/protein.json'))

def transform_cuisine_ingredients(recipe, cuisine):
    '''
    Takes the recipe and cuisine and transforms the ingredients in the recipe for that cuisine
    '''
    for food_type in recipe['ingredients']:

        cuisine_food_type = cuisine[food_type]
        for ing in recipe['ingredients'][food_type]:
            # don't transform ingredients without a unit
            if ing['measurement'] == '':
                continue
    
            # overwrite the changes we made for the ingredient (if any customizations are found)
            if set_custom_ingredient(ing, cuisine['custom']):
                continue

            # special method for protein
            if 'protein' in food_type:
                set_protein_ingredient(
                    ing, food_type, cuisine)
                continue

            # if the matched word is not already an ingredient in the cuisine
            if len(cuisine_food_type) and ing['matched_word'] not in cuisine_food_type:
                        # if any (key in ing['matched_word']:
                set_generic_ingredient(
                    ing, cuisine_food_type)
            # if the ingredient is already a part of the cuisine, then remove it from the cuisine dict
            else:
                if len(cuisine_food_type):
                    if type(cuisine_food_type) == list:
                        cuisine_food_type.remove(ing['matched_word'])
                    elif type(cuisine_food_type) == dict:
                        del cuisine_food_type[ing['matched_word']]

def transform_cuisine_steps(recipe, cuisine):
    '''
    Transforms the steps in the recipe for the given cuisine
    '''
    mapping = generate_ingredient_mapping(recipe['ingredients'])
    for step in recipe['steps']:
        # transform ingredients in steps
        new_ingredients = []
        for ing in step['ingredients']:
            if ing in mapping:
                new_ingredients.append(mapping[ing])
        step['ingredients'] = new_ingredients
        
        # transform raw step
        for ing in mapping:
            if ing in step['raw_step']:
                step['raw_step'] = step['raw_step'].replace(ing, mapping[ing])
    
    for ing in mapping:
        if ing in recipe['title']:
            recipe['title'] = recipe['title'].replace(ing, mapping[ing])
    return False

def generate_ingredient_mapping(ingredients):
    '''
    Generates the ingredient mapping for the recipe
    '''
    mapping = {}
    for food_type in ingredients:
        for ing in ingredients[food_type]:
            mapping[ing['matched_word']] = ing['ingredient']
    return mapping

def set_protein_ingredient(ing, protein_type, cuisine):
    '''
    Takes the protein type (primary_protein, secondary_protein, etc.) and transforms the protein
    '''
    # get the protein category for the ingredient from protein.json
    protein_category = protein_json[protein_type.replace(
        '_protein', '')][ing['matched_word']]['category']
    if len(cuisine[protein_type][protein_category]):
        ing['ingredient'] = cuisine[protein_type][protein_category].pop()


def set_generic_ingredient(ing, mappings):
    '''
    For generic ingredients (not protein)
    '''
    # if transformations are list
    if type(mappings) == list:
        # remove the first ingredient
        ing['ingredient'] = mappings.pop(0)
    # if the transformations are a dictionary
    # then try to find each key in the ingredient
    elif type(mappings) == dict:
        # print('using dict for ing:')
        # print(json.dumps(ing, indent=2))
        # use levenshtein distance to find best match
        min_lev = float("inf")
        food_group = ''
        food_match = ''
        for key in mappings:
            # print(set(mappings[key]['alt'] + [key]))
            keywords = set(mappings[key]['alt'] + [key])

            lev_score, best_food = best_match(
                min_lev, keywords, ing['matched_word'])
            # print(lev_score, ing['matched_word'], best_food)
            if lev_score < min_lev:
                min_lev = lev_score
                food_group = key
                food_match = best_food

                # if there is an exact match break out of the loop
                if lev_score == 0:
                    break

        # now at this point our food_group is the key in mappings
        # that we want to extract the transformed ingredient from
        # print(mappings[food_group])
        ing['ingredient'] = mappings[food_group]['types'].pop(
            0) + ' ' + food_group
        if not len(mappings[food_group]['types']):
            del mappings[food_group]

def set_custom_ingredient(ing, mappings):
    '''
    Overwrites ingredients with custom mappings
    '''
    if ing['matched_word'] in mappings:
        ing['ingredient'] = mappings[ing['matched_word']]
        return True
    return False