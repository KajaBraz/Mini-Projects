import glob
import re
import os
from gensim.parsing.preprocessing import remove_stopwords, STOPWORDS
from gensim.utils import tokenize
from nltk.stem import PorterStemmer


def get_texts(folder_name):
    text_files = [f for f in glob.glob(folder_name + '*.txt')]
    return text_files


def read(texts_list):
    titles = []
    texts = []

    for text in texts_list:
        with open(text, encoding='utf-8-sig') as f:
            # f = open(text, encoding='utf-8-sig')
            content = re.sub(r'[^\s\w\d]', '', f.read())
            texts.append(content)
            titles.append(os.path.basename(text)[:-4])
    return titles, texts


def preprocess(texts_list):
    my_stopwords = STOPWORDS.union({'\n'})
    texts_tokens = [tokenize(text, lower=True) for text in texts_list]
    texts_no_stop = [[word for word in text if word not in my_stopwords] for text in texts_tokens]
    return texts_no_stop


def stemming(texts_list):
    porter = PorterStemmer()
    stems = [[porter.stem(token) for token in text] for text in texts_list]
    return stems


if __name__ == '__main__':
    titles_files = get_texts('books/')
    # print(titles_files)

    titles, texts = read(titles_files)
    # print(titles)
    # print(texts[0])

    texts_preprocessed = preprocess(texts)
    # print(texts_preprocessed[0])

    stemmed = stemming(texts_preprocessed)
    print(stemmed[0])
