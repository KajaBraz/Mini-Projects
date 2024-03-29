from collections import Counter

import spacy
from nltk import word_tokenize, SnowballStemmer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob
from wordcloud import WordCloud
import many_stop_words
import languages
import re
from spacy import displacy
import xx_ent_wiki_sm
import en_core_web_sm
import en_core_web_lg

import topics


def get_stopwords(language_code: str, extra_stopwords: {str}) -> {str}:
    available_languages = set(many_stop_words.available_languages)
    if language_code in available_languages:
        my_stopwords = many_stop_words.get_stop_words(language_code)
        return my_stopwords.union(extra_stopwords)


def stem_text(text: str, lang_code: str) -> [str]:
    if lang_code in languages.languages.keys():
        tokens = word_tokenize(text)
        stemmer = SnowballStemmer(languages.languages[lang_code])
        stems = [stemmer.stem(token) for token in tokens]
        return stems
    return []


def get_cloud(text: str, page_name: str, language_code: str, personalized_stopwords: {str}):
    available_languages = set(many_stop_words.available_languages)
    if language_code in available_languages:
        # my_stopwords = many_stop_words.get_stop_words(language_code)
        wordcloud = WordCloud(stopwords=personalized_stopwords, include_numbers=True, width=600, height=400).generate(
            text)
    else:
        wordcloud = WordCloud(stopwords=personalized_stopwords, include_numbers=True).generate(text)

    png_title = re.sub(r'[\W\s]+', '_', page_name)
    if png_title[-1] == '_':
        png_title = png_title[:-1]

    path = f'static/images/{png_title}.png'
    wordcloud.to_file(path)
    return path


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
        return 'balance between personal opinion and factual information'
    return 'factual information'


def get_most_frequent_words(text: str, lang_code: str, extra_stopwords: {str}, most_common_n: int) -> {str: int}:
    my_stopwords = list(get_stopwords(lang_code, extra_stopwords))
    words = text.split(' ')
    meaningful_words = [word for word in words if word not in my_stopwords]
    bow = Counter(meaningful_words)
    return bow.most_common(most_common_n)


def count_words(clear_text: str, lang_code: str, extra_stopwords: {str}) -> {str: int}:
    my_stopwords = get_stopwords(lang_code, extra_stopwords)
    stemmed_stopwords = stem_text(' '.join(my_stopwords), lang_code)
    all_words = clear_text.split(' ')
    all_unique_words = set(all_words)
    words_no_stopwords = [True for word in all_words if word not in my_stopwords]
    unique_words_no_stopwords = [True for word in all_unique_words if word not in my_stopwords]
    all_stems = stem_text(clear_text, lang_code)
    all_unique_stems = set(stem_text(clear_text, lang_code))
    stems_no_stopwords = [True for word in all_stems if word not in stemmed_stopwords]
    unique_stems_no_stopwords = [True for word in all_unique_stems if word not in stemmed_stopwords]
    counts = {'all_words': len(all_words),
              'all_unique_words': len(all_unique_words),
              'words_no_stopwords': len(words_no_stopwords),
              'unique_words_no_stopwords': len(unique_words_no_stopwords),
              'all_stems': len(all_stems),
              'all_unique_stems': len(all_unique_stems),
              'stems_no_stopwords': len(stems_no_stopwords),
              'unique_stems_no_stopwords': len(unique_stems_no_stopwords)}
    return counts


def get_and_save_ner(unprocessed_text: str, lang_code: str, doc_title: str):
    if lang_code == 'en':
        nlp = en_core_web_sm.load()
    else:
        nlp = xx_ent_wiki_sm.load()
    doc = nlp(unprocessed_text)
    entity_label_pairs = [(x.text, x.label_) for x in doc.ents]
    label_counts = Counter([x.label_ for x in doc.ents])

    html_title = re.sub(r'[\W\s]', '_', doc_title)
    if html_title[-1] == '_':
        html_title = html_title[:-1]
    html_title = f'static/labelled_texts/html_{html_title}.html'
    # displacy.serve(doc, style='ent')
    ner_text = displacy.render(doc, style='ent')
    with open(html_title, 'w', encoding='utf-8') as html_file:
        html_file.write(ner_text)

    return entity_label_pairs, label_counts, ner_text, html_title


def discover_topics(n: int, lang_code: str, extra_stopwords: {}, text: str):
    # TODO change the algorithm as now it takes very long to obtain the results
    """
        Function that calculates similarity of words used in the given text with the provided topics
    :param n: the number of topics
    :param lang_code:
    :param extra_stopwords:
    :param text: text without noise
    :return: list of tuples:
        1st element - topic, cumulative score of top 5 words
        2nd element - 5 most relevant words for a given topic
    """
    if lang_code == 'en':
        nlp = spacy.load('en_core_web_lg')
        tokens = set(nlp(text))

        similarity_results = {}
        similarity_pairs = {}
        for topic in topics.topics:
            similarity_results[topic] = {}
            nlp_topic = nlp(topic)
            for token in tokens:
                similarity_results[topic][token] = nlp_topic.similarity(token)
            most_similar_tokens = sorted(similarity_results[topic].items(), key=lambda item: item[1], reverse=True)[:5]
            top_5_similarity_sum = sum([similarity[1] for similarity in most_similar_tokens])
            similarity_pairs[(topic, top_5_similarity_sum)] = [similarity[0] for similarity in most_similar_tokens]

        most_similar = sorted(similarity_pairs.items(), key=lambda item: item[0][1], reverse=True)[:n]
        return most_similar
    return 'supported only for English'
