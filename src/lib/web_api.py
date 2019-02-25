from urllib.request import urlopen

def web_get(url):
    html = urlopen(url)
    return html
