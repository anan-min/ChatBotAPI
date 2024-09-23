from pythainlp import word_tokenize
from collections import Counter
def count_thai_words(text):
    tokens = word_tokenize(text, engine='newmm')
    word_count = Counter(tokens)
    return len(word_count)
