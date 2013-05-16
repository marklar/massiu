#
# Franchise Highlights
#      num FB likes
#      num @battlefield followers
#      num #bf4 tweets in time period (this hour, today, this week)
#    MISSING: FB likes.
#
#

import gather
import store
import twitter

import bf4_facebook  # num_likes
import bf4_counts    # num_tweets

TWITTER_SCREEN_NAME = 'battlefield'

def highlights():
    """ :: None -> Dictionary """
    return {
        'fb_likes': {
            'user': bf4_facebook.USERNAME,
            'count': bf4_facebook.num_likes()
        },

        'followers': {
            'user': TWITTER_SCREEN_NAME,
            'count': twitter.get_num_followers(TWITTER_SCREEN_NAME)
        },

        'tweets': {
            'hashtag': 'bf4_counts',
            'counts': bf4_counts.num_tweets()
        }
    }

