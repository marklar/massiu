from util import gather
from util import store
from util import fetch


STREAMS = [s['name'] for s in fetch.account()['streams']]

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

update()
# one_time_setup()

