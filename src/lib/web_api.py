import requests

def web_get(url, resp_type='html'):
    if resp_type == 'html':
        data = requests.get(url).html()
    elif resp_type == 'json':
        data = requests.get(url).json()
    else:
        return False
    return data