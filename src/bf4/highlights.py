#
# Franchise Highlights
#      num FB likes
#      num @battlefield followers
#      num #bf4 tweets in time period (this hour, today, this week)
#    MISSING: FB likes.
#
# TODO:
# YouTube channel: username?
# View counts:
#   - count for each video?
#   - single aggregate count?
#

from util import twitter

import bf4.facebook  # num_likes
import bf4.counts    # num_tweets

TWITTER_SCREEN_NAME = 'battlefield'

def highlights():
    """ :: None -> Dictionary """
    return {
        'fb_likes': {
            'user': bf4.facebook.USERNAME,
            'count': bf4.facebook.num_likes()
        },

        'followers': {
            'user': TWITTER_SCREEN_NAME,
            'count': twitter.get_num_followers(TWITTER_SCREEN_NAME)
        },

        'tweets': {
            'hashtag': bf4.counts.HASHTAG,
            'counts': bf4.counts.num_tweets()
        }
    }

