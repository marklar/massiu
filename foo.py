import fetch
import store

ACCOUNT = 'MR_breel'
API_KEY = 'abf59546eabec151a5565a81d8285ebf'  # stream mgnt API
EA_HASHTAGS = [s.lower() for s in ['PVZ2E3', 'BF4', 'FIFA', 'MADDEN',
                                   'UFC', 'NBA', 'RESPAWN', 'NFS']]
EA_HASHTAGS_W_HASH = ['#' + s for s in EA_HASHTAGS]

def get_hashtags(tweet):
    return [tag['text'].lower() for tag in tweet['entities']['hashtags']]

def has_hashtag(tweet, hashtag):
    """ Tweet, String -> Boolean """
    return hashtag in get_hashtags(tweet)

def filter_by_hashtag(tweets, hashtag):
    return filter(lambda t: has_hashtag(t, hashtag),
                  tweets)

def show_tweets(tweets):
    print 'How many tweets?'
    print len(tweets)
    print ''
    print 'hashtags:'
    for tw in tweets:
        hts = get_hashtags(tw)
        print hts
        # if len(hts) == 0:
        if True:
            print tw
            print ''
    print ''

def get_earliest_id(tweets):
    return min(t['id'] for t in tweets)

def fetch_and_store_all_tweets(account_name, stream_name):
    """ String, String -> None
    First, grab the newest ones.
    Get the earliest ID out of that collection.
    Then, use 'start_id' to get the previous collection.
    Again, get its earliest ID...
    """
    low_id = None
    while True:
        tweets = fetch.stream(account_name, stream_name, start_id=low_id)
        if not tweets:
            break
        store.put(stream_name, tweets)
        low_id = get_earliest_id(tweets)
        print 'Low ID: %s' % low_id

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
    show_tweets(all_tweets)

    # And can perform filtering and counting w/ Mongo queries.
    counts = {}
    for ht in EA_HASHTAGS:
        tag_tweets = filter_by_hashtag(all_tweets, ht)
        counts[ht] = len(tag_tweets)
    return counts

stream_name = 'nfs_leaderboard'
# resp_data = fetch.account(ACCOUNT)
# resp_data = fetch.meta(ACCOUNT, stream_name)
# resp_data = fetch.stream(ACCOUNT, stream_name)

# fetch_and_store_all_tweets(ACCOUNT, 'ea_activity')
# fetch_and_store_all_tweets(ACCOUNT, 'pvz')
fetch_and_store_all_tweets(ACCOUNT, 'respawn')
