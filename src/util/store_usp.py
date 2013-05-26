
import store
import pymongo
from bson.objectid import ObjectId

COLL_NAME = 'usp_quotes'

def get_coll():
    return store.get_db()[COLL_NAME]

def get_quotes(brand, usp):
    q = {
        'brand': brand,
        'usp': usp,
    }
    return get_coll().find(q).sort('_id', pymongo.DESCENDING)

def insert_quote(brand, usp, text, name, image_url):
    doc = {
        'brand': brand,
        'usp': usp,
        'text': text,
        'name': name,
        'image': image_url
    }
    return get_coll().insert(doc)

def delete_quote(doc_id):
    oid = ObjectId(doc_id)
    get_coll().remove(oid)
