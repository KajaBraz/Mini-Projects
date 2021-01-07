from collections import Counter
from prepare_chunks import read_text, pos_tagging, word_sentence_tokenize, syntax_parsing


def chunk_counter(chunked_sentences, pos, num_most_common):
    chunks = [tuple(subtree) for sentence in chunked_sentences for subtree in
              sentence.subtrees(filter=lambda t: t.label() == pos)]
    chunks_counter = Counter()
    for chunk in list(chunks):
        chunks_counter[chunk] += 1
    return chunks_counter.most_common(num_most_common)


if __name__ == '__main__':
    dorian_gray = read_text('texts/dorian_gray.txt')
    pos_tagged = pos_tagging(word_sentence_tokenize(dorian_gray))
    parsed_np, parsed_vp = syntax_parsing(pos_tagged)
    most_common_np_chunks = chunk_counter(parsed_np, 'NP', 20)
    most_common_vp_chunks = chunk_counter(parsed_vp, 'VP', 20)
    print(most_common_np_chunks)
    print(most_common_vp_chunks)
