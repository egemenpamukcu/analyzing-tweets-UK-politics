"""
CS121: Analyzing Election Tweets (Solutions)

Algorithms for efficiently counting and sorting distinct `entities`,
or unique values, are widely used in data analysis.

Functions to implement:

- count_tokens
- find_top_k
- find_min_count
- find_most_salient

You may add helper functions.
"""

import math
from util import sort_count_pairs


def count_tokens(tokens):
    '''
    Counts each distinct token (entity) in a list of tokens

    Inputs:
        tokens: list of tokens (must be immutable)

    Returns: dictionary that maps tokens to counts
    '''
    dict_tokens = {}
    for i in tokens:
        dict_tokens[i] = dict_tokens.get(i, 0) + 1
    return dict_tokens


def create_pair_count(tokens):
    '''
    Counts each distinct token (entity) in a list of tokens

    Inputs:
        tokens: list of tokens (must be immutable)

    Returns: returns list of tuples showing distinct token and
        number of repetitions
    '''
    lst_count = []
    for i in tokens:
        lst_count.append((i, tokens.count(i)))
    return list(set(lst_count))


def find_top_k(tokens, k):
    '''
    Find the k most frequently occuring tokens

    Inputs:
        tokens: list of tokens (must be immutable)
        k: a non-negative integer

    Returns: list of the top k tokens ordered by count.
    '''

    #Error checking (DO NOT MODIFY)
    if k < 0:
        raise ValueError("In find_top_k, k must be a non-negative integer")

    sorted_tokens = sort_count_pairs(create_pair_count(tokens))
    top_k = []
    for i in range(k):
        if i < len(sorted_tokens):
            top_k.append(sorted_tokens[i][0])
    return top_k


def find_min_count(tokens, min_count):
    '''
    Find the tokens that occur *at least* min_count times

    Inputs:
        tokens: a list of tokens  (must be immutable)
        min_count: a non-negative integer

    Returns: set of tokens
    '''

    #Error checking (DO NOT MODIFY)
    if min_count < 0:
        raise ValueError("min_count must be a non-negative integer")
    minl = [token for token in tokens if tokens.count(token) >= min_count]
    return set(minl)


def max_freq(doc):
    '''
    Calculates the repetitions for the term repeated the
        most in a document

    Inputs:
        doc: list

    Returns: (integer) the frequency of the most repeated term
    '''
    freq_list = [doc.count(term) for term in doc]
    return max(freq_list)


def compute_tf(term, doc):
    '''
    Calculates term frequency of the given term

    Inputs:
        term: value for which tf will be computed
        doc: list

    Returns: (float) term frequency score of the term
    '''
    ratio = doc.count(term) / max_freq(doc)
    tf = 0.5 + 0.5 * ratio
    return tf


def compute_idf(docs, term):
    '''
    Calculates inverse document frequency of the given term

    Inputs:
        term: value for which tf will be computed
        docs: list of lists containing terms

    Returns: (float) inverse document frequency score of the term
    '''
    num_w_term = 0
    for doc in docs:
        if term in doc:
            num_w_term += 1
    return math.log(len(docs) / num_w_term)


def compute_tfidf(docs, doc, term):
    '''
    Calculates augmented frequency of the given term

    Inputs:
        term: value for which tf will be computed
        doc: list
        docs: list of lists containing terms

    Returns: (float) augmented frequency score by multiplying
        tf and idf
    '''
    salience = compute_tf(term, doc) * compute_idf(docs, term)
    return salience


def find_salient(docs, threshold):
    '''
    Compute the salient words for each document.  A word is salient if
    its tf-idf score is strictly above a given threshold.

    Inputs:
      docs: list of list of tokens
      threshold: float

    Returns: list of sets of salient words
    '''
    list_salient = []
    for doc in docs:
        doc_salient = []
        for term in doc:
            if compute_tfidf(docs, doc, term) > threshold:
                doc_salient.append(term)
        list_salient.append(set(doc_salient))
    return list_salient
