from tfidf import *
import sys
from collections import Counter


filename = sys.argv[1]
xmltext = gettext(filename)
tokens = tokenize(xmltext)
tokens = stemwords(tokens)
tokens = Counter(tokens).most_common(10)
for token in tokens:
    print(token[0],token[1])
