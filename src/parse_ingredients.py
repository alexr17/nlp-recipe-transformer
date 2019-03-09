import nltk
import json
from src.lib.clean import valid_tkn
from src.lib.helpers import best_match

debug = False

fruits_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/fruits.txt')])
herbs_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/herbs.txt')])
vegetables_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/vegetables.txt')])
condiments_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/condiments.txt')])
carbs_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/carbs.txt')])
binders_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/binders.txt')])
protein_json = json.load(open('./src/lib/categories/food_groups/protein.json'))
primary_protein_kw = set(protein_json['primary'].keys())
secondary_protein_kw = set(protein_json['secondary'].keys())
tertiary_protein_kw = set(protein_json['tertiary'].keys())

food_groups = {
    "fruit": fruits_kw,
    "herb": herbs_kw,
    "vegetable": vegetables_kw,
    "condiment": condiments_kw,
    "carb": carbs_kw,
    "binder": binders_kw,
    "primary_protein": primary_protein_kw,
    "secondary_protein": secondary_protein_kw,
    "tertiary_protein": tertiary_protein_kw
}

def parse_ingredients(ingredients):
    '''
    Takes a list of ingredients
    And splits out the quantities and descriptor
    '''

    new_lst = []
    measurement_kw = set([line.strip() for line in open('./src/lib/categories/ingredients/quantities.txt')])
    descriptor_kw = set([line.strip() for line in open('./src/lib/categories/ingredients/descriptors.txt')])

    for raw_ingredient in ingredients:
        ingredient = nltk.word_tokenize(raw_ingredient)

        # measurement
        i = 0
        quantity = []
        while ingredient[i].isdigit() or "/" in ingredient[i]:
            quantity.append(ingredient[i])
            i += 1
        measurement = []
        flag = False
        for x in ingredient:
            if x == ')':
                flag = False
            if flag and (x in measurement_kw or x.isdigit()):
                measurement.append(x)
            elif x in measurement_kw:
                measurement.append(x)
            if x == '(':
                flag = True

        # Convert quantity from string to number
        number = 0
        for num in quantity:
            if "/" in num:
                # Fraction to float
                n,d = num.split('/')
                num = (float(n)/float(d))
            else:
                num = int(num)
            number += num

        descriptors = [x for x in ingredient if x in descriptor_kw]

        stopwords = set(descriptors) | set(measurement) | set(quantity)

        # ingredient
        ingredient = " ".join([x for x in ingredient if valid_tkn(x, stopwords, set())])

        # any word that we don't want at the beginning/end of the ingredient due to parsing
        strip_words = {'and', 'or', '&'}
        if ingredient[-3:] in strip_words:
            ingredient = ingredient[:-4]
        elif ingredient[:3] in strip_words:
            ingredient = ingredient[4:]

        new_lst.append(
            {
                "quantity": number,
                "measurement": " ".join(measurement),
                "ingredient": ingredient,
                "descriptors": descriptors,
                "raw_ingredient": raw_ingredient
            }
        )

    return new_lst

def kw_in_food_group_set(ingredient):
    '''
    Checks if a string (ingredient) is in one of the ingredient text files
    '''
    for fg in food_groups:
        if ingredient in food_groups[fg]:
            return fg
    return False

def split_ingredients(ingredients):
    '''
    Takes a list of ingredients and parses each ingredient
    Returns a list of parsed ingredient objects
    '''
    food_split = {
        "fruit": [],
        "herb": [],
        "vegetable": [],
        "condiment": [],
        "carb": [],
        "binder": [],
        "primary_protein": [],
        "secondary_protein": [],
        "tertiary_protein": []
    }
    for ingredient in ingredients:
        item = ingredient['ingredient']
        food_type = kw_in_food_group_set(item)
        if food_type:
            ingredient["matched_word"] = item
            food_split[food_type].append(ingredient)
            continue

        # split ingredient and iterate over each word
        sp_ing = item.split(' ')

        # do bigrams first, then singular words
        if len(sp_ing) > 1:
            bigrams = [sp_ing[i:] for i in range(2)]
            bigrams = zip(*bigrams)
            bigrams = [" ".join(bigram) for bigram in list(bigrams)]

            bigram_flag = False
            for bigram in bigrams:
                food_type = kw_in_food_group_set(bigram)
                if food_type:
                    ingredient["matched_word"] = bigram
                    bigram_flag = True
                    food_split[food_type].append(ingredient)
                    break

            if not bigram_flag:
                for tkn in sp_ing:
                    food_type = kw_in_food_group_set(tkn)
                    if food_type:
                        ingredient["matched_word"] = tkn
                        food_split[food_type].append(ingredient)
                        break
            if "matched_word" in ingredient:
                continue

        # now match with levenshtein
        min_lev = float("inf")
        food_group = ''
        food_match = ''
        for fg in food_groups:
            lev_score, best_food = best_match(min_lev, food_groups[fg], item)
            if lev_score < min_lev:
                min_lev = lev_score
                food_group = fg
                food_match = best_food
        ingredient["matched_word"] = food_match
        food_split[food_group].append(ingredient)

        if debug and len(ingredient) < min_lev * 1.5:
            print(f"Ingredient: ({ingredient['ingredient']}) matched to ({ingredient['matched_word']}) has a lev score of {min_lev} that is extremely high")

    return food_split
