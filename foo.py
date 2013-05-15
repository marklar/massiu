import re
from gather import gather_tweets
import hashtags
import store

ACCOUNT = 'MR_breel'
API_KEY = 'abf59546eabec151a5565a81d8285ebf'  # stream mgnt API
EA_HASHTAGS = [s.lower() for s in ['PVZ2E3', 'BF4', 'FIFA', 'MADDEN',
                                   'UFC', 'NBA', 'RESPAWN', 'NFS']]
EA_HASHTAGS_W_HASH = ['#' + s for s in EA_HASHTAGS]

def ea_activity():
    """ () -> {tag: count}
    Number of Tweets for each title's hashtag.

    With MR's "Compare API", one can do this:
    http://dev.massrelevance.com/docs/api/v1.0/compare/
    But only so long as each hashtag has its own stream.

    Since we have all these hashtags in a single stream,
    we'll need to collect the Tweets and perform our own counts.
    """
    #! MR will include the Tweet even if it matches
    #! by virtue of the "retweeted-status".

    # Actually, the tweets should come from Mongo.
    all_tweets = fetch.store_all_tweets(ACCOUNT, 'ea_activity')
    hashtags.show_tweets(all_tweets)

    # And can perform filtering and counting w/ Mongo queries.
    counts = {}
    for ht in EA_HASHTAGS:
        tag_tweets = hashtags.filter_by_hashtag(all_tweets, ht)
        counts[ht] = len(tag_tweets)
    return counts

# stream_name = 'nfs_leaderboard'
# resp_data = fetch.account(ACCOUNT)
# resp_data = fetch.meta(ACCOUNT, stream_name)
# resp_data = fetch.stream(ACCOUNT, stream_name)

for src in ['ea_activity', 'pvz', 'respawn']:
    print "--SRC-- :", src
    gather_tweets(ACCOUNT, src)

def make_re(hashtag):
    return re.compile("^%s$" % hashtag, re.IGNORECASE)

REGEXES = {
    'nba': make_re('nba'),
    'fifa': make_re('fifa')
}

def ea_counts():
    counts = {}
    for name, rex in REGEXES.iteritems():
        counts[name] = store.count_hashtags('ea_activity', rex)
    return counts
        
print ea_counts()

