import gather

# 'respawn' - out

STREAMS = [
    'bf4_counts',
    'bf4_usp',
    'ea_activity',
    'ea_featured',
    'eae3_counts',
    'nfs_counts',
    'nfs_leaderboard',
    'pvz_counts',
    'pvz_featured'
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
