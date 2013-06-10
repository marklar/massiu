#
# Franchise Highlights
#      num FB likes
#      num @battlefield followers
#      num #bf4 tweets in time period (this hour, today, this week)
#
#

from util import twitter
from util import youtube
from util import facebook

import bf4.counts

TWITTER_SCREEN_NAME = 'battlefield'
EA_SCREEN_NAME = 'ea'

FB_USERNAME = 'Battlefield'

YOUTUBE_USERNAME = 'Battlefield'

def highlights():
    """ :: None -> Dictionary """
    # (yt_views, yt_subs) = youtube.get_analytics(YOUTUBE_USERNAME)
    (yt_views, yt_subs) = get_youtube_stats(YOUTUBE_USERNAME)
    return {
        # TODO: This is canned.
        'youtube': {
            'user': YOUTUBE_USERNAME,
            'views': yt_views,
            'subs': yt_subs
        },

        # TODO: This is canned.
        # 'fb_likes': facebook.get_likes(FB_USERNAME),
        # https://www.facebook.com/battlefield
        'fb_likes': 4863667,

        'bf4_followers': {
            'user': TWITTER_SCREEN_NAME,
            'count': twitter.get_num_followers(TWITTER_SCREEN_NAME)
        },

        'ea_followers': {
            'user': EA_SCREEN_NAME,
            'count': twitter.get_num_followers(EA_SCREEN_NAME)
        },

        'tweets': {
            'hashtag': '#' + bf4.counts.HASHTAG,
            'counts': bf4.counts.num_tweets()
        }
    }

def get_youtube_stats(username):
    # http://www.youtube.com/user/Battlefield/about
    views = 104424628
    subs = 662482
    return (views, subs)


if __name__ == '__main__':
    print highlights()
