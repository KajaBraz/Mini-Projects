from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
import numpy as np


def calculate_tf_idf(texts: [str]):
    vectorizer = CountVectorizer()
    counts = vectorizer.fit_transform(texts)
    transformer = TfidfTransformer(norm=None)
    tfidf_scores_transformed = transformer.fit_transform(counts)
    return tfidf_scores_transformed


def calculate_tf_idf2(texts: [str]):
    vectorizer = TfidfVectorizer(norm=None)
    tfidf_scores = vectorizer.fit_transform(texts)
    return tfidf_scores


def check_tfidf_similarity(scores1, scores2):
    if np.allclose(scores1.todense(), scores2.todense()):
        return True
    return False


if __name__ == '__main__':
    pass
