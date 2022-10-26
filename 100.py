import requests
import webbrowser as wb
from bs4 import BeautifulSoup as bs
from ban import ban


def get_links():
    links = []
    url_list = get_url_list()
    for i, url in enumerate(url_list):
        r = requests.get(url)
        print(f'parsing {i+1} page')
        links = [*links, *parse(r)]
    return links


def get_url_list():
    page_start, page_end = map(int, input('start to end >>> ').split())
    url_list = list(f"https://reestr.rublacklist.net/ru/?page={page}&status=1&gov=3&date_start=&date_end=" for page in
                    range(page_start, page_end + 1))
    return url_list


def parse(r):
    links = []
    soup = bs(r.text, "html5lib")
    for i, tr in enumerate(soup.find_all('a', href=True)):
        if 'record' in tr['href'] and i % 2:
            link = tr.text
            if not any([ban_word in link for ban_word in ban]):
                links.append(link)
    return links


def main():
    source = r'C:\Users\matiz\AppData\Local\Yandex\YandexBrowser\Application\browser.exe'
    wb.register('ya', None, wb.BackgroundBrowser(source))
    final_links = get_links()
    print(f'{len(final_links)} links')
    a = int(input('links to open >>> '))
    for cnt in range(a):
        wb.get('ya').open_new_tab(final_links[cnt])


main()
