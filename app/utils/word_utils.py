from pythainlp import word_tokenize
from collections import Counter
import re

def count_thai_words(text):
    tokens = word_tokenize(text, engine='newmm')
    word_count = Counter(tokens)
    return len(word_count)

def is_thai_text(text):
    """Check if the text contains Thai characters"""
    thai_pattern = re.compile(r'[\u0E00-\u0E7F]')
    return bool(thai_pattern.search(text))

def detect_language(text):
    """Detect if text is Thai or English"""
    if is_thai_text(text):
        return 'th'
    else:
        return 'en'
