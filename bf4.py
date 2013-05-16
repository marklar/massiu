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

def usp():
    """
    Reply with:
      + USP quote
      + related MR things: tweets / FB posts
    """
    return {
        'brand_logo': None,
        'usp': 'online multiplayer!',
        'quotes': [
            {
                'profile_image': None,
                'name': 'Bob Smith',
                'quote': "In the realm of online combat, Battlefield 4 provides thrills that few games can match."
            },

            {
                'profile_image': None,
                'name': 'Chris Waters',
                'quote': "Battlefield 4 is a thrilling action game that immerses you in the chaos of combat like never before."
            },

            {
                'profile_image': None,
                'name': 'Jim Jones',
                'quote': "Battlefield 4 boasts a fast-paced and thrilling campaign, as well as some of the most immersive and exciting multiplayer action ever seen on consoles."
}
        ]
    }

# print usp()
