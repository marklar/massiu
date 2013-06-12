#
# Photos of fans with zombies on show floor.
# Twitter account: @Bolthouse2400
#

import pymongo
import random

import util.store
import util.gather
import util.photos as pix
import pvz.via_me

PHOTO_STREAM = 'pvz_photos'

def get_pix_of_both_kinds(num):
    regulars = get_photos()
    via_mes = from_via_me()
    all_pix = list(set((via_mes + regulars)))
    return n_rand(num, all_pix)

def n_rand(num, lst):
    res = []
    for i in range(0, num):
        idx = random.randint(0, len(lst)-1)
        res.append(lst.pop(idx))
    return res

def get_photos():
    return pix.get_imgs_from_tweets(PHOTO_STREAM)

#-----------------

def from_via_me():
    util.store.drop_coll(PHOTO_STREAM)
    util.gather.only_new_tweets(PHOTO_STREAM)
    query = {'entities.urls.expanded_url': {'$exists': True}}
    coll = util.store.get_db()[PHOTO_STREAM]
    tweets = coll.find(query).sort('id_str', pymongo.DESCENDING)
    pics = [ pvz.via_me.get_pic_from_tweet(t) for t in tweets ]
    return [p for p in pics if not None]
