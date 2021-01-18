from articles_texts import articles
from preprocessing import prepare_data
from tf_idf_score import calculate_tf_idf, calculate_tf_idf2, check_tfidf_similarity, print_results


def run(texts):
    preprocessed = [prepare_data(text) for text in texts]
    tfidf_scores_transformed = calculate_tf_idf(preprocessed)
    tfidf_scores = calculate_tf_idf2(preprocessed)
    print('Are the two tf-idf scores the same?', check_tfidf_similarity(tfidf_scores_transformed[0], tfidf_scores[0]))
    print_results(tfidf_scores[0], tfidf_scores[1], len(preprocessed))
    print('-----------------------------------')
    print_results(tfidf_scores_transformed[0], tfidf_scores_transformed[1], len(preprocessed))


if __name__ == '__main__':
    run(articles)
