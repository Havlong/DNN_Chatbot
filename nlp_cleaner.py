import nltk

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
stop_tokens = ['!', '?', ',', '.', ':', ';', '-', '_']


def tokenize(message):
    return word_tokenize(message)


def process_token(token):
    return lemmatizer.lemmatize(token.lower())


def clean_up_tokens(tokens):
    return [process_token(token) for token in tokens if token not in stop_tokens]


def clean_up_sentence(message):
    sentence_words = tokenize(message)
    sentence_words = list(map(process_token, sentence_words))
    return sentence_words
