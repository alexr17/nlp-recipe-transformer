from bs4 import BeautifulSoup
from src.lib.web_api import web_get
### import statements above here


def parse_html(url):
	html = web_get(url)
	soup = BeautifulSoup(html, 'html.parser')

	cuisine_html = soup.select('meta[itemprop="recipeCategory"]')
	cuisines = []
	for i in cuisine_html:
		cuisines.append(i['content'])

	instructions_html = soup.select('span.recipe-ingred_txt.added')
	instructions = []
	for i in instructions_html:
		instructions.append(i.text)

	# TODO: implement this
