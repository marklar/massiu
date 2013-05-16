import gather

STREAMS = [
    'bf4',
    'ea_activity',
    'ea_featured',
    'nfs_leaderboard',
    'pvz',
    'respawn'
]

def one_time_setup():
    for src in STREAMS:
        print "--SRC-- :", src
        gather.all_tweets(src)

def update():
    for src in STREAMS:
        print "--SRC-- :", src
        gather.only_new_tweets(src)

update()
