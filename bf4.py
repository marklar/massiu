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

import bf4_facebook  # num_likes
import bf4_counts    # num_tweets

TWITTER_SCREEN_NAME = 'battlefield'

def franchise_highlights():
    return {
        'fb-likes': bf4_facebook.num_likes(),
        'followers': twitter.get_num_followers(TWITTER_SCREEN_NAME),
        'num-tweets': bf4_counts.num_tweets()
    }

# print franchise_highlights()
