#
# 1. Franchise Highlights
#      num FB likes
#      num @battlefield followers
#      num #bf4 tweets in time period (this hour, today, this week)
#    MISSING: FB likes.
#
# 2. USP
#    Display:
#       - quote
#       - related tweets / FB-posts  (moderated)
#    MISSING: EA has to provide criteria for the stream.
#

import gather
import store
import twitter

TWITTER_SCREEN_NAME = 'battlefield'
COLL_NAME = 'bf4_usp'

def get_followers():
    twitter.get_num_followers(TWITTER_SCREEN_NAME)

def bf4_counts():
    """ :: None -> {'this_hour': Int, ...}
    Num #bf4 tweets in time period (this hour, today, this week).
    """
    ##
    ## ToDo: Use Twitter API to search for tweets, too.
    ##
    gather.only_new_tweets(COLL_NAME)
    tweets = store.get_all(COLL_NAME)
    dates = (t['created_at'] for t in tweets)
    for d in dates:
        print d

#-------------

sample_date_str = 'Wed May 15 23:33:42 +0000 2013'

#
# For each date, determine whether it's this hour, today, this week.
# Convert 'now' to seconds-since-epoch (SSE).
# Convert each date_str to SSE.
# ...
#


# bf4_counts()
