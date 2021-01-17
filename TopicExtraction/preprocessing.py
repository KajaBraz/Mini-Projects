from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from collections import Counter
import re


def part_of_speech(word):
    synonyms = wordnet.synsets(word)
    pos_count = Counter()
    for pos in ['n', 'v', 'a', 'r']:
        pos_count[pos] = len([synonym for synonym in synonyms if synonym.pos() == pos])

    return pos_count.most_common(1)[0][0]


def prepare_data(s: str) -> str:
    stop_words = stopwords.words('english')
    normalizer = WordNetLemmatizer()
    no_punctuation = re.sub(r'\W+', ' ', s).lower()
    normalized = [normalizer.lemmatize(token, part_of_speech(token)) for token in word_tokenize(no_punctuation)]
    text_no_stop_words = ' '.join([word for word in normalized if word not in stop_words])
    return text_no_stop_words


if __name__ == '__main__':
    print(prepare_data('It is a test string. Checking...'))
