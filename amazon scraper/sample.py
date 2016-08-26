from pprint import pprint
from bs4 import BeautifulSoup
import requests

url = 'http://www.amazon.com/dp/B00267T9LG/'
response = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})

soup = BeautifulSoup(response.content)
tags = {}
for li in soup.select('table#productDetails_techSpec_section_1 tr'):
    try:
        title = li.b
        key = title.text.strip().rstrip(':')
        value = title.next_sibling.strip()

        tags[key] = value
    except AttributeError:
        break

pprint(tags)
