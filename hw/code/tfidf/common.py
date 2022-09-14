from tfidf import *
import sys
from collections import Counter


filename = sys.argv[1]
with open(filename,'r') as f:
    xmlstring = f.read()
xmltext = gettext(xmlstring)
tokens = tokenize(xmltext)
tokens = stemwords(tokens)
tokens = Counter(tokens).most_common(10)
for token in tokens:
    print(token[0],round(token[1],3))
