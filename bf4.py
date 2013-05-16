import gather
import store

COLL_NAME = 'bf4'

def bf4_counts():
    """
    time frames:
      - This week
      - Today
      - This hour
    """

    ##
    ## ToDo: Use Twitter API to search for tweets, too.
    ##

    gather.only_new_tweets(COLL_NAME)
    tweets = store.get_all(COLL_NAME)
    dates = (t['created_at'] for t in tweets)
    for d in dates:
        print d

# bf4_counts()
