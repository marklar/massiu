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

MINS_IN_HOUR = 60
MINS_IN_DAY = 60 * 24

def num_tweets():
    minutes = fetch.get_minutes(NEW_STREAM, MINS_IN_HOUR)
    one_hour = sum(minutes)
    return {
        'hour': one_hour,
        'day':  one_hour * 24,      # bogus!
        'week': one_hour * 24 * 7   # bogus!
    }
