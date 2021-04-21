from prepare_chunks import read_text, pos_tagging, word_sentence_tokenize, syntax_parsing, get_wordcloud
from get_most_common_chunks import chunk_counter
import os


def get_insight(path):
    text = read_text(path)
    pos_tagged = pos_tagging(word_sentence_tokenize(text))
    parsed_np, parsed_vp = syntax_parsing(pos_tagged)
    most_common_np_chunks = chunk_counter(parsed_np, 'NP', 30)
    most_common_vp_chunks = chunk_counter(parsed_vp, 'VP', 30)
    print(os.path.basename(path).rsplit('.')[0])
    print('NOUN PHRASE')
    print(most_common_np_chunks)
    print('VERB PHRASE')
    print(most_common_vp_chunks)
    print()


if __name__ == '__main__':
    texts = ['texts/dorian_gray.txt', 'texts/pinocchio.txt', 'texts/the_iliad.txt', 'texts/frankenstein.txt']
    for title in texts:
        get_insight(title)
        get_wordcloud(title)
