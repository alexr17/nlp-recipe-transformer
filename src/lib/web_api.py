from urllib.request import urlopen
from bs4 import BeautifulSoup

def web_get(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    return soup
