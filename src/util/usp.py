import string
import pymongo
from bson.objectid import ObjectId

import store

COLL_NAME = 'usp_quotes'

def insert_quote(brand, usp, text, name, image_url):
    """ For quotes entered through the UI. """
    doc = {
        'is_tweet': False,
        'brand': brand,
        'usp': usp,
        'text': text,
        'name': name,
        'image': image_url.replace('_normal.', '.')
    }
    return get_coll().insert(doc)

def get_quotes(brand, usp):
    quotes = list(get(brand, usp))

    # ObjectIds aren't JSON serializable.
    for q in quotes:
        q['_id'] = str(q['_id'])
        # del q['_id']

    return {
        'brand': brand,
        'usp': usp,
        'quotes': quotes
    }

def delete_quote(doc_id):
    oid = ObjectId(doc_id)
    get_coll().remove(oid)

#--------------------

def get_coll():
    return store.get_db()[COLL_NAME]

def get(brand, usp):
    q = {
        'brand': brand,
        'usp': usp,
    }
    return get_coll().find(q).sort('_id', pymongo.DESCENDING)
