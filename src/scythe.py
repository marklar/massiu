from util import gather
from util import store

# 'respawn' - out

STREAMS = [
    'bf4_usp',
    'ea_activity',
    'ea_featured',
    'ea_starred',
    'nfs_leaderboard',
    'pvz_featured',
    'pvz_photos',
    'pvz_starred',
    'sports_easportsignite_featured',
    'sports_easportsignite_starred',
    'sports_feelthefight_featured',
    'sports_feelthefight_starred',
    'sports_fifa14_featured',
    'sports_fifa14_starred',
    'sports_maddennext25_featured',
    'sports_maddennext25_starred',
    'sports_wearelive_featured',
    'sports_wearelive_starred'
]

#
# TODO: For 'ea_activity', don't need to grab the actual tweets.
# Only need to grab {'_id': XXX, 'hashtags': [AAA, BBB], 'created_at': ZZZ}.
# Smaller DB & simpler queries.
#

def one_time_setup():
    for src in STREAMS:
        store.drop_coll(src)
        print "--SRC-- :", src
        gather.all_tweets(src)

def update():
    for src in STREAMS:
        print "--SRC-- :", src
        gather.only_new_tweets(src)

# update()
one_time_setup()

