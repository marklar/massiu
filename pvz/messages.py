import pymongo
from util import store

MSG_COLL = 'pvz_messages'

def delete_message(_id):
    get_coll().remove(_id)

def put_message(msg):
    get_coll().save(msg)

def get_one():
    res = list(get_all())
    try:
        return { 'text': res[0]['text'] }
    except IndexError:
        return None

def get_all():
    return get_coll().find().sort('_id', pymongo.DESCENDING)

def get_coll():
    return store.get_db()[MSG_COLL]
