from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
import numpy as np
import pandas as pd


def calculate_tf_idf(texts: [str]):
    vectorizer = CountVectorizer()
    counts = vectorizer.fit_transform(texts)
    transformer = TfidfTransformer(norm=None)
    tfidf_scores_transformed = transformer.fit_transform(counts)
    names = vectorizer.get_feature_names()
    return tfidf_scores_transformed, names


def calculate_tf_idf2(texts: [str]):
    vectorizer = TfidfVectorizer(norm=None)
    tfidf_scores = vectorizer.fit_transform(texts)
    names = vectorizer.get_feature_names()
    return tfidf_scores, names


def check_tfidf_similarity(scores1, scores2):
    if np.allclose(scores1.todense(), scores2.todense()):
        return True
    return False


def print_results(scores, feature_names, texts_num):
    column_names = [f'Text n.{x}' for x in range(1, texts_num + 1)]
    df = pd.DataFrame(scores.T.todense(), index=feature_names, columns=column_names)
    for text_num in range(1, texts_num + 1):
        print(df[[f'Text n.{text_num}']].idxmax())


if __name__ == '__main__':
    pass
