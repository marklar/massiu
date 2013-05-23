#
# TODO: Limit the number of 'starred' to the 5 most recent.
#

import string

from util import store
from util import fetch

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
    starred = get(stream_name_root + '_starred', hashtag)
    featured = get(stream_name_root + '_featured', hashtag)

    # TODO: Limit the number of starred to 5?
    novel_featured = [f for f in featured if f not in starred]

    return {
        'hashtag': hashtag,
        'starred_tweets': starred,
        'other_tweets': novel_featured
    }

def get(str_name, tag):
    return list(store.with_hashtag(str_name, tag))
    