from wordcloud import WordCloud
import many_stop_words

import prepare_url_text


def get_cloud(text: str, language_code: str = ''):
    available_languages = set(many_stop_words.available_languages)
    if language_code in available_languages:
        wordcloud = WordCloud(stopwords=many_stop_words.get_stop_words(language_code)).generate(text)
    else:
        wordcloud = WordCloud().generate(text)
    wordcloud.to_file('cloud.png')


if __name__ == '__main__':
    url = prepare_url_text.get_url_content(
        'https://www.tuttosport.com/news/calcio/coppa-italia/2021/05/13-81655553/'
        'juve-atalanta_la_finale_di_coppa_italia_con_4300_spettatori')
    text = prepare_url_text.get_text(url)
    get_cloud(text, 'it')
