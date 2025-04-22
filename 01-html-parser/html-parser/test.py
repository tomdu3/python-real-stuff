import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint

url = "https://www.bestbuy.com/site/insignia-35-pint-dehumidifier-with-energy-star-certification-white/6385840.p"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

page = requests.get(url, headers=headers)
if page.status_code == 200:
    soup = BeautifulSoup(page.text, "html.parser")
else:
    raise Exception(f"Failed to fetch page. HTTP status code: {page.status_code}")


pprint(soup.prettify())
