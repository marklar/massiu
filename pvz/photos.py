#
# Photos of fans with zombies on show floor.
#
# Twitter account: @Bolthouse2400
#

from util import store
from util import gather

def get_photos(num):
    # TODO: This is the WRONG STREAM.  Just for fake data.
    return get_imgs_from_tweets('pvz_featured')[:num]

#----------------------------

def get_imgs_from_tweets(stream_name):
    gather.only_new_tweets(stream_name)
    coll = store.get_db()[stream_name]
    q = {'entities.media.media_url': {'$exists': True}}
    pics = [get_pic(t) for t in coll.find(q)]
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
