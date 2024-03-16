import requests
from bs4 import BeautifulSoup
import json


BASE_URL = 'http://quotes.toscrape.com'

quotes_list = []
authors_list = []


def get_page_content(url):
    response = requests.get(url)
    content = BeautifulSoup(response.content, 'html.parser')
    return content


def get_quotes(content):
    q = {}
    quotes = content.find_all('div', class_='quote')

    for quote in quotes:
        author = quote.find("small", class_="author").text.strip()
        get_authors(get_page_content(BASE_URL + quote.a["href"]))
        tags_list = [tag.text for tag in quote.find_all("a", class_="tag")]
        q = {
            "quote": quote.find("span", class_="text").text.strip(),
            "author": author,
            "tags": tags_list
        }
        quotes_list.append(q)


def get_authors(content):
    authors = content.find('div', class_='author-details')
    author = {
        "fullname": authors.find("h3", class_="author-title").text,
        "born_date": authors.find("span", class_="author-born-date").text,
        "born_location": authors.find(
            "span", class_="author-born-location"
        ).text,
        "description": authors.find(
            "div", class_="author-description"
        ).text.strip(),
    }
    authors_list.append(author)



def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


page_content = get_page_content(BASE_URL)

while True:
    get_quotes(page_content)

    next_page_link = page_content.find('li', class_='next')
    if next_page_link is None:
        break

    next_page_url = BASE_URL + page_content.find('li', class_='next').a["href"]
    page_content = get_page_content(next_page_url)

save_to_json(quotes_list, 'quotes.json')
save_to_json(authors_list, 'authors.json')
