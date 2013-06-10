import itertools
import string  # lstrip, replace
import pymongo
import re

from util import store
from util import fetch
from util import gather

FEATURED_SUFFIX = '_featured'
STARRED_SUFFIX = '_starred'

def get_all_featured(stream_root):
    hashtags = get_hashtags(stream_root)
    # return [get_featured(stream_root, h) for h in hashtags]
    return get_featured(stream_root, hashtags[0])

#----------------------------------------

def get_hashtags(stream_root):
    kws = get_keywords(stream_root)
    return [rm_hash(k) for k in kws]

def get_keywords(stream_root):
    metadata = fetch.meta(stream_root + '_featured')
    return metadata['sources']['keyword']

def rm_hash(keyword):
    return keyword.lstrip('#')

def get_featured(stream_name_root, hashtag):
    """
    Return both starred and featured.
    Remove any from featured that already appear in starred.
    """
    # TODO
    store.drop_coll(stream_name_root + STARRED_SUFFIX)
    store.drop_coll(stream_name_root + FEATURED_SUFFIX)

    # Return only ONE starred tweet.
    starred = get_slims(stream_name_root + STARRED_SUFFIX, hashtag)
    try:
        starred = starred[0]
    except IndexError:
        starred = None
    featured = get_slims(stream_name_root + FEATURED_SUFFIX, hashtag)

    # Return no more than 30 other tweets.
    novel_featured = [f for f in featured if f != starred][:30]

    return {
        'hashtag': '#' + hashtag,
        'starred_tweet': starred,
        'other_tweets': novel_featured
    }

def old_get_slims(stream_name, hashtag):
    gather.only_new_tweets(stream_name)
    # return [slim(t) for t in store.with_hashtag(stream_name, hashtag)]
    return [slim(t)
            for t in store.get_all(stream_name).sort('id_str', pymongo.DESCENDING)]

def get_slims(stream_name, hashtag):
    tweet_lists = []
    old_id = None
    while True:
        tweets = fetch.stream(
            stream_name,
            account_name='MR_breel',
            start_id=old_id)
        if not tweets:
            break
        old_id = tweets[0]['id_str']
        tweet_lists.append(tweets)
        
    # [slim(t) for sublist in tweet_lists for t in sublist]
    return [slim(t) for t in itertools.chain.from_iterable(tweet_lists)]
    
def slim(tweet):
    """ Extract from tweet only the info we care about. """
    user = tweet['user']
    return {
        'text':        rm_urls(tweet['text']),
        'name':        user['name'],
        'image':       user['profile_image_url'].replace('_normal.', '.'),
        'screen_name': '@' + user['screen_name']
    }
    
PATTERN = 'http://[^\s]*(\s+|$)'
def rm_urls(text):
    return re.sub(PATTERN, '', text)
