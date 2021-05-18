import prepare_url_text
import text_analysis


def get_details(my_url: str, desired_collocations: [str]):
    url_data = prepare_url_text.get_url_components(my_url)
    text_components = prepare_url_text.get_main_content(url_data)
    clean_text = prepare_url_text.remove_noise(' '.join(text_components))
    my_text = prepare_url_text.add_personalized_collocations(desired_collocations, clean_text)
    lang = prepare_url_text.get_language(my_text)
    print(lang)
    print(my_text)
    website = prepare_url_text.get_website_name(url_data)
    text_analysis.get_cloud(my_text, website, lang)
    text_polarity, text_subjectivity = text_analysis.get_sentiment_scores(my_text)
    print('text_polarity:', text_polarity, '; text_subjectivity:', text_subjectivity)
    sentiment = text_analysis.analyze_sentiment(text_polarity)
    print(sentiment)
    subjectivity_level = text_analysis.analyze_subjectivity(text_subjectivity)
    print(subjectivity_level)


if __name__ == '__main__':
    get_details('https://www.tuttosport.com/news/calcio/coppa-italia/2021/05/13-81655553/'
                'juve-atalanta_la_finale_di_coppa_italia_con_4300_spettatori',
                ['serie a', 'coppa italia', 'reggio emilia', 'foro italico'])
    print('------------------------------------------------------------')
    get_details('https://www.bbc.com/news/world-europe-56222992', [])
    print('------------------------------------------------------------')
    get_details(
        'https://www.rainews.it/dl/rainews/media/Genova-Nasce-la-Casa-dei-cantautori-'
        'Il-ricordo-di-Battiato-a188cae5-de09-4367-96d7-93b697b2ff6a.html#foto-1', [])
    print('------------------------------------------------------------')
    get_details('https://podroze.onet.pl/aktualnosci/wlochy-emilia-romania-przygotowana-na-sezon-turystyczny/894hnk6',
                ['Emilia Romania'])
