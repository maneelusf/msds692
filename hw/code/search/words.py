import os
import re
import string


def filelist(root):
    """Return a fully-qualified list of filenames under root directory"""
    filelist = []
    for root, dirs, files in os.walk(root):
        for file in files:
            # append the file name to the list
            filelist.append(os.path.join(root, file))
    return filelist


def get_text(fileName):
    f = open(fileName, encoding='latin-1')
    s = f.read()
    f.close()
    return s


def words(text):
    """
    Given a string, return a list of words normalized as follows.
    Split the string to make words first by using regex compile() function
    and string.punctuation + '0-9\\r\\t\\n]' to replace all those
    char with a space character.
    Split on space to get word list.
    Ignore words < 3 char long.
    Lowercase all words
    """
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')
    nopunct = regex.sub(" ", text)  # delete stuff but leave at least a space to avoid clumping together
    words = nopunct.split(" ")
    words = [w for w in words if len(w) > 2]  # ignore a, an, to, at, be, ...
    words = [w.lower() for w in words]
    # print words
    return words


def results(docs, terms):
    """
    Given a list of fully-qualifed filenames, return an HTML file
    that displays the results and up to 2 lines from the file
    that have at least one of the search terms.
    Return at most 100 results.  Arg terms is a list of string terms.
    """
    def checklist(terms,sentence):
        a = False
        for term in terms:
            if term in sentence.lower():
                a = True
                break
        return a
    html_strings = ''
    for doc in docs:
        with open(doc,'r') as f:
            file_list = f.readlines()
            for sentence_number,sentence in enumerate(file_list):
                if checklist(terms,sentence) == True:
                    break
            if sentence_number == 0:
                html_string = file_list[0].lower() + file_list[1].lower()
            else:
                html_string = file_list[sentence_number - 1].lower() + file_list[sentence_number].lower()
            for term in terms:
                html_string = html_string.replace(term, '<b>{}</b>'.format(term))
                html_string = '''<p><a href="{}">{}</a><br>
         {}<br><br>'''.format(doc,doc,html_string)
            html_strings = html_strings + html_string
    main_string = '''<html>
    <body>
    <h2>Search results for <b>{}</b> in {} files</h2>{}   
</body>
</html>'''.format(' '.join(terms),len(docs),html_strings)
    return main_string



def filenames(docs):
    """Return just the filenames from list of fully-qualified filenames"""
    if docs is None:
        return []
    return [os.path.basename(d) for d in docs]
