from src.parse import parse_html
# import statements above here

def run():
    parse_html('https://www.allrecipes.com/recipe/223203/orzo-and-chicken-stuffed-peppers/?internalSource=streams&referringId=13289&referringContentType=Recipe%20Hub&clickId=st_trending_b')
    return False

if __name__ == '__main__':
    run()
