
import string  # lstrip

from util import store
from util import fetch
from util import gather

FEATURED_SUFFIX = '_featured'
STARRED_SUFFIX = '_starred'

def get_all_featured(stream_root):
    hashtags = get_hashtags(stream_root)
    return [get_featured(stream_root, h) for h in hashtags]

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
    starred = get_w_tag(stream_name_root + STARRED_SUFFIX, hashtag)
    featured = get_w_tag(stream_name_root + FEATURED_SUFFIX, hashtag)

    # TODO: Limit the number of starred to 5?
    novel_featured = [f for f in featured if f not in starred]

    return {
        'hashtag': '#' + hashtag,
        'starred_tweets': starred,
        'other_tweets': novel_featured
    }

def get_w_tag(stream_name, hashtag):
    gather.only_new_tweets(stream_name)
    return [slim(t) for t in store.with_hashtag(stream_name, hashtag)]
    
def slim(tweet):
    """ Extract from tweet only the info we care about. """
    u = tweet['user']
    return {
        'text': tweet['text'],
        'name': u['name'],
        'image': u['profile_image_url'],
        'screen_name': u['profile_image_url']
    }
