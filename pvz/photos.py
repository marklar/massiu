#
# Photos of fans with zombies on show floor.
#
# Twitter account: @Bolthouse2400
#

from util import store

def photos():
    return list(store.get_all('pvz_photos'))
