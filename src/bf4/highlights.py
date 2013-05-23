#
# Franchise Highlights
#      num FB likes
#      num @battlefield followers
#      num #bf4 tweets in time period (this hour, today, this week)
#
# TODO:
# YouTube channel: username?
# View counts:
#   - count for each video?
#   - single aggregate count?
#

from util import twitter
from util import youtube
from util import facebook

import bf4.counts

TWITTER_SCREEN_NAME = 'battlefield'

# TODO: Which is the right FB username?
FB_USERNAME = 'OfficialBattlefield4'

YOUTUBE_USERNAME = 'Battlefield'

def highlights():
    """ :: None -> Dictionary """
    (yt_views, yt_subs) = youtube.get_analytics(YOUTUBE_USERNAME)
    return {
        'youtube': {
            'user': YOUTUBE_USERNAME,
            'views': yt_views,
            'subs': yt_subs
        },

        'fb_likes': {
            'user': FB_USERNAME,
            'count': facebook.get_likes(FB_USERNAME)
        },

        'followers': {
            'user': TWITTER_SCREEN_NAME,
            'count': twitter.get_num_followers(TWITTER_SCREEN_NAME)
        },

        'tweets': {
            'hashtag': '#' + bf4.counts.HASHTAG,
            'counts': bf4.counts.num_tweets()
        }
    }

if __name__ == '__main__':
    print highlights()
