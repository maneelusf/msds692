import sys

import nltk
from nltk.stem.porter import *
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import xml.etree.cElementTree as ET
from collections import Counter
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import zipfile
import os
import numpy as np

def gettext(xmltext) -> str:
    """
    Parse xmltext and return the text from <title> and <text> tags
    """


    # ensure there are no weird char
    xmltext = xmltext.encode('ascii', 'ignore')
    tree = ET.fromstring(xmltext)
    title_string = []
    text_string = []
    for i in tree.iterfind('title'):
        title_string.append(i.text)
    for i in tree.iterfind('.//text/*'):
        text_string.append(i.text)
    title_string = ' '.join(title_string)
    text_string = ' '.join(text_string)
    final_string = title_string + ' ' + text_string
    return final_string


def tokenize(text) -> list:
    """
    Tokenize text and return a non-unique list of tokenized words
    found in the text. Normalize to lowercase, strip punctuation,
    remove stop words, drop words of length < 3, strip digits.
    """
    text = text.lower()
    text = re.sub('[' + string.punctuation + '0-9\\r\\t\\n]', ' ', text)
    tokens = nltk.word_tokenize(text)
    tokens = [w for w in tokens if len(w) > 2]  # ignore a, an, to, at, be, ...
    tokens = [w for w in tokens if w not in ENGLISH_STOP_WORDS]
    return tokens
    ...


def stemwords(words) -> list:
    """
    Given a list of tokens/words, return a new list with each word
    stemmed using a PorterStemmer.
    """
    stemmer = PorterStemmer()
    words = [stemmer.stem(plural) for plural in words]
    return words


def tokenizer(text) -> list:
    return stemwords(tokenize(text))


def compute_tfidf(corpus:dict) -> TfidfVectorizer:
    """
    Create and return a TfidfVectorizer object after training it on
    the list of articles pulled from the corpus dictionary. Meaning,
    call fit() on the list of document strings, which figures out
    all the inverse document frequencies (IDF) for use later by
    the transform() function. The corpus argument is a dictionary
    mapping file name to xml text.
    """

    documents = list(corpus.values())
    tfidf = TfidfVectorizer(input='content',
                            analyzer='word',
                            preprocessor=gettext,
                            tokenizer=tokenizer,
                            stop_words='english', # even more stop words
                            decode_error = 'ignore')
    tfidf = tfidf.fit(documents)
    return tfidf




def summarize(tfidf:TfidfVectorizer, text:str, n:int):
    """
    Given a trained TfidfVectorizer object and some XML text, return
    up to n (word,score) pairs in a list. Discard any terms with
    scores < 0.09. Sort the (word,score) pairs by TFIDF score in reverse order.
    """
    X = tfidf.transform([text]).toarray()
    indexes = np.nonzero(X)[1]

    list1 = [(tfidf.get_feature_names_out()[i],X[:,i][0]) for i in indexes if X[:,i][0]>=0.09]
    list1.sort(key = lambda x: (x[1],x[0]),reverse = True)
    return list1[:n]

def load_corpus(zipfilename:str) -> dict:
    """
    Given a zip file containing root directory reuters-vol1-disk1-subset
    and a bunch of *.xml files, read them from the zip file into
    a dictionary of (filename,xmltext) associations. Use namelist() from
    ZipFile object to get list of xml files in that zip file.
    Convert filename reuters-vol1-disk1-subset/foo.xml to foo.xml
    as the keys in the dictionary. The values in the dictionary are the
    raw XML text from the various files.
    """
    dict1 = {}
    with zipfile.ZipFile(zipfilename, 'r') as f:
        names = f.namelist()
        for name in names[1:]:
            dict1[name.split('/')[1]] = f.read(name)
    return dict1




