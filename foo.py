import requests
import pymongo
import json

ROOT_URL = 'http://tweetriver.com/'
ACCOUNT = 'MR_breel'
API_KEY = 'abf59546eabec151a5565a81d8285ebf'  # stream mgnt API
EA_HASHTAGS = [s.lower() for s in ['PVZ2E3', 'BF4', 'FIFA', 'MADDEN',
                                   'UFC', 'NBA', 'RESPAWN', 'NFS']]
EA_HASHTAGS_W_HASH = ['#' + s for s in EA_HASHTAGS]

#
# Get these advanced meta feature enabled?:
#  - Top retweeted tweets.
#  - Top contributors.
#

def stream_url(acct, strm, limit=None, since_id=None, start=None):
    """ String, String -> String """
    return '%s/%s/%s.json' % (ROOT_URL, acct, strm)

def meta_url(acct, strm):
    """ String, String -> String """
    return '%s/%s/%s/meta.json' % (ROOT_URL, acct, strm)

def account_url(acct):
    """ String -> String """
    return '%s/%s.json' % (ROOT_URL, acct)

DEF_HEADERS = {'Accept-Encoding': 'gzip'}
def get_data(url, payload):
    """ String, Dict -> Response data """
    resp = requests.get(url, params = payload, headers = DEF_HEADERS)
    # return r.text.encode('utf-8')
    return json.loads(resp.text)

def get_account(account_name):
    """ String -> Response data
    Provides meta info for all streams in a single request. """
    url = account_url(account_name)
    payload = {}
    return get_data(url, payload)

def get_meta(account_name, stream_name):
    """ String, String -> Response data
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
        'sources': 1,  # shows keywords!
        'networks': True,
        'num_contributors': 5  # not enabled
    }
    return get_data(url, payload)

# Store info about most-recent entity (i.e. its ID).
def get_stream(account_name, stream_name):
    """ String, String -> Response data
    limit : max: 200
    since_id : Only entities *newer* than the supplied since_id
    reverse : return items in reverse order?
    replies : If a reply, include its replied-to Tweet in 'in_reply_to'?
    geo_hint : If lacking, attempt to populate geo location data from author's profile info.
    """
    url = stream_url(account_name, stream_name)
    payload = {
        'reverse': True,
        'replies': True,
        'limit': 200   # default: 50.  max: 200.
    }
    return get_data(url, payload)

def get_oldest_tweets():
    return 1

def has_hashtag(tweet, hashtag):
    """ Tweet, String -> Boolean """
    tags = [tag['text'].lower() for tag in tweet['entities']['hashtags']]
    return hashtag in tags

def get_tweets_with_hashtag(hashtag, tweets):
    """ Filter """
    # return (t in for t in tweets if has_hashtag(t, hashtag))
    return filter(lambda t: has_hashtag(t, hashtag),
                  tweets)

def get_hashtags(tweet):
    return [e['text'].lower() for e in tweet['entities']['hashtags']]

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
    all_tweets = get_stream(ACCOUNT, 'ea_activity')

    print 'How many tweets?'
    print len(all_tweets)
    print ''
    print 'hashtags:'
    for tw in all_tweets:
        hts = get_hashtags(tw)
        print hts
        if len(hts) == 0:
            print tw
            print ''
    print ''

    # And can perform filtering and counting w/ Mongo queries.
    counts = {}
    for ht in EA_HASHTAGS:
        tag_tweets = get_tweets_with_hashtag(ht, all_tweets)
        counts[ht] = len(tag_tweets)
    return counts

stream_name = 'nfs_leaderboard'
# resp_data = get_account(ACCOUNT)
# resp_data = get_meta(ACCOUNT, stream_name)
# resp_data = get_stream(ACCOUNT, stream_name)

print ea_activity()
