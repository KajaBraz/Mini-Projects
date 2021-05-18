import trafilatura
from bs4 import BeautifulSoup
from urllib import request
from textblob import TextBlob


def get_url_content(url: str) -> [str]:
    html = request.urlopen(url).read()
    soup = BeautifulSoup(html)
    for script in soup(['script', 'style']):
        script.decompose()
    strips = list(soup.stripped_strings)
    return strips


def get_text_and_lang(string_list: [str]) -> (str, str):
    text = ' '.join(string_list)
    blob = TextBlob(text)
    lang = blob.detect_language()
    return text, lang


def get_title_and_text(url: str) -> (str, str):
    content = trafilatura.fetch_url(url)
    content_dict = trafilatura.bare_extraction(content)
    return content_dict['title'], content_dict['text']
    # return trafilatura.extract(content, include_comments=False, with_metadata=True)


if __name__ == '__main__':
    my_url = 'https://www.tuttosport.com/news/calcio/coppa-italia/2021/05/13-81655553/' \
             'juve-atalanta_la_finale_di_coppa_italia_con_4300_spettatori'
    # content = get_url_content(my_url)
    # print(content[:10])
    # my_text, text_lang = get_text_and_lang(content)
    # print(text_lang, my_text[:150])

    title, plain_text = get_title_and_text(my_url)
    print(title)
    print(plain_text)
