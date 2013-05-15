import fetch
import store

def get_oldest_id(tweets):
    # Or is this 0?
    return tweets[-1]['id_str']

def get_newest_id(tweets):
    return tweets[0]['id_str']

def gone_back_enough(prev_newest_id, tweets):
    return prev_newest_id in (t['id_str'] for t in tweets)
    
def gather_tweets(account_name, stream_name):
    """ String, String, Int, Int -> None

    Used to gather tweets from Mass Relevance.
    Get all tweets down to prev_newest_id_fetched.
    The first time you call it, just get them all.
    After that, check to see what low_id you have and include it.
    """
    prev_newest_id = store.get_newest_id(stream_name)
    
    tweets = fetch.stream(account_name, stream_name)
    if not tweets:
        return
    print "num tweets:", len(tweets)

    # If any...
    # Store them.
    store.put(stream_name, tweets)
    # For next time, remember the newest one we've gotten.
    store.set_newest_id(stream_name, get_newest_id(tweets))

    # Got enough?  Stop.
    if gone_back_enough(prev_newest_id, tweets):
        return

    # Where to start.
    old_id = get_oldest_id(tweets)
    while True:

        # Get newest tweets <= newest_id.
        tweets = fetch.stream(account_name, stream_name,
                              start_id=old_id)
        if not tweets:
            break
        print "num tweets:", len(tweets)
        # If any, store them.
        store.put(stream_name, tweets)

        # Got enough?  Stop.
        if gone_back_enough(prev_newest_id, tweets):
            break

        # Determine where to start next batch.
        old_id = get_oldest_id(tweets)
        print 'Oldest ID fetched: %s' % old_id
