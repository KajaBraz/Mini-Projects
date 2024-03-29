from pprint import pprint

import prepare_url_text
import text_analysis


def get_details(my_url: str, desired_collocations: [str] = None, extra_stopwords: {} = None):
    text_insight = {}
    url_data = prepare_url_text.get_url_components(my_url)
    text_components = prepare_url_text.get_main_content(url_data)
    unprocessed_text = '.'.join(text_components)
    clean_text = prepare_url_text.remove_noise(unprocessed_text)

    if desired_collocations is None:
        desired_collocations = []

    my_text = prepare_url_text.add_personalized_collocations(desired_collocations, clean_text)
    lang = prepare_url_text.get_language(my_text)
    print(lang)
    print(my_text)
    # text_insight['text']=my_text
    text_insight['language'] = lang

    if extra_stopwords is None:
        extra_stopwords = {}

    personalized_stopwords = text_analysis.get_stopwords(lang, extra_stopwords)
    website, title = prepare_url_text.get_website_name_and_title(url_data)
    cloud_path = text_analysis.get_cloud(my_text, title, lang, personalized_stopwords)
    text_insight['website'] = website
    text_insight['title'] = title
    text_insight['cloud'] = cloud_path

    text_polarity, text_subjectivity = text_analysis.get_sentiment_scores(my_text)
    print('text_polarity:', text_polarity, '; text_subjectivity:', text_subjectivity)
    text_insight['text_polarity'] = text_polarity
    text_insight['text_subjectivity'] = text_subjectivity

    sentiment = text_analysis.analyze_sentiment(text_polarity)
    print('detected sentiment: ', sentiment)
    text_insight['sentiment'] = sentiment

    subjectivity_level = text_analysis.analyze_subjectivity(text_subjectivity)
    print(subjectivity_level)
    text_insight['subjectivity_level'] = subjectivity_level

    most_common = text_analysis.get_most_frequent_words(my_text, lang, personalized_stopwords, 10)
    print('most common words:')
    pprint(most_common)
    text_insight['most_common'] = most_common

    word_counts = text_analysis.count_words(my_text, lang, personalized_stopwords)
    pprint(word_counts)
    text_insight['word_counts'] = word_counts

    stems = text_analysis.stem_text(my_text, lang)

    ner_pairs, label_counts, ner_text, html_path = text_analysis.get_and_save_ner(unprocessed_text, lang,
                                                                                  text_components[0])
    pprint(ner_pairs[:10])
    pprint(label_counts.most_common(5))
    text_insight['ner_pairs'] = ner_pairs
    text_insight['label_counts'] = label_counts
    text_insight['ner_text'] = ner_text
    text_insight['html_path'] = html_path

    discovered_topics = text_analysis.discover_topics(10, lang, personalized_stopwords, my_text)
    text_insight['topics'] = discovered_topics
    print('topics')
    pprint(discovered_topics)

    return text_insight


if __name__ == '__main__':
    get_details('https://www.tuttosport.com/news/calcio/coppa-italia/2021/05/13-81655553/'
                'juve-atalanta_la_finale_di_coppa_italia_con_4300_spettatori',
                ['serie a', 'coppa italia', 'reggio emilia', 'foro italico'], {'siervo', 'tennis', 'tratta'})
    print('------------------------------------------------------------')
    get_details('https://www.bbc.com/news/world-europe-56222992')
    print('------------------------------------------------------------')
    get_details(
        'https://www.rainews.it/dl/rainews/media/Genova-Nasce-la-Casa-dei-cantautori-'
        'Il-ricordo-di-Battiato-a188cae5-de09-4367-96d7-93b697b2ff6a.html#foto-1',
        None, {'parte'})
    print('------------------------------------------------------------')
    get_details('https://podroze.onet.pl/aktualnosci/wlochy-emilia-romania-przygotowana-na-sezon-turystyczny/894hnk6',
                ['Emilia Romania'])
    print('------------------------------------------------------------')
    get_details(
        'https://www.gazzetta.it/Calcio/Serie-A/Juventus/25-05-2021/partita-del-cuore-diretta-live-4101331690263.shtml',
        None, {'serie a'})
    print('------------------------------------------------------------')
    get_details('https://thevision.com/innovazione/italia-programmatori-donne/')
