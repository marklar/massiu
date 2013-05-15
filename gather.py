import fetch
import store

def get_oldest_id(tweets):
    return tweets[0]['id_str']

def get_newest_id(tweets):
    return tweets[-1]['id_str']

def gone_back_enough(prev_newest_id, tweets):
    return prev_newest_id in (t['id_str'] for t in tweets)

def gather_tweets_newer_than(account, stream_name, prev_newest_id):
    """ :: String, String, String -> None
    Gather (fetch and store) all tweets newer than prev_newest_id.
    """
    return None

def gather_tweets(account_name, stream_name, old_id=None):
    """ :: String, String, String -> None
    Gather (fetch and store) all tweets older than old_id.
    """
    while True:
        print ''

        # Get newest tweets <= old_id.
        tweets = fetch.stream(account_name, stream_name, start_id=old_id)
        if not tweets:
            break

        # If old_id is None, then record the newest_id you see.
        newest_id = get_newest_id(tweets)
        if old_id is None:
            store.set_newest_id(stream_name, newest_id)

        # If any, store them.
        print "Num tweets:", len(tweets)
        store.put(stream_name, tweets)

        # Determine where to start next batch.
        old_id = get_oldest_id(tweets)
        print 'Oldest ID fetched: %s' % old_id
        # And remember how far back in time we got.
        store.set_oldest_id(stream_name, old_id)
