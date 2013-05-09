# from pymongo import MongoClient, DuplicateKeyError
import pymongo

DB_NAME = 'b_reel'

# globals
client = None
db = None

def get_client():
    global client
    if client is None:
        client = pymongo.MongoClient()
    return client

def get_db():
    global db
    if db is None:
        db = get_client()[DB_NAME]
    return db

def put(collection, tweets):
    # Add _id to each.
    for t in tweets:
        t['_id'] = t['id']
    coll = get_db()[collection]
    for t in tweets:
        try:
            coll.insert(t)
        except pymongo.errors.DuplicateKeyError:
            None
        
