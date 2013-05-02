import requests
import pymongo

# -- Config --
cfg = {
    'root_url' : 'http://tweetriver.com/',
    'account_name' : 'MR_breel',
    'key': 'abf59546eabec151a5565a81d8285ebf' # for stream management API
}

#
# Get these advanced meta feature enabled?:
#  - Top retweeted tweets.
#  - Top contributors.


def stream_url(acct, strm, limit=None, since_id=None, start=None):
    return '%s/%s/%s.json' % (cfg['root_url'], acct, strm)

def meta_url(acct, strm):
    return '%s/%s/%s/meta.json' % (cfg['root_url'], acct, strm)

def account_url(acct):
    return '%s/%s.json' % (cfg['root_url'], acct)

def get_account(account_name):
    """ Provides meta info for all streams in a single request. """
    url = account_url(account_name)
    payload = {}
    r = requests.get(url, params = payload)
    print r.text

def get_meta(account_name, stream_name):
    """
    activity:
      num_minutes : how many 'minute'
      num_days : how many 'daily'
    advanced:
      num_trends : "trends" - number of top and total trends
      num_hashtags : "hashtag tracking" - number of developing hashtags
      num_contributors : "contributor tracking" - number of top contributor handles
    """
    url = meta_url(account_name, stream_name)
    payload = {
        'networks': True,
        'num_contributors': 5  # not enabled
    }
    r = requests.get(url, params = payload)
    print r.text


# Store info about most-recent entity (i.e. its ID).
def get_stream(account_name, stream_name):
    """
    limit : max: 200
    since_id : Only entities *newer* than the supplied since_id
    reverse : return items in reverse order?
    replies : If a reply, include its replied-to Tweet in 'in_reply_to'?
    geo_hint : If lacking, attempt to populate geo location data from author's profile info.
    """
    url = stream_url(account_name, stream_name)
    payload = {
        'reverse': True,
        'replies': True
    }
    r = requests.get(url, params = payload)
    print r.text

stream_name = 'pvz'
# get_stream(cfg['account_name'], stream_name)
# get_meta(cfg['account_name'], stream_name)
get_account(cfg['account_name'])
