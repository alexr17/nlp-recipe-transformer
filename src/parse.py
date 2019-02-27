from bs4 import BeautifulSoup
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


def parse_ingredients(ingredients):
	'''
	Takes a list of ingredients
	And splits it into categories
	'''
	return False
