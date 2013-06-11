# 
# the visualization needs to pull in the latest two photos
# tweeted by the @needforspeed account with the hashtags:
#    #NFSRivalsTopCops
#    #NFSRivalsTopRacers
#

from web import ctx
import util.photos as pix

COLL       = 'nfs_photos'    # @needforspeed
COP_TAG    = 'NFSRivalsTopCops'
RACERS_TAG = 'NFSRivalsTopRacers'

DEF_COPS   = ['0000_cop1.jpg',   '0001_cop2.jpg']
DEF_RACERS = ['0002_racer1.jpg', '0003_racer2.jpg']

def get_photos(prot_n_host):
    return {
        'topcop'   : get_cops(prot_n_host),
        'topracer' : get_racers(prot_n_host)
    }

def get_cops(prot_n_host):
    return get(COP_TAG,
               prot_n_host,
               DEF_COPS)

def get_racers(prot_n_host):
    return get(RACERS_TAG,
               prot_n_host,
               DEF_RACERS)

def get(tag, prot_n_host, defs):
    live = pix.get_imgs_from_tweets(COLL, hashtag=tag)[:2]
    full_defs = [full_path(prot_n_host, f) for f in defs]
    return (live + full_defs)[:2]

def full_path(prot_n_host, f):
    return prot_n_host + '/static/NFS-gamestats-defaultImage_' + f
