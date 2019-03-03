import nltk
from bs4 import BeautifulSoup
from src.lib.clean import valid_tkn
from src.lib.web_api import web_get
from src.lib.helpers import levenshtein
# import statements above here


def parse_html(cooking_url):
    '''
    Takes a cooking url (assumed to be allrecipes) and extracts the relevant
    information: cuisines, ingredients, steps, etc.

    It returns an object with the information about the recipe.
    '''
    try:
        html = web_get(cooking_url)
    except:
        return {}
    soup = BeautifulSoup(html, 'html.parser')

    cuisine_html = soup.select('meta[itemprop="recipeCategory"]')
    cuisines = []
    for cuisine in cuisine_html:
        cuisine_text = cuisine['content'].strip().lower()
        if cuisine_text:
            cuisines.append(cuisine_text)

    ingredients_html = soup.select('span.recipe-ingred_txt.added')
    ingredients = []
    for ingredient in ingredients_html:
        ingredient_text = ingredient.text.strip().lower()
        if ingredient_text and ingredient_text not in ['add all ingredients to list']:
            ingredients.append(ingredient_text)

    steps_html = soup.select('span.recipe-directions__list--item')
    steps = []
    for step in steps_html:
        step_text = step.text.strip().lower()
        if step_text:
            steps.append(step_text)

    title = soup.select('h1.recipe-summary__h1')[0].text.strip().lower()

    return {
        "title": title,
        "recipe_categories": cuisines,
        "ingredients": ingredients,
        "steps": steps
    }


def parse_ingredients(ingredients):
    '''
    Takes a list of ingredients
    And splits out the quantities and method
    '''

    new_lst = []
    measurement_kw = set([line.strip() for line in open('./src/lib/categories/ingredients/quantities.txt')])
    method_kw = set([line.strip() for line in open('./src/lib/categories/ingredients/methods.txt')])

    for raw_ingredient in ingredients:
        ingredient = nltk.word_tokenize(raw_ingredient)
        print(ingredient)

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
            if flag:
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

        # default quantity to 1
        # if not number:
        # 	number = 1
        methods = [x for x in ingredient if x in method_kw]

        stopwords = set(methods) | set(measurement) | set(quantity)

        # ingredient
        ingredient = " ".join([x for x in ingredient if valid_tkn(x, stopwords, set())])

        # any word that we don't want at the beginning/end of the ingredient due to parsing
        strip_words = {'and'}
        if ingredient[-3:] in strip_words:
            ingredient = ingredient[:-4]
        elif ingredient[:3] in strip_words:
            ingredient = ingredient[4:]

        new_lst.append(
            {
                "quantity": number,
                "measurement": " ".join(measurement),
                "ingredient": ingredient,
                "methods": methods,
                "raw_ingredient": raw_ingredient
            }
        )

    return new_lst

fruits_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/fruits.txt')])
herbs_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/herbs.txt')])
vegetables_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/vegetables.txt')])
condiments_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/condiments.txt')])
carbs_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/carbs.txt')])
binders_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/binders.txt')])
protein_kw = set([line.strip() for line in open('./src/lib/categories/food_groups/protein.txt')])

food_groups = {
    "fruit": fruits_kw,
    "herb": herbs_kw,
    "vegetable": vegetables_kw,
    "condiment": condiments_kw,
    "carb": carbs_kw,
    "binder": binders_kw,
    "protein": protein_kw
}
def kw_in_food_group_set(ingredient):
    if ingredient in fruits_kw:
        return "fruit"
    elif ingredient in herbs_kw:
        return "herb"
    elif ingredient in vegetables_kw:
        return "vegetable"
    elif ingredient in condiments_kw:
        return "condiment"
    elif ingredient in carbs_kw:
        return "carb"
    elif ingredient in binders_kw:
        return "binder"
    elif ingredient in protein_kw:
        return "protein"
    else:
        return False

def split_ingredients(ingredients):
    food_split = {
        "fruit": [],
        "herb": [],
        "vegetable": [],
        "condiment": [],
        "carb": [],
        "binder": [],
        "protein": []
    }
    for ingredient in ingredients:
        item = ingredient['ingredient']
        food_type = kw_in_food_group_set(item)
        if food_type:
            food_split[food_type].append(ingredient)
        else:
            # split ingredient and iterate
            sp_ing = item.split(' ')
            flag = False
            if len(sp_ing) > 1:
                for tkn in sp_ing:
                    food_type = kw_in_food_group_set(tkn)
                    if food_type:
                        food_split[food_type].append(ingredient)
                        flag = True
            if not flag:
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
                food_split[food_group].append(ingredient)

    return food_split



def best_match(min_lev, food_group, ingredient):
    food_match = ''
    for food in food_group:
        lev = levenshtein(food, ingredient)
        # print(lev)
        if lev < min_lev:
            min_lev = lev
            food_match = food
    return min_lev, food_match
