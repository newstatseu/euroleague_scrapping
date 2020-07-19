import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'}

session = requests.Session()
session.trust_env = False

def simple_get(url):
    call = session.get(url, headers=headers, timeout = 25)
    return call.content