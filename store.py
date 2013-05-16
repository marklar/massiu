#
# Shortcut MongoDB methods for:
#   - inserting tweets in bulk, and
#   - fetching all tweets (w/o select criteria).
# 

import pymongo

DB_NAME = 'b_reel'

# globals (mutating)
client = None
db = None

def get_client():
    """ Cache MongoClient. """
    global client
    if client is None:
        client = pymongo.MongoClient()
    return client

def get_db():
    """ Cache DB reference. """
    global db
    if db is None:
        db = get_client()[DB_NAME]
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

#-- tweet counts --

def count_hashtags(collection_name, hashtag_re):
    query = { 'entities.hashtags.text': hashtag_re }
    return get_db()[collection_name].find(query).count()

#-- tweets --

def put(collection_name, tweets):
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
        return agg_result['result'][0]['extreme_id']
    else:
        return None

def with_db_ids(tweets):
    """ Mutates arg. """
    for t in tweets:
        t['_id'] = t['id_str']
    return tweets
