#
# Num #bf4 tweets in time period (this hour, today, this week)
#

from util import my_time
from datetime import datetime
from util import gather
from util import store

from util import fetch

HASHTAG = 'bf4'
NEW_STREAM = 'bf4_highlights'

def num_tweets():
    metadata = fetch.meta(NEW_STREAM)
    hourly = metadata['activity']['hourly']['total'][0]
    daily = metadata['activity']['daily']['total'][0]
    return {
        'hour': hourly,
        'day':  daily,
        'week': daily * 7   # bogus!
    }

def old_num_tweets():
    gather.only_new_tweets(NEW_STREAM)
    coll = store.get_db()[NEW_STREAM]
    ct = lambda dt: coll.find({'created_at_datetime': {'$gte': dt}}).count()
    now = datetime.utcnow()
    return {
        'hour': ct(now - my_time.DELTA_1_HOUR),
        'day':  ct(now - my_time.DELTA_1_DAY),
        'week': ct(now - my_time.DELTA_1_WEEK)
    }
