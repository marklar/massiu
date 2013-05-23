#
# Num #bf4 tweets in time period (this hour, today, this week)
#

from util import my_time
from util import gather
from util import store
from util import hashtags

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

def count_in_delta(dates, delta):
    """ :: [datetime.datetime], datetime.timedelta -> Int """
    now = my_time.los_angeles_now()
    cnt = 0
    for d in dates:
        if now - d <= delta:
            cnt += 1
    return cnt
