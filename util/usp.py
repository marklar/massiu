# -*- coding: utf-8 -*-
import re
import string
import pymongo
from bson.objectid import ObjectId

import store

COLL_NAME = 'usp_quotes'

def insert_quote(brand, usp, text, name, image_url, is_tweet):
    """ For quotes entered through the UI. """
    doc = {
        'is_tweet': is_tweet,
        'brand': brand,
        'usp': usp,
        'text': replace_apostrophes(text),
        'name': name,
        'image': image_url.replace('_normal.', '.')
    }
    return get_coll().insert(doc)

def replace_apostrophes(text):
    t = re.sub(u'’', "'", text)
    t = re.sub(u'”', '"', t)
    return re.sub(u'“', '"', t)

def get_quotes(brand, usp):
    quotes = list(get(brand, usp))

    # ObjectIds aren't JSON serializable.
    for q in quotes:
        q['_id'] = str(q['_id'])  # need _id in order to delete
        q['usp'] = fix_usp_for_display(q['usp'])
        q['text'] = replace_apostrophes(q['text'])

    return {
        'brand': brand,
        'usp': fix_usp_for_display(usp),
        'quotes': quotes
    }

def fix_usp_for_display(usp):
    return re.sub('^.*: ', '', usp)

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
