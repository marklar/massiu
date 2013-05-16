import gather

ACCOUNT = 'MR_breel'
# API_KEY = 'abf59546eabec151a5565a81d8285ebf'  # stream mgnt API

STREAMS = ['ea_activity', 'nfs_leaderboard', 'pvz', 'respawn']

def one_time_setup():
    for src in STREAMS:
        print "--SRC-- :", src
        gather.all_tweets(ACCOUNT, src)

def update():
    for src in STREAMS:
        print "--SRC-- :", src
        gather.only_new_tweets(ACCOUNT, src)

update()
