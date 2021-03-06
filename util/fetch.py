#
# Minimalist lib for accessing entities from Mass Relevance.
# Requests response as gzipped JSON and returns as simple
# Py data structures (dict, list, etc.).
#

import reqs

ACCOUNT_NAME = 'MR_breel'

# Usage of `since_id` and `start_id` is mutually exclusive;
# only one of these parameters may be used in a single request.
#
# since_id :: string
# Tweet ID (e.g.: 255682528302747648)
# Fetch only Tweets approved AFTER this one, getting newer ones first.
#
# start_id :: string
# Tweet ID: (e.g.: 255682528302747648)
# Fetch Tweets approved BEFORE this one.  (i.e. "more", going back in time)
# Supply the 'id' of the last viewed entity to request
# the set of entities that came before it in the stream.
#
def stream(stream_name, account_name=ACCOUNT_NAME, start_id=None, limit=200):
    url = stream_url(account_name, stream_name)
    payload = {
        'start_id': start_id,
        'reverse': False,  # False: oldest come first.
        'replies': True,   # If reply, include orig Tweet in 'in_reply_to'?
        'limit': limit     # Default: 50.  Max: 200.
    }
    return reqs.get_data(url, payload)

def account(account_name=ACCOUNT_NAME):
    """
    :: String -> Response data
    Provides meta info for all streams in a single request.
    """
    url = account_url(account_name)
    payload = {}
    return reqs.get_data(url, payload)

MINS_IN_DAY = 24 * 60

def get_minutes(stream, num_minutes=MINS_IN_DAY):
    metadata = meta(stream, num_minutes=num_minutes)
    # The END of the list of numbers is the most recent data.
    # So we turn it around to work with the FRONT of the list.
    minutes = metadata['activity']['minute']['total']
    minutes.reverse()
    return minutes

def meta(stream_name, account_name=ACCOUNT_NAME, num_minutes=MINS_IN_DAY):
    """
    :: String, String -> Response data
    activity:
      num_minutes: how many 'minute'
      num_days: how many 'daily'
    advanced:
      num_trends: "trends" - number of top and total trends
      num_hashtags: "hashtag tracking" - number of developing hashtags
      num_contributors: "contributor tracking" - number of top contributor handles
    """
    url = meta_url(account_name, stream_name)
    payload = {
        'activity': 1,   # activity & count properties
        'num_hours': 1,
        'num_minutes': num_minutes,
        'num_days': 1,
        'sources': 1,  # shows keywords!
        'networks': True,
        'num_contributors': 5  # not enabled
    }
    return reqs.get_data(url, payload)


#------------------

ROOT_URL = 'http://tweetriver.com/'
stream_url = lambda acct, strm: '%s/%s/%s.json' % (ROOT_URL, acct, strm)
meta_url = lambda acct, strm: '%s/%s/%s/meta.json' % (ROOT_URL, acct, strm)
account_url = lambda acct: '%s/%s.json' % (ROOT_URL, acct)

