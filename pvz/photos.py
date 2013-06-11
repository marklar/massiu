#
# Photos of fans with zombies on show floor.
#
# Twitter account: @Bolthouse2400
#

import pymongo
import util.store
import util.gather
import util.photos as pix

PHOTO_STREAM = 'pvz_photos'

def get_photos(num):
    return pix.get_imgs_from_tweets(PHOTO_STREAM)[:num]

#-----------------

def get_imgs_from_via_me(num):
    util.store.drop_coll(PHOTO_STREAM)
    util.gather.only_new_tweets(PHOTO_STREAM)
    query = {'entities.urls.expanded_url': {'$exists': True}}
    coll = util.store.get_db()[PHOTO_STREAM]
    pics = [ get_pic(t)
             for t in coll.find(query).sort('id_str', pymongo.DESCENDING) ]
    return [p for p in pics if not None]

def get_pic(tweet):
    try:
        url = tweet['entities']['urls'][0]
        return url['expanded_url']
    except KeyError:
        return None
        
