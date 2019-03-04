import json
from bs4 import BeautifulSoup
from src.parse_ingredients import parse_ingredients, split_ingredients
from src.parse_steps import parse_methods, parse_tools, split_steps
from src.lib.web_api import web_get
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

def format_recipe(recipe):
    '''
    Takes a recipe url and runs the parsing methods, returning a parsed recipe
    '''
    raw_recipe = parse_html(recipe)
    raw_recipe['ingredients'] = parse_ingredients(raw_recipe['ingredients'])

    ingredients = [ingredient['ingredient'] for ingredient in raw_recipe['ingredients']]
    raw_recipe['ingredients'] = split_ingredients(raw_recipe['ingredients'])

    tools = parse_tools(raw_recipe['steps'])
    raw_recipe['tools'] = tools

    methods = parse_methods(raw_recipe['steps'])
    raw_recipe['methods'] = methods

    steps = split_steps(raw_recipe['steps'], ingredients, tools, methods)
    raw_recipe['steps'] = steps

    return raw_recipe
