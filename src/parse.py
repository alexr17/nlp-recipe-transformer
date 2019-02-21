from src.lib.web_api import web_get
### import statements above here


def parse_html(url):
    html = web_get(url)

    # TODO: implement this