from collections import Counter


def chunk_counter(chunked_sentences, pos, num_most_common):
    chunks = [tuple(subtree) for sentence in chunked_sentences for subtree in
              sentence.subtrees(filter=lambda t: t.label() == pos)]
    chunks_counter = Counter()
    for chunk in list(chunks):
        chunks_counter[chunk] += 1
    return chunks_counter.most_common(num_most_common)
