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

def with_db_ids(tweets):
    """ Mutates arg. """
    for t in tweets:
        t['_id'] = t['id_str']
    return tweets

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


#-- collection meta-information --

#-- oldest --
#  (no longer used?)

def set_oldest_id(collection_name, oldest_id):
    set_x_id(collection_name, 'oldest_id', oldest_id)

def get_oldest_id(collection_name):
    get_x_id(collection_name, 'oldest_id')

#-- newest --

def set_newest_id(collection_name, newest_id):
    set_x_id(collection_name, 'newest_id', newest_id)

def get_newest_id(collection_name):
    get_x_id(collection_name, 'newest_id')

#-- helpers --

def set_x_id(collection_name, name, val):
    coll = get_db()[collection_name]
    doc = {
        '_id': name,
        'val': val
    }
    coll.save(doc)

def get_x_id(collection_name, name):
    coll = get_db()[collection_name]
    query = {'_id': name}
    doc = coll.find_one(query)
    if doc is not None:
        return doc['val']
    else:
        return None
