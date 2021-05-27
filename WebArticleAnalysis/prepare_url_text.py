from bs4 import BeautifulSoup
from urllib import request
from textblob import TextBlob

import re
import trafilatura


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


def get_url_components(url: str) -> dict:
    content = trafilatura.fetch_url(url)
    return trafilatura.bare_extraction(content)
    # return trafilatura.extract(content, include_comments=False, with_metadata=True)


def get_main_content(url_components: dict) -> (str, str, str):
    return url_components['title'], url_components['description'], url_components['text']


def get_language(text: str) -> str:
    return TextBlob(text).detect_language()


def remove_noise(text: str) -> str:
    no_special_chars = re.sub(r'[^\w%€$]', ' ', text.lower().strip())
    return re.sub(r'\s\s+', ' ', no_special_chars)


def add_personalized_collocations(collocation_list: [str], text: str) -> str:
    text_updated = text
    for collocation in collocation_list:
        joined = collocation.lower().replace(' ', '_')
        text_updated = text_updated.replace(collocation.lower(), joined)
    return text_updated


def get_website_name_and_title(url_components: dict) -> (str, str):
    return url_components['sitename'], url_components['title']
