#
# Shortcut MongoDB methods for:
#   - inserting tweets in bulk, and
#   - fetching all tweets (w/o select criteria).
# 

import pymongo
# from pymongo import Connection
import os
from urlparse import urlsplit

from util import hashtags

DEF_MONGO_URI = 'mongodb://localhost:27017/b_reel'

# globals (mutating)
client = None
db = None

def drop_coll(collection_name):
    get_db()[collection_name].drop()

def get_client(host, port):
    """ Cache MongoClient. """
    global client
    if client is None:
        client = pymongo.MongoClient(host, port)
    return client

def get_db():
    """ Cache DB reference. """
    global db
    if db is None:
        # MONGOLAB_URL
        mongo_url = os.getenv('MONGOHQ_URL', DEF_MONGO_URI)
        uri = urlsplit(mongo_url)

        # Get your DB
        client = get_client(uri.netloc, uri.port)
        db = client[uri.path[1:]]
        # authenticate
        if '@' in mongo_url:
            user_pass = uri.netloc.split('@')[0].split(':')
            db.authenticate(user_pass[0], user_pass[1])
    return db

#-- collection meta-information --

def get_min_id_str(collection_name):
    """ :: String -> String
    Given a collection, find the lowest (min) id_str value.
    """
    return get_extreme_id_str(collection_name, '$min')

def get_max_id_str(collection_name):
    """ :: String -> String
    Given a collection, find the highest (max) id_str value.
    """
    return get_extreme_id_str(collection_name, '$max')

#-- tweets w/ hashtag --

def count_hashtag(collection_name, hashtag):
    """ hashtag: no '#'! """
    return with_hashtag(collection_name, hashtag).count()

def with_hashtag(collection_name, hashtag):
    """
    hashtag: no '#'!
    -> cursor
    """
    hashtag_re = hashtags.make_re(hashtag)
    query = { 'entities.hashtags.text': hashtag_re }
    return get_db()[collection_name].find(query)

#-- tweets --

def put_tweets(collection_name, tweets):
    """ :: String, [Tweet] -> None
    Insert all tweets into collection.
    If any are repeats, just ignore and continue.
    """
    coll = get_db()[collection_name]
    coll.insert(
        with_db_ids(tweets),
        w=0,                    # disable write acknowledgement
        continue_on_error=True  # don't stop bulk insert upon dupe ID failure
    )

def get_all(collection_name):
    """ Return cursor over collection. """
    coll = get_db()[collection_name]
    return coll.find()

#--------------

ORIGIN_COLLECTION = 'origin'

def get_origin_data():
    """ Get the most-recently inserted. """
    coll = get_db()[ORIGIN_COLLECTION]
    return coll.find().sort({'_id': -1})[0]

def put_origin_data(dico):
    coll = get_db()[ORIGIN_COLLECTION]
    coll.insert(dico)
    

#-- helpers --

def get_extreme_id_str(collection_name, operator):
    """ :: String -> String
    Given a collection, find the min/max id_str value.
    """
    coll = get_db()[collection_name]
    # Perform an aggregation to find the min/max id_str.
    # http://docs.mongodb.org/manual/reference/aggregation/min/
    agg_result = coll.aggregate([
        { '$group': { '_id': 0, 'extreme_id': { operator: "$id_str"} } }
    ])
    if agg_result['ok'] == 1:
        try:
            return agg_result['result'][0]['extreme_id']
        except IndexError:
            return None
    else:
        return None

def with_db_ids(tweets):
    """ Mutates arg. """
    for t in tweets:
        t['_id'] = t['id_str']
    return tweets
