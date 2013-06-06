import pymongo
from datetime import datetime, timedelta
from dateutil import tz

from util import store

HOURS_DELTA_UTC_LA = 7
LA_TIME_ZONE = tz.gettz('America/Los_Angeles')
def la_now():
    return datetime.now(LA_TIME_ZONE)

MSG_COLL = 'ea_messages'

def delete_message(_id):
    get_coll().remove(_id)

def put_message(dico):
    get_coll().save(dico)

def get_jsonable_active_msg():
    msg = get_active_message()
    if msg is not None:
        return dict([
            (k, msg[k])
            for k in ['text', 'duration_secs']
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
            now = la_now()
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
        'stop_time': {'$lte': la_now()}
    })

#--------------

def get_already_active_message():
    now = la_now()
    return get_one_message({
        'displayed_at': {'$ne': None},
        'stop_time': {'$gt': now}
    })
    
def get_next_active_message():
    now = la_now()
    return get_one_message({
        'displayed_at': {'$exists': False},
        'desired_start_time': {'$lte': now}
    })

def get_one_message(query):
    return get_coll().find_one(query)

def get_messages(query):
    """ Sort: prioritize those to be displayed first. """
    cursor = get_coll().find(query)
    dts = list(cursor.sort('desired_start_time', pymongo.DESCENDING))
    for dt in dts:
        for attr in ['desired_start_time', 'created_at']:
            dt[attr] -= timedelta(hours = HOURS_DELTA_UTC_LA)
    return dts

def get_coll():
    return store.get_db()[MSG_COLL]
