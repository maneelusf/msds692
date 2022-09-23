# Recommending Articles

*All projects in this class are individual projects, not group projects.  You may not look at or discuss code with others until after you have submitted your own individual effort.*

The goal of this project is to learn how to make a simple article recommendation engine using a semi-recent advance in natural language processing called [word2vec](http://arxiv.org/pdf/1301.3781.pdf) (or just *word vectors*). In particular, we're going to use a "database" from [Stanford's GloVe project](https://nlp.stanford.edu/projects/glove/) trained on a dump of Wikipedia. The project involves reading in a database of word vectors and a corpus of text articles then organizing them into a handy table (list of lists) for processing.

Around the recommendation engine, you are going to build a web server that displays a list of [BBC](http://mlg.ucd.ie/datasets/bbc.html) articles for URL `http://localhost:5000` (testing) or whatever the IP address is of your Amazon server (deployment):

<img src=figures/articles.png width=200>

Clicking on one of those articles takes you to an article page that shows the text of the article as well as a list of five recommended articles:

<img src=figures/article1.png width=450>

<img src=figures/article2.png width=450>

You will do your work in `recommender-`*userid*.

## Discussion

### Article word-vector centroids

Those of you who were not in the [MSDS501 computational boot camp](https://github.com/USFCA-MSDS/msds501) should read the project description [Word similarity and relationships](https://github.com/USFCA-MSDS/msds501/blob/master/projects/wordsim.md). The document explains word vectors enough to complete this project.

In a nutshell, each word has a vector of, say, 300 floating-point numbers that somehow capture the meaning of the word, at least as it relates to other words within a corpus. These vectors are derived from a neural network that learns to map a word to an output vector such that neighboring words in some large corpus are close in 300-space. ("The main intuition underlying the model is the simple observation that ratios of word-word co-occurrence probabilities have the potential for encoding some form of meaning." see [GloVe project](https://nlp.stanford.edu/projects/glove/).)

Two words are related if their word vectors are close in 300 space. Similarly, if we compute the centroid of a document's cloud of word vectors, related articles should have centroids close in 300 space. Words that appear frequently in a document push the centroid in the direction of that word's vector. The centroid is just the sum of the vectors divided by the number of words in the article. Given an article, we can compute the distance from its centroid to every other article's centroid. The article centroids closest to the article of interest's centroid are the most similar articles. Surprisingly, this simple technique works well as you can see from the examples above.

Given a word vector filename, such as `glove.6B.300d.txt`, and the root directory of the BBC article corpus, we will use the following functions from `doc2vec.py` in the main `server.py` file to load them into memory. Finding the glove and articles arguments is trickier than usual because we are launching the Web server using gunicorn. For example:

```
gunicorn -D --threads 4 -b 0.0.0.0:5000 --access-logfile server.log --timeout 60 server:app glove.6B.300d.txt bbc
```

To find `glove.6B.300d.txt` and `bbc`, we look at just after the `server:app` argument:

```python
# get commandline arguments
i = sys.argv.index('server:app') # find out where arguments start
glove_filename = sys.argv[i+1]
articles_dirname = sys.argv[i+2]

gloves = load_glove(glove_filename)
articles = load_articles(articles_dirname, gloves)
```

The `gloves` variable is the dictionary mapping a word to its 300-vector vector. The `articles` is a list of records, one for each article. An article record is just a list containing the fully-qualified file name, the article title, the text without the title, and the word vector computed from the text without the title.

Then to get the list of most relevant five articles, we'll do this:

```python
seealso = recommended(doc, articles, 5)
```

The description of all those functions is in `doc2vec.py` from the starter kit, but it's worth summarizing them here:

```python
def load_glove(filename):
    """
    Read all lines from the indicated file and return a dictionary
    mapping word:vector where vectors are of numpy `array` type.
    GloVe file lines are of the form:

    the 0.418 0.24968 -0.41242 0.1217 ...

    So split each line on spaces into a list; the first element is the word
    and the remaining elements represent factor components. The length of the vector
    should not matter; read vectors of any length.

    When computing the vector for each document, use just the text, not the text and title.
    """
    ...
```

```python
def load_articles(articles_dirname, gloves):
    """
    Load all .txt files under articles_dirname and return a table (list of lists/tuples)
    where each record is a list of:

      [filename, title, article-text-minus-title, wordvec-centroid-for-article-text]

    We use gloves parameter to compute the word vectors and centroid.

    The filename is fully-qualified name of the text file including
    the path to the root of the corpus passed in on the command line.
    """
    ...
```
 
```python
def recommended(article, articles, n):
    """
    Return a list of the n articles (records with filename, title, etc...)
    closest to article's word vector centroid. The article is one of the elements
    (tuple) from the articles list.
    """
    ...
```

### Efficiency of loading the glove file

It's important to be efficient with memory usage when loading the glove file because as a process runs out of memory it starts to slow down. We call this thrashing because it is swapping things in and out of memory to the disk and back to try to operate within the constraints given to it. For example, don't use list and dictionary comprehensions to split up the glove file as it will require too much memory. (t2.medium machines at Amazon only have 4G RAM). Instead, process the glove file one line at a time and build the dictionary in that loop; for example:

```
d = {}
for line in f.readlines():
    d[...] = ...
```

If your system requires too much memory, your Amazon server will appear to freeze and not respond because it is taking too much time to process the glove file.
 
### Testing your library

At this point you should test your library. There's no point in trying to build a server that uses this library if we're not confident it works. It is much easier to debug a simple main program rather than a web server.  For example, with a main in `doc2vec.py`, you can run it like this:

```bash
python doc2vec.py ~/data/glove.6B/glove.6B.300d.txt ~/github/msds692/bbc
```

Here is the start of a suitable main:

```python
if __name__ == '__main__':
    glove_filename = sys.argv[1]
    articles_dirname = sys.argv[2]

    gloves = load_glove(glove_filename)
    articles = load_articles(articles_dirname, gloves)
    
    print(gloves['dog'])
    ...
```



## Getting started

Download the [starterkit](https://github.com/USFCA-MSDS/msds692/tree/master/hw/code/recommender), which has the following files and structure:

```
├── doc2vec.py
├── server.py
└── templates
    ├── article.html
    └── articles.html
```

There are predefined functions with comments indicating the required functionality.



## Deliverables

### Github

In your github repository, you should submit the following:

* URL.txt; this is a single line text file terminated by a newline character that indicates the machine name or URL address of your server at Google
* doc2vec.py; implement `words()`, `doc2vec()`, `distances()`, `recommended()`

**Please do not add data files such as the word vectors or the BBC corpus to your repository!**


Note that you must give fully-qualified pathnames to the word vectors and the root of the BBC article corpus, if they are not in the same directory.

## Evaluation

To evaluate your projects, the grader and I will run the [test_server.py](https://github.com/USFCA-MSDS/msds692/blob/master/hw/code/recommender/test_server.py) script, from your repo root directory, that automatically pulls your article list page and a selection of article pages to check that your recommendations match our solution.

**Without the IP.txt file at the root of your repository, we cannot test your server and you get a zero!**  Our script reads your IP.txt file with:

```python
with open("IP.txt") as f:
	host = f.read().strip()
```

The starterkit has `localhost:5000` in it so you can test locally before deploying to your server. You must replace `localhost` with the **public** IP address of your server.

It also reads some pickled "truth" data structures that encode the articles from my solution's web server. That data was generated with [pickle_truth.py](https://github.com/USFCA-MSDS/msds692/blob/master/hw/code/recommender/pickle_truth.py).

Here is a sample test run:

```bash
$ cd ~/grading/MSDS692/recommender-hajij
$ python -m pytest -v test_server.py
============================================ test session starts =============================================
platform darwin -- Python 2.7.12, pytest-2.9.2, py-1.4.31, pluggy-0.3.1 -- /Users/USFCA-MSDS/anaconda2/bin/python
cachedir: .cache
rootdir: /Users/USFCA-MSDS/grading/MSDS692/recommender-parrt, inifile: 
collected 2 items 

test_server.py::test_links PASSED
test_server.py::test_sample_articles PASSED

========================================== 2 passed in 0.57 seconds ==========================================
```

*Getting the article list right is worth 20% and getting the recommended articles right is worth 80%.* As you have the complete test, you should be able to get it working and we will grade in binary fashion (works or it doesn't).

*Make sure that your web server process is still running after you break the `ssh` connection by using a browser to connect at your server's public IP address*.



