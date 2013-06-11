#
# Get photos from stream --
# optionally only those with a particular hashtag.
#
import pymongo

from util import store
from util import gather
from util import hashtags

def get_imgs_from_tweets(stream_name, hashtag=None):
    gather.only_new_tweets(stream_name)
    query = {'entities.media.media_url': {'$exists': True}}
    if hashtag is not None:
        hashtag_re = hashtags.make_re(hashtag)
        query['entities.hashtags.text'] = hashtag_re
    coll = store.get_db()[stream_name]
    pics = [get_pic(t)
            for t in coll.find(query).sort('id_str', pymongo.DESCENDING)]
    return [p for p in pics if not None]
        
def get_pic(tweet):
    """ Assumes there's just one media_url. """
    try:
        med_ents = tweet['entities']['media']
        for me in med_ents:
            try:
                return me['media_url']
            except KeyError:
                pass
    except KeyError:
        return None
