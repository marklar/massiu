#
# Fetch data (tweets) from Mass Relevance.
# Store data in MongoDB.
#

import fetch
import store

def all_tweets(stream_name, account=fetch.ACCOUNT_NAME):
    """ :: String, String -> None
    Gather (fetch & store) all tweets ever.
    """
    gather_tweets(stream_name, account)

def only_new_tweets(stream_name, account=fetch.ACCOUNT_NAME):
    """ :: String, String -> None
    Gather (fetch & store) all tweets since the last time.
    """
    prev_newest_id = store.get_max_id_str(stream_name)
    gather_tweets(stream_name, account, prev_newest_id=prev_newest_id)

def only_older_tweets(stream_name, account=fetch.ACCOUNT_NAME):
    """ :: String, String -> None
    Gather (fetch & store) all tweets older than prev_oldest_id.
    """
    prev_oldest_id = store.get_min_id_str(stream_name)
    gather_tweets(stream_name, account, prev_oldest_id=prev_oldest_id)


#-- helpers --

def gather_tweets(stream_name, account,
                  prev_oldest_id=None,
                  prev_newest_id=None):
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
        tweets = fetch.stream(stream_name,
                              account_name=account,
                              start_id=old_id)
        if not tweets:
            break

        # If we got any tweets, store them.
        store.put_tweets(stream_name, tweets)

        # Determine where to start next batch.
        old_id = get_oldest_id(tweets)
        # print 'Oldest ID fetched: %s' % old_id

        # If have an ID older (smaller) than prev_newest_id, we're done.
        if prev_newest_id is not None and old_id <= prev_newest_id:
            # print 'Reached prev_newest_id:', prev_newest_id
            break

# When {'reverse': False} ...

# ...the oldest tweet is at the *start* of the list.
def get_oldest_id(tweets):
    return tweets[0]['id_str']

# ...and the newest tweet is at the *end* of the list.
def get_newest_id(tweets):
    return tweets[-1]['id_str']
