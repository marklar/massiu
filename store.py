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
    """
    Insert all tweets into collection.
    If any are repeats, just ignore and continue.
    """
    coll = get_db()[collection_name]
    for t in with_db_ids(tweets):
        try:
            coll.insert(t)
        except pymongo.errors.DuplicateKeyError:
            None

def get_all(collection_name):
    """ Return cursor over collection. """
    coll = get_db()[collection_name]
    return coll.find()

#-- newest id --

def set_newest_id(collection_name, newest_id):
    coll = get_db()[collection_name]
    doc = {
        '_id': 'newest_id',
        'val': newest_id
    }
    coll.save(doc)

def get_newest_id(collection_name):
    coll = get_db()[collection_name]
    query = {'_id': 'newest_id'}
    doc = coll.find_one(query)
    if doc is not None:
        return doc['val']
    else:
        return None
