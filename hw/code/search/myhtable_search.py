# Got slate magazine data from http://www.anc.org/data/oanc/contents/
# rm'd .xml, .anc files, leaving just .txt
# 4534 files in like 55 subdirs

from htable import *
from words import get_text, words

def myhtable_create_index(files):
    """
    Build an index from word to set of document indexes
    This does the exact same thing as create_index() except that it uses
    your htable.  As a number of htable buckets, use 4011.
    Returns a list-of-buckets hashtable representation.
    """
    nbuckets = 4011
    table = htable(nbuckets)
    for file_number,file in enumerate(files):
        result = set(words(get_text(file)))
        for word in result:
            file_name_list = htable_get(table, word)

            if file_name_list!=None:
                if file_name_list!= file_name_list.union({file_number}):
                    htable_put(table, word, file_name_list.union({file_number}))
            else:
                htable_put(table,word,{file_number})

    return table



def myhtable_index_search(files, index, terms):
    """
    This does the exact same thing as index_search() except that it uses your htable.
    I.e., use htable_get(index, w) not index[w].
    """
    file_list = []
    for term in terms:
        file_name_list = htable_get(index, term)
        if file_name_list!=None:
            file_list.append(file_name_list)
    if file_list != []:
        file_list = set.intersection(*file_list)
        a = [files[file] for file in list(file_list)]
    else:
        a = []

    return a


