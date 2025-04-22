from bs4 import BeautifulSoup
import json
import requests
from pprint import pprint


def main():
    # get html file from url
    url = "https://webscraper.io/test-sites/e-commerce/allinone"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    print(soup)


if __name__ == "__main__":
    main()
