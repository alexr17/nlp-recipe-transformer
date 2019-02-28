import nltk
from bs4 import BeautifulSoup
from src.lib.clean import valid_tkn
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

	new_lst = []
	quantities_kw = set([line.strip() for line in open('./src/lib/categories/ingredients/quantities.txt')])
	method_kw = set([line.strip() for line in open('./src/lib/categories/ingredients/methods.txt')])
	
	for raw_ingredient in ingredients:
		ingredient = nltk.word_tokenize(raw_ingredient)
		
		# measurement
		i = 0
		quantity = []
		while ingredient[i].isdigit() or "/" in ingredient[i]:
			quantity.append(ingredient[i])
			i += 1
		measurement = [x for x in ingredient if x in quantities_kw]

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
