from tfidf import *
import pandas as pd

zipfilename = sys.argv[1]
#summarizefile = sys.argv[2]



tfidf = TfidfVectorizer(input='content',
                        analyzer='word',
                        preprocessor=gettext,
                        tokenizer=tokenizer,
                        stop_words='english', # even more stop words
                        decode_error = 'ignore')
X = tfidf.fit_transform([zipfilename])
dict1 = {}
for tag,score in zip(tfidf.get_feature_names(),X.toarray()[0]):
    dict1[tag] = score
dict1 = {k: v for k, v in sorted(dict1.items(), key=lambda item: item[1],reverse = True)}
import pdb;pdb.set_trace()


...
