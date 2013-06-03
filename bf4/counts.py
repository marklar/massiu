#
# Num #bf4 tweets in time period (this hour, today, this week)
#

from util import my_time
from datetime import datetime
from util import gather
from util import store

HASHTAG = 'bf4'
NEW_STREAM = 'bf4_activity'
def num_tweets():
    gather.only_new_tweets(NEW_STREAM)
    coll = store.get_db()[NEW_STREAM]
    ct = lambda dt: coll.find({'created_at_datetime': {'$gte': dt}}).count()
    now = datetime.utcnow()
    return {
        'hour': ct(now - my_time.DELTA_1_HOUR),
        'day':  ct(now - my_time.DELTA_1_DAY),
        'week': ct(now - my_time.DELTA_1_WEEK)
    }
