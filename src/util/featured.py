#
# TODO: Limit the number of 'starred' to the 5 most recent.
#

from util import fetch

def featured(stream_name_root, hashtag):
    """
    Return both starred and featured.
    Remove any from featured that already appear in starred.
    """
    starred = get(stream_name_root, '_starred')
    featured = get(stream_name_root, '_featured')
    novel_featured = [f for f in featured if f not in starred]
    return {
        'hashtag': hashtag,
        'starred_tweets': starred,
        'other_tweets': novel_featured
    }

#-------------------------

def get(stream_name_root, suffix):
    stream_name = stream_name_root + suffix
    return fetch.stream(stream_name)
