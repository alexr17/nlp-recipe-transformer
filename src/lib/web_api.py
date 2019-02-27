from urllib.request import urlopen

def web_get(url):
    html = urlopen(url)
    return html

def get_ingredients_list():
    '''
    Gets a list of ingredients
    '''
    # https://www.bbc.com/food/ingredients
    # https://github.com/NYTimes/ingredient-phrase-tagger
    # https://github.com/lingcheng99/Flavor-Network
    # First recipe: 6663