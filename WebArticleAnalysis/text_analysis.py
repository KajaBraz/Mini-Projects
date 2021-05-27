import re
from pprint import pprint
from collections import Counter
from nltk import word_tokenize, SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from spacy.kb import Path
from textblob import TextBlob
from wordcloud import WordCloud
import many_stop_words
import languages
import spacy
import xx_ent_wiki_sm
import en_core_web_sm


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
    return {}


def get_cloud(text: str, page_name: str, language_code: str, personalized_stopwords: {str}):
    available_languages = set(many_stop_words.available_languages)
    if language_code in available_languages:
        # my_stopwords = many_stop_words.get_stop_words(language_code)
        wordcloud = WordCloud(stopwords=personalized_stopwords, include_numbers=True).generate(
            text)
    else:
        wordcloud = WordCloud(stopwords=personalized_stopwords, include_numbers=True).generate(text)

    png_title = re.sub(r'[\W\s]', '_', page_name)
    if png_title[-1] == '_':
        png_title = png_title[:-1]

    path = 'cloud_' + png_title + '.png'
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
    # ner_text = spacy.displacy.serve(doc, style='ent')
    ner_text = spacy.displacy.render(doc, style='ent')
    with open(f'html_{html_title}.html', 'w', encoding='utf-8') as html_file:
        html_file.write(ner_text)

    return entity_label_pairs, label_counts
