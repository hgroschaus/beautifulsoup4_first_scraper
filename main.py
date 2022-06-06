import requests
from bs4 import BeautifulSoup
import pandas as p


def extract_data(div_quote):
    quote = div_quote.find('span', {'class':'text'}).get_text()
    author = div_quote.find('small', {'class':'author'}).get_text()
    tags = [tag.get_text() for tag in div_quote.find_all('a', {'class':'tag'})]
    data = {
      'quote': quote,
      'author': author,
      'tags': tags
    }
    return data


def get_quote(url):
    page = requests.get(url)
    parsed_page = BeautifulSoup(page.content, 'lxml')
    quotes = parsed_page.find_all('div', {'class':'quote'})

    if len(quotes) > 0:
        quote_list = [extract_data(q) for q in quotes]
        return quote_list
    else:
        return None
    

data = get_quote('https://quotes.toscrape.com/')

for i in range(2, 100):
    page_url = f'https://quotes.toscrape.com/page/{i}/'
    current_page_quote = get_quote(page_url)
    if not current_page_quote:
        break
    data += current_page_quote

    data_p = p.DataFrame.from_dict(data)
    data_p.to_csv('/home/hgroschaus/pproj/python/web_scrapping/beautifulsoup/data.csv')