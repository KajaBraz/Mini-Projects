from urllib import request
from bs4 import BeautifulSoup


def get_url_content(url: str) -> [str]:
    html = request.urlopen(url).read()
    soup = BeautifulSoup(html)
    for script in soup(['script', 'style']):
        script.decompose()
    strips = list(soup.stripped_strings)
    return strips


def get_text(string_list: [str]) -> str:
    return ' '.join(string_list)


if __name__ == '__main__':
    content = get_url_content('https://www.tuttosport.com/news/calcio/coppa-italia/2021/05/13-81655553/'
                              'juve-atalanta_la_finale_di_coppa_italia_con_4300_spettatori')
    print(content)
