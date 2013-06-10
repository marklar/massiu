#
# Photos of fans with zombies on show floor.
#
# Twitter account: @Bolthouse2400
#

import util.photos as pix

PHOTO_STREAM = 'pvz_photos'

def get_photos(num):
    return pix.get_imgs_from_tweets(PHOTO_STREAM)[:num]
