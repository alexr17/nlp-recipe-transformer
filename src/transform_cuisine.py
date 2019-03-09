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
                ing['transformed_ing'] = ing['ingredient']
                if len(cuisine_food_type):
                    if type(cuisine_food_type) == list:
                        cuisine_food_type.remove(ing['matched_word'])
                    elif type(cuisine_food_type) == dict:
                        del cuisine_food_type[ing['matched_word']]

def transform_cuisine_steps(recipe, cuisine):
    '''
    Transforms the steps in the recipe for the given cuisine
    '''
    return False

def set_protein_ingredient(ing, protein_type, cuisine):
    '''
    Takes the protein type (primary_protein, secondary_protein, etc.) and transforms the protein
    '''
    # get the protein category for the ingredient from protein.json
    protein_category = protein_json[protein_type.replace(
        '_protein', '')][ing['matched_word']]['category']
    if len(cuisine[protein_type][protein_category]):
        ing['transformed_ing'] = cuisine[protein_type][protein_category].pop()
    else:
        ing['transformed_ing'] = ing['ingredient']


def set_generic_ingredient(ing, mappings):
    '''
    For generic ingredients (not protein)
    '''
    # if transformations are list
    if type(mappings) == list:
        # remove the first ingredient
        ing['transformed_ing'] = mappings.pop(0)
    # if the transformations are a dictionary
    # then try to find each key in the ingredient
    elif type(mappings) == dict:

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
        ing['transformed_ing'] = mappings[food_group]['types'].pop(
            0) + ' ' + food_group
        if not len(mappings[food_group]):
            del mappings[food_group]

def set_custom_ingredient(ing, mappings):
    '''
    Overwrites ingredients with custom mappings
    '''
    if ing['matched_word'] in mappings:
        ing['transformed_ing'] = mappings[ing['matched_word']]
        return True
    return False