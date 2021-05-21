from collections import Counter

from nltk import word_tokenize, SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob
from wordcloud import WordCloud
import many_stop_words

import languages
import prepare_url_text


def get_stopwords(language_code: str, extra_stopwords: {str}) -> {str}:
    available_languages = set(many_stop_words.available_languages)
    if language_code in available_languages:
        my_stopwords = many_stop_words.get_stop_words(language_code)
        return my_stopwords.union(extra_stopwords)


def stem_text(text: str, lang_code: str) -> [str]:
    tokens = word_tokenize(text)
    stemmer = SnowballStemmer(languages.languages[lang_code])
    stems = [stemmer.stem(token) for token in tokens]
    return stems


def get_cloud(text: str, page_name: str, language_code: str, personalized_stopwords: {str}):
    available_languages = set(many_stop_words.available_languages)
    if language_code in available_languages:
        # my_stopwords = many_stop_words.get_stop_words(language_code)
        wordcloud = WordCloud(stopwords=personalized_stopwords, include_numbers=True).generate(
            text)
    else:
        wordcloud = WordCloud(stopwords=personalized_stopwords, include_numbers=True).generate(text)
    wordcloud.to_file(page_name.replace(' ', '_') + '_' + 'cloud.png')


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


def get_most_frequent_words(text: str, lang_code: str, extra_stopwords: {str}, most_common_n: int) -> {str: int}:
    my_stopwords = list(get_stopwords(lang_code, extra_stopwords))
    words = text.split(' ')
    meaningful_words = [word for word in words if word not in my_stopwords]
    bow = Counter(meaningful_words)
    return bow.most_common(most_common_n)


def count_words(clear_text: str, lang_code: str, extra_stopwords: {str}) -> {str: int}:
    my_stopwords = get_stopwords(lang_code, extra_stopwords)
    all_words = clear_text.split(' ')
    all_unique_words = set(all_words)
    words_no_stopwords = [True for word in all_words if word not in my_stopwords]
    unique_words_no_stopwords = [True for word in all_unique_words if word not in my_stopwords]
    unique_stems = set(stem_text(clear_text, lang_code))
    counts = {'all_words': len(all_words), 'all_unique_words': len(all_unique_words),
              'words_no_stopwords': len(words_no_stopwords),
              'unique_words_no_stopwords': len(unique_words_no_stopwords),
              'unique_stems': len(unique_stems)}
    return counts


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
    # print(lang, my_text)
    # website = prepare_url_text.get_website_name(url_data)
    # # get_cloud(my_text, website, lang)
    # text_polarity, text_subjectivity = get_sentiment_scores(my_text)
    # print(text_polarity, text_subjectivity)
    # sentiment = analyze_sentiment(text_polarity)
    # print(sentiment)
    # subjectivity_level = analyze_subjectivity(text_subjectivity)
    # print(subjectivity_level)
    get_most_frequent_words(my_text, lang, {'siervo', 'tennis', 'tratta'}, 10)
