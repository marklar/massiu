#
# Num #bf4 tweets in time period (this hour, today, this week)
#

import time
from datetime import datetime, date, timedelta
from dateutil import tz

from util import gather
from util import store
from util import hashtags

HASHTAG_RE = hashtags.make_re('bf4')
COUNTS_COLL_NAME = 'ea_activity'

DELTA_1_HOUR = timedelta(hours = 1)
DELTA_1_DAY  = timedelta(days  = 1)
DELTA_1_WEEK = timedelta(weeks = 1)

LA_TIME_ZONE = tz.gettz('America/Los_Angeles')


def num_tweets():
    """ :: None -> {}
    Num #bf4 tweets in time period (this hour, today, this week).
    """
    ##
    ## ToDo: Use Twitter API to search for tweets, too?
    ##
    gather.only_new_tweets(COUNTS_COLL_NAME)
    tweets = store.with_hashtag(COUNTS_COLL_NAME, HASHTAG_RE)
    dates = [make_la_date(t['created_at']) for t in tweets]
    return {
        'hour': count_in_delta(dates, DELTA_1_HOUR),
        'day':  count_in_delta(dates, DELTA_1_DAY),
        'week': count_in_delta(dates, DELTA_1_WEEK)
    }


#----------------------

def make_la_date(date_str):
    """ :: String -> datetime.datetime
    e.g. 'Wed May 15 23:33:42 +0000 2013'
    """
    time_struct = time.strptime(date_str, "%a %b %d %H:%M:%S +0000 %Y")
    return datetime.fromtimestamp(time.mktime(time_struct), LA_TIME_ZONE)

def count_in_delta(dates, delta):
    """ :: [datetime.datetime], datetime.timedelta -> Int """
    now = datetime.now(LA_TIME_ZONE)
    cnt = 0
    for d in dates:
        if now - d <= delta:
            cnt += 1
    return cnt
