import requests
from bs4 import BeautifulSoup

getPageSoup = lambda url: BeautifulSoup(requests.get(url).text, 'html.parser') 


def parseQuotes(url='http://quotes.toscrape.com/'):
    soup = getPageSoup(url)
    qt = soup.find_all('span', class_='text')
    qa = soup.find_all('small', class_='author')
    qtags = soup.find_all('div', class_='tags')
    for idx, text in enumerate(qt):
        quote_tags = ', '.join(x.text for x in qtags[idx].find_all('a', class_='tag'))
        print(f'{text.text} - {qa[idx].text} [{quote_tags}]')


def parseScrapingClubPagination(url='https://scrapingclub.com/exercise/list_basic/'):
    pages = getPageSoup(url).find('ul', class_='pagination'
                                ).find_all('a', class_='page-link')
    pages = [x['href'] for x in pages]
    if not pages:
        print(f'No pages found @ {url}')
        return
    allcount = 0
    for page_idx, suburl in enumerate(pages, 1):
        soup = getPageSoup(url + suburl)
        items = soup.find_all('div', class_='col-lg-4 col-md-6 mb-4')
        for i in items:
            allcount += 1
            item_name = i.find('h4', class_='card-title').text.strip()
            item_price = i.find('h5').text
            print(f'{page_idx=}/{allcount=}. {item_price=}, {item_name=}')

if __name__ == '__main__':
    # parseQuotes()
    parseScrapingClubPagination()
