import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

def clean_text(text, all_mentions):
    # If retweet, delete RT and name of the account
    text = re.sub('(RT\s.*):', '', text)
    # Find all links and delete them
    all_links = re.findall('(https:.*?)\s', text + ' ')
    for i in all_links:
        text = text.replace(i, '')
    for i in all_mentions:
        text = text.replace('@' + i, '')
    # Tokens
    tokens = word_tokenize(text.replace('-', ' '))
    # convert to lower case
    tokens = [w.lower() for w in tokens ]
    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    phrase = " ".join(words)
    return phrase, all_links