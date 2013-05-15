import fetch
import store

def all_tweets(account, stream_name):
    """ :: String, String -> None
    Gather (fetch & store) all tweets ever.
    """
    gather_tweets(account, stream_name)

def only_new_tweets(account, stream_name):
    """ :: String, String -> None
    Gather (fetch & store) all tweets since the last time.
    """
    prev_newest_id = store.get_newest_id(stream_name)
    gather_tweets(account, stream_name, prev_newest_id=prev_newest_id)

def only_older_tweets(account, stream_name, prev_oldest_id):
    """ :: String, String, String -> None
    Gather (fetch & store) all tweets older than prev_oldest_id.
    """
    gather_tweets(account, stream_name, prev_oldest_id=prev_oldest_id)

#-- helpers --

def gather_tweets(account, stream_name, prev_oldest_id=None, prev_newest_id=None):
    """ :: String, String, String, String -> None
    Gather (fetch & store) all tweets.
    For prev_oldest_id or prev_newest_id, use at most 1.
    If neither, get all tweets.
    If prev_oldest_id, get only those older than prev_oldest_id.
    If prev_newest_id, get only those newer than prev_newest_id.
    """
    assert (prev_oldest_id is None or prev_newest_id is None)
    old_id = prev_oldest_id
    while True:
        # Get newest tweets <= old_id.
        tweets = fetch.stream(account, stream_name, start_id=old_id)
        if not tweets:
            break

        # If no old_id, then we've just grabbed the newest tweets,
        # so record the newest_id from this group.
        if old_id is None:
            store.set_newest_id(stream_name, get_newest_id(tweets))

        # If we got any tweets, store them.
        print ''
        print 'Num tweets:', len(tweets)
        store.put(stream_name, tweets)

        # Determine where to start next batch.
        old_id = get_oldest_id(tweets)
        print 'Oldest ID fetched: %s' % old_id

        # If have an ID older (smaller) than prev_newest_id, we're done.
        if prev_newest_id is not None and old_id <= prev_newest_id:
            print 'Reached prev_newest_id:', prev_newest_id
            break

# When {'reverse': False} ...

# ...the oldest tweet is at the *start* of the list.
def get_oldest_id(tweets):
    return tweets[0]['id_str']

# ...and the newest tweet is at the *end* of the list.
def get_newest_id(tweets):
    return tweets[-1]['id_str']

# def gone_back_enough(prev_newest_id, tweets):
#     """ Deprecated. """
#     return (prev_newest_id is not None   # So we can short-circuit.
#             and
#             prev_newest_id in (t['id_str'] for t in tweets))
    
