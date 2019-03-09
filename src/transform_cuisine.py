import json
from src.lib.helpers import best_match

protein_json = json.load(open('./src/lib/categories/food_groups/protein.json'))
def transform_cuisine_ingredients(recipe, cuisine):
    '''
    Takes the recipe and cuisine and transforms the ingredients in the recipe for that cuisine
    '''
    for food_type in recipe['ingredients']:

        c_transformations = cuisine[food_type]
        for ing in recipe['ingredients'][food_type]:
            # special method for protein
            if 'protein' in food_type:
                set_cuisine_protein_ingredient(
                    ing, food_type, cuisine, c_transformations)
                continue

            # if the matched word is not already an ingredient in the cuisine
            if len(c_transformations) and ing['matched_word'] not in c_transformations:
                        # if any (key in ing['matched_word']:
                set_cuisine_generic_ingredient(
                    ing, cuisine, c_transformations)
                # if the ingredient is already a part of the cuisine, then remove it from the cuisine dict
            else:
                ing['transformed_ing'] = ing['ingredient']
                if len(c_transformations):
                    if type(c_transformations) == list:
                        c_transformations.remove(ing['matched_word'])
                    elif type(c_transformations) == dict:
                        del c_transformations[ing['matched_word']]


def set_cuisine_protein_ingredient(ing, protein_type, cuisine, mappings):
    '''
    Takes the protein type (primary_protein, secondary_protein, etc.) and transforms the protein
    '''
    print(mappings)
    # right now we have an ingredient,
    protein_category = protein_json[protein_type.replace(
        '_protein', '')][ing['matched_word']]['category']
    if len(cuisine[protein_type][protein_category]):
        ing['transformed_ing'] = cuisine[protein_type][protein_category].pop()
    else:
        ing['transformed_ing'] = ing['ingredient']


def set_cuisine_generic_ingredient(ing, cuisine, mappings):
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

# def set_cuisine_custom_ingredient(ing, cuisine, mappings):
