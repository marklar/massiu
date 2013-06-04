#
# Shortcut MongoDB methods for:
#   - inserting tweets in bulk, and
#   - fetching all tweets (w/o select criteria).
# 

import pymongo
import os
from urlparse import urlsplit
import time
from datetime import datetime, timedelta
from dateutil import tz

from util import hashtags

DEF_MONGO_URI = 'mongodb://localhost:27017/b_reel'

# globals (mutating)
client = None
db = None

def drop_coll(collection_name):
    get_db()[collection_name].drop()

def get_client(loc):
    """ Memoize MongoClient. """
    global client
    if client is None:
        client = pymongo.MongoClient(loc)
    return client

def get_db():
    """ Memoize DB reference. """
    global db
    if db is None:
        # MONGOLAB_URL
        mongo_url = os.getenv('MONGOHQ_URL', DEF_MONGO_URI)
        uri = urlsplit(mongo_url)

        # Authentication necessary?
        if '@' in uri.netloc:
            # Get DB
            parts = uri.netloc.split('@')
            client = get_client(parts[1])
            db = client[uri.path[1:]]
            # Authenticate
            (user, passwd) = parts[0].split(':')
            db.authenticate(user, passwd)
        else:
            # Get DB
            client = get_client(uri.netloc)
            db = client[uri.path[1:]]

    return db

#-- cache --

DELTA = timedelta(minutes=5)

def cache_key(obj, *args):
    key = obj.__class__.__name__
    for a in args:
        key += (' ' + a)
    return key

def get_cache():
    return get_db()['cache']

def get_cached(obj, *args):
    dt = datetime.utcnow() - DELTA
    key = cache_key(obj, *args)
    q = {'_id': key, 'created_at': {'$gte': dt}}
    doc = get_cache().find_one(q)
    if doc is not None:
        return doc['val']
    else:
        return None

def put_cached(val, obj, *args):
    doc = {
        '_id': cache_key(obj, *args),
        'val': val,
        'created_at': datetime.utcnow()
    }
    return get_cache().save(doc)

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

UTC_TIME_ZONE = tz.gettz('Europe/London')

FORMAT = "%a %b %d %H:%M:%S +0000 %Y"
def make_utc_datetime(date_str):
    """ :: String -> datetime.datetime
    e.g. 'Wed May 15 23:33:42 +0000 2013'
    """
    time_struct = time.strptime(date_str, FORMAT)
    return datetime.fromtimestamp(time.mktime(time_struct), UTC_TIME_ZONE)

def add_created_at_datetime(tweet):
    tweet['created_at_datetime'] = make_utc_datetime(tweet['created_at'])
    return tweet

def put_tweets(collection_name, tweets):
    """ :: String, [Tweet] -> None
    Insert all tweets into collection.
    If any are repeats, just ignore and continue.
    """
    coll = get_db()[collection_name]
    dt_tweets = [add_created_at_datetime(t) for t in tweets]
    coll.insert(
        with_db_ids(dt_tweets),
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
    """ More-recent first. """
    coll = get_db()[ORIGIN_COLLECTION]
    return coll.find().sort('_id', pymongo.DESCENDING)

def put_origin_data(dico):
    coll = get_db()[ORIGIN_COLLECTION]
    coll.insert(dico)

#--------------

NFS_GAME_STATS_COLLECTION = 'nfs_game_stats'

def get_most_recent_nfs_game_stats():
    stats = get_nfs_game_stats()[0]
    del stats['_id']
    return stats

def get_nfs_game_stats():
    """ More-recent first. """
    coll = get_db()[NFS_GAME_STATS_COLLECTION]
    return coll.find().sort('_id', pymongo.DESCENDING)

def put_nfs_game_stats(dico):
    coll = get_db()[NFS_GAME_STATS_COLLECTION]
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
