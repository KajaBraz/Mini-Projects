from nltk.tokenize import PunktSentenceTokenizer, word_tokenize
from nltk import pos_tag, RegexpParser


def read_text(path) -> str:
    return open(path, encoding='utf-8').read()


def word_sentence_tokenize(text: str) -> [[str]]:
    text = text.lower()
    sentence_tokenizer = PunktSentenceTokenizer(text)
    sentences_tokenized = sentence_tokenizer.tokenize(text)
    words_tokenized = [word_tokenize(sentence) for sentence in sentences_tokenized]
    return words_tokenized


def pos_tagging(tokenized: [[str]]) -> [[(str)]]:
    pos_tagged_text = [pos_tag(sentence) for sentence in tokenized]
    return pos_tagged_text


def syntax_parsing(pos_tagged):
    np_chunk_grammar = 'NP: {<DT>?<JJ>*<NN>}'
    vp_chunk_grammar = 'VP: {<DT>?<JJ>*<NN><VB.*><RB.?>?}'
    # <VB.*> matches VB->present tense, VBD->past tense, VBN->past participle
    # <RB.?> matches any form of adverb: regular RB, comparative RBR, superlative RBS

    np_chunk_parser = RegexpParser(np_chunk_grammar)
    vp_chunk_parser = RegexpParser(vp_chunk_grammar)

    np_chunked_text = [np_chunk_parser.parse(sentence) for sentence in pos_tagged]
    vp_chunked_text = [vp_chunk_parser.parse(sentence) for sentence in pos_tagged]

    return np_chunked_text, vp_chunked_text
