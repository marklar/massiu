# 
# the visualization needs to pull in the latest two photos
# tweeted by the @needforspeed account with the hashtags:
#    #NFSRivalsTopCops
#    #NFSRivalsTopRacers
#

import util.photos as pix

COLL       = 'nfs_photos'    # @needforspeed
COP_TAG    = 'NFSRivalsTopCops'
RACERS_TAG = 'NFSRivalsTopRacers'

def get_photos():
    return {
        'topcop'   : pix.get_imgs_from_tweets(COLL, hashtag=COP_TAG)[:2],
        'topracer' : pix.get_imgs_from_tweets(COLL, hashtag=RACERS_TAG)[:2]
    }
