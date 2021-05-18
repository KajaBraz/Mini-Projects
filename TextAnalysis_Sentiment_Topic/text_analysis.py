from textblob import TextBlob
from wordcloud import WordCloud
import many_stop_words

import prepare_url_text


def get_cloud(text: str, page_name: str, language_code: str = ''):
    available_languages = set(many_stop_words.available_languages)
    if language_code in available_languages:
        wordcloud = WordCloud(stopwords=many_stop_words.get_stop_words(language_code), include_numbers=True).generate(
            text)
    else:
        wordcloud = WordCloud(include_numbers=True).generate(text)
    wordcloud.to_file(page_name + '_' + 'cloud.png')


def get_sentiment_scores(text: str) -> (float, float):
    polarity, subjectivity = TextBlob(text).sentiment
    return polarity, subjectivity


def analyze_sentiment(polarity: float) -> str:
    if polarity <= -0.5:
        return 'negative'
    elif -0.5 < polarity < -0.15:
        return 'slightly negative'
    elif -0.15 <= polarity <= 0.15:
        return 'neutral'
    elif 0.15 < polarity < 0.5:
        return 'slightly positive'
    return 'positive'


def analyze_subjectivity(subjectivity: float) -> str:
    if subjectivity >= 0.66:
        return 'personal opinion'
    elif 0.66 > subjectivity > 0.33:
        return 'equilibrium between personal opinion and factual information'
    return 'factual information'


if __name__ == '__main__':
    my_url = 'https://www.tuttosport.com/news/calcio/coppa-italia/2021/05/13-81655553/' \
             'juve-atalanta_la_finale_di_coppa_italia_con_4300_spettatori'
    # content = prepare_url_text.get_url_content(my_url)
    # my_text, text_lang = prepare_url_text.get_text_and_lang(content)
    url_data = prepare_url_text.get_url_components(my_url)
    text_components = prepare_url_text.get_main_content(url_data)
    clean_text = prepare_url_text.remove_noise(' '.join(text_components))
    collocations_to_consider = ['serie a', 'coppa italia', 'reggio emilia', 'foro italico']
    my_text = prepare_url_text.add_personalized_collocations(collocations_to_consider, clean_text)
    lang = prepare_url_text.get_language(my_text)
    print(lang, my_text)
    website = prepare_url_text.get_website_name(url_data)
    get_cloud(my_text, website, lang)
    text_polarity, text_subjectivity = get_sentiment_scores(my_text)
    print(text_polarity, text_subjectivity)
    sentiment = analyze_sentiment(text_polarity)
    print(sentiment)
    subjectivity_level = analyze_subjectivity(text_subjectivity)
    print(subjectivity_level)
