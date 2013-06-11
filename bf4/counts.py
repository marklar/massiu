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
