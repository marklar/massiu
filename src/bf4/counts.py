#
# Num #bf4 tweets in time period (this hour, today, this week)
#

from util import my_time
from datetime import datetime
from util import gather
from util import store
from util import hashtags

NEW_STREAM = 'bf4_activity'
def new_num_tweets():
    gather.only_new_tweets(NEW_STREAM)
    coll = store.get_db()[NEW_STREAM]
    ct = lambda dt: coll.find({'created_at_datetime': {'$gte': dt}}).count()
    now = datetime.utcnow()
    return {
        'hour': ct(now - my_time.DELTA_1_HOUR),
        'day':  ct(now - my_time.DELTA_1_DAY),
        'week': ct(now - my_time.DELTA_1_WEEK)
    }

HASHTAG = 'bf4'
COUNTS_COLL_NAME = 'ea_activity'

#
# FIXME: Seems to be a problem with collecting new-enough tweets.
# None of them are ever from within the last 1 hour.
#
def num_tweets():
    """ :: None -> {}
    Num #bf4 tweets in time period (this hour, today, this week).
    """
    gather.only_new_tweets(COUNTS_COLL_NAME)
    tweets = store.with_hashtag(COUNTS_COLL_NAME, HASHTAG)
    datetimes = [my_time.make_datetime(t['created_at']) for t in tweets]
    return {
        'hour': count_in_delta(datetimes, my_time.DELTA_1_HOUR),
        'day':  count_in_delta(datetimes, my_time.DELTA_1_DAY),
        'week': count_in_delta(datetimes, my_time.DELTA_1_WEEK)
    }

#----------------------

def count_in_delta(datetimes, delta):
    """ :: [datetime.datetime], datetime.timedelta -> Int """
    now = my_time.los_angeles_now()
    cnt = 0
    for dt in datetimes:
        if now - dt <= delta:
            cnt += 1
    return cnt
