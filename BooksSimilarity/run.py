from prepare_texts import get_texts, read, preprocess, stemming
from words_occurrences import get_dict, bows, most_common


def discover_similar_books():
    titles_files = get_texts('books/')
    # print(titles_files)

    titles, texts = read(titles_files)
    # print(titles)
    # print(texts[0])

    texts_preprocessed = preprocess(texts)
    # print(texts_preprocessed[0])

    stemmed = stemming(texts_preprocessed)
    # print(stemmed[0])

    stems_dict = get_dict(stemmed)
    # print(stems_dict)

    bags_of_words = bows(stems_dict, stemmed)
    # print(bags_of_words[0])

    df = most_common(0, bags_of_words, stemmed)
    print(df)


if __name__ == '__main__':
    discover_similar_books()
