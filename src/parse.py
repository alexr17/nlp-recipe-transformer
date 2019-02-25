from bs4 import BeautifulSoup
from src.lib.web_api import web_get
### import statements above here


def parse_html(cooking_url):
	'''
	Takes a cooking url (assumed to be allrecipes) and extracts the relevant
	information: cuisines, ingredients, steps, etc.
	
	It returns an object with the information about the recipe.
	'''
	html = web_get(cooking_url)
	soup = BeautifulSoup(html, 'html.parser')

	cuisine_html = soup.select('meta[itemprop="recipeCategory"]')
	cuisines = []
	for i in cuisine_html:
		cuisines.append(i['content'].strip())

	ingredients_html = soup.select('span.recipe-ingred_txt.added')
	ingredients = []
	for i in ingredients_html:
		ingredients.append(i.text.strip())

	steps_html = soup.select('span.recipe-directions__list--item')
	steps = []
	for i in steps_html:
		steps.append(i.text.strip())

	return {
		"cuisines": cuisines,
		"ingredients": ingredients,
		"steps": steps
	}

def parse_ingredients(ingredients):
	'''
	Takes a list of ingredients
	'''
	return False