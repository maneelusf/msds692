from collections import defaultdict  # https://docs.python.org/2/library/collections.html

from words import get_text, words


def create_index(files):
    """
    Given a list of fully-qualified filenames, build an index from word
    to set of document IDs. A document ID is just the index into the
    files parameter (indexed from 0) to get the file name. Make sure that
    you are mapping a word to a set of doc IDs, not a list.
    For each word w in file i, add i to the set of document IDs containing w
    Return a dict object mapping a word to a set of doc IDs.
    """
    dictionary = {}
    for file_number,file in enumerate(files):
        result = set(words(get_text(file)))
        for word in result:
            if word in dictionary.keys():
                dictionary[word].extend([file_number])
            else:
                dictionary[word] = [file_number]
    return dictionary
        #result.extend(words(get_text(file)))




def index_search(files, index, terms):
    """
    Given an index and a list of fully-qualified filenames, return a list of
    filenames whose file contents has all words in terms parameter as normalized
    by your words() function.  Parameter terms is a list of strings.
    You can only use the index to find matching files; you cannot open the files
    and look inside.
    """
    file_list = []
    for term in terms:
        if term in index.keys():
            file_list.append(set(index[term]))
    if len(file_list)>0:
        file_list = set.intersection(*file_list)
        a = [files[file] for file in list(file_list)]
    else:
        a = None
    return a