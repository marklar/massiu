#
# Minimalist lib for accessing entities from Mass Relevance.
# Requests response as gzipped JSON and returns as simple
# Py data structures (dict, list, etc.).
#

import requests
import json


ROOT_URL = 'http://tweetriver.com/'
API_KEY = 'abf59546eabec151a5565a81d8285ebf'  # stream mgnt API

stream_url = lambda acct, strm: '%s/%s/%s.json' % (ROOT_URL, acct, strm)
meta_url = lambda acct, strm: '%s/%s/%s/meta.json' % (ROOT_URL, acct, strm)
account_url = lambda acct: '%s/%s.json' % (ROOT_URL, acct)

#------------------

DEF_HEADERS = {'Accept-Encoding': 'gzip'}
def get_data(url, payload):
    """
    :: String, Dict -> Response data
    Make a request to MR.
    Assume it succeeds.
    Return the result data.
    """
    resp = requests.get(url, params = payload, headers = DEF_HEADERS)
    return json.loads(resp.text)

#------------------

def account(account_name):
    """
    :: String -> Response data
    Provides meta info for all streams in a single request.
    """
    url = account_url(account_name)
    payload = {}
    return get_data(url, payload)

def meta(account_name, stream_name):
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
        'sources': 1,  # shows keywords!
        'networks': True,
        'num_contributors': 5  # not enabled
    }
    return get_data(url, payload)

#------------------
#
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

def stream(account_name, stream_name, start_id=None):
    url = stream_url(account_name, stream_name)
    payload = {
        'start_id': start_id,
        'reverse': False,  # False: oldest come first.
        'replies': True,   # If reply, include orig Tweet in 'in_reply_to'?
        'limit': 200       # Default: 50.  Max: 200.
    }
    return get_data(url, payload)

