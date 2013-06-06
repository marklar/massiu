import pymongo
from bson.objectid import ObjectId
from datetime import datetime, timedelta

from util import store

MSG_COLL = 'messages'

def delete_message(id_str):
    _id = ObjectId(id_str)
    get_coll().remove(_id)

def put_message(dico):
    get_coll().save(dico)

def get_jsonable_active_msg():
    msg = get_active_message()
    if msg is not None:
        return dict([
            (k, msg[k])
            for k in ['brand', 'text', 'duration_secs']
        ])
    else:
        return None

def get_active_message():
    msg = get_already_active_message()
    if msg is not None:
        return msg
    else:
        msg = get_next_active_message()
        if msg is not None:
            now = datetime.now()
            msg['displayed_at'] = now
            msg['stop_time'] = now + timedelta(seconds = msg['duration_secs'])
            put_message(msg)
            return msg
        else:
            return None

def get_future_messages():
    return get_messages({
        'displayed_at': None
    })

def get_expired_messages():
    return get_messages({
        'displayed_at': {'$ne': None},
        'stop_time': {'$lte': datetime.now()}
    })

#--------------

def get_already_active_message():
    now = datetime.now()
    return get_one_message({
        'displayed_at': {'$ne': None},
        'stop_time': {'$gt': now}
    })
    
def get_next_active_message():
    now = datetime.now()
    return get_one_message({
        'displayed_at': {'$exists': False},
        'desired_start_time': {'$lte': now}
    })

def get_one_message(query):
    return get_coll().find_one(query)

def get_messages(query):
    """ Sort: prioritize those to be displayed first. """
    return get_coll().find(query).sort('desired_start_time', pymongo.ASCENDING)

def get_coll():
    return store.get_db()[MSG_COLL]

# Problem:
#
# Message A starts earlier, ends later.
# Message B starts later, ends sooner.
# Currently, B gets completely eclipsed.
#
# How to make it so that B doesn't get passed over completely?
# Flag each message as already_displayed or not.
#
# Change 'start_time' to 'desired_start_time'.
# Make 'stop_time' None until the thing gets dislpayed.
# Add attributes: 'displayed_at' (def: None), and 'is_expired' (def: False).
# When displayed, set 'displayed_at' and 'stop_time'.
#
# Active:
#    'displayed_at' is not None and 'stop_time' not passed.
#    If none, then 'displayed_at' is None and 'desired_start_time' is passed.
# Future: 'desired_start_time' not passed.
# Expired:
#    'displayed_at' is not None and 'stop_time' is passed.
#    Add 'is_expired': True.
#
# Each time, check to see whether the currently active
#

