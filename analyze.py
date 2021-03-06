"""
Analyze module
"""

import unicodedata
import sys

from basic_algorithms import find_top_k, find_min_count, find_salient

##################### DO NOT MODIFY THIS CODE #####################

def keep_chr(ch):
    '''
    Find all characters that are classifed as punctuation in Unicode
    (except #, @, &) and combine them into a single string.
    '''
    return unicodedata.category(ch).startswith('P') and \
        (ch not in ("#", "@", "&"))

PUNCTUATION = " ".join([chr(i) for i in range(sys.maxunicode)
                        if keep_chr(chr(i))])

# When processing tweets, ignore these words
STOP_WORDS = ["a", "an", "the", "this", "that", "of", "for", "or",
              "and", "on", "to", "be", "if", "we", "you", "in", "is",
              "at", "it", "rt", "mt", "with"]

# When processing tweets, words w/ a prefix that appears in this list
# should be ignored.
STOP_PREFIXES = ("@", "#", "http", "&amp")


#####################  MODIFY THIS CODE #####################


############## Part 2 ##############

# Task 2.1


def list_values(tweets, entity_desc):
    '''
    Lists the values fitting the entity description

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc

    Returns: list of entities
    '''
    key = entity_desc[0]
    subkey = entity_desc[1]
    case_sensitive = entity_desc[2]

    lst_val = []
    for tweet in tweets:
        for i in tweet['entities'][key]:
            if case_sensitive:
                lst_val.append(i[subkey])
            else:
                lst_val.append(str.lower(i[subkey]))
    return lst_val


def find_top_k_entities(tweets, entity_desc, k):
    '''
    Find the k most frequently occuring entitites

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc
        k: integer

    Returns: list of entities
    '''
    lst_val = list_values(tweets, entity_desc)
    top_k_entities = find_top_k(lst_val, k)

    return top_k_entities


# Task 2.2
def find_min_count_entities(tweets, entity_desc, min_count):
    '''
    Find the entitites that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc
        min_count: integer

    Returns: set of entities
    '''
    lst_val = list_values(tweets, entity_desc)
    min_count_entities = find_min_count(lst_val, min_count)
    return min_count_entities




############## Part 3 ##############


def pre_process(tweet, case_sensitive, stop_require=True):
    '''
    Pre processes the tweet text to remove certain words and characters

    Inputs:
        tweet: dictionary containing details on the tweet
        case_sensitive: boolean
        stop_require: boolean, shows whether stop words will be removed

    Returns: list of processed words
    '''
    abridged_text = tweet['abridged_text'].split()
    processed_text = []
    pre_processed_text = []

    for i, word in enumerate(abridged_text):
        abridged_text[i] = word.strip(PUNCTUATION)
    for word in abridged_text:
        if stop_require:
            if word not in STOP_WORDS:
                pre_processed_text.append(word)
        else:
            pre_processed_text = abridged_text
    for word in pre_processed_text:
        if  not word.startswith(STOP_PREFIXES) and word != '':
            processed_text.append(word)
    if not case_sensitive:
        for i, word in enumerate(processed_text):
            processed_text[i] = str.lower(word)

    return processed_text


def compute_ngrams(tweet, n, case_sensitive, stop_requirement=True):
    '''
    Computes the n-gram of the given tweet based on the n value

    Inputs:
        tweet: dictionary
        n: integer
        case_sensitive: boolean
        stop_requirement: boolean

    Returns: n-gram
    '''
    processed_text = pre_process(tweet, case_sensitive, stop_requirement)
    ngram = []
    if len(processed_text) >= n:
        for i, _ in enumerate(processed_text):
            ngram.append(tuple(processed_text[i:i + n]))
            if len(ngram) >= len(processed_text) - n + 1:
                break
    return ngram


def find_top_k_ngrams(tweets, n, case_sensitive, k):
    '''
    Find k most frequently occurring n-grams

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        k: integer

    Returns: list of n-grams
    '''
    total_ngrams = []
    for tweet in tweets:
        ngram = compute_ngrams(tweet, n, case_sensitive)
        for tpl in ngram:
            total_ngrams.append(tpl)
    top_k_ngrams = find_top_k(total_ngrams, k)
    return top_k_ngrams



def find_min_count_ngrams(tweets, n, case_sensitive, min_count):
    '''
    Find n-grams that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        min_count: integer

    Returns: set of n-grams
    '''
    total_ngrams = []
    for tweet in tweets:
        ngram = compute_ngrams(tweet, n, case_sensitive)
        for tpl in ngram:
            total_ngrams.append(tpl)
    min_count_ngrams = find_min_count(total_ngrams, min_count)
    return min_count_ngrams


def find_salient_ngrams(tweets, n, case_sensitive, threshold):
    '''
    Find the salient n-grams for each tweet.

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        threshold: float

    Returns: list of sets of strings
    '''
    total_ngrams = []
    for tweet in tweets:
        total_ngrams.append(compute_ngrams(tweet, n, case_sensitive, False))
    salient_ngrams = find_salient(total_ngrams, threshold)
    return salient_ngrams
