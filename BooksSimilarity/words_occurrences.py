from gensim import corpora
import pandas as pd


def get_dict(word_list):
    d = corpora.Dictionary(word_list)
    return d


def bows(dict, word_list):
    bag_of_words = [dict.doc2bow(w) for w in word_list]
    return bag_of_words


def most_common(book_ind, bag_of_words, stems):
    labels = ['ind', 'occurences']
    occurences = pd.DataFrame(bag_of_words[book_ind], columns=labels)
    tokens = [stems[book_ind][i] for i in occurences.ind]
    occurences.insert(2, 'tokens', tokens)
    occ_sorted = occurences.sort_values(by=['occurences'], ascending=False, inplace=False)
    return occ_sorted
