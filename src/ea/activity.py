#
# Uses a single MR stream ('ea_activity')
# to gather tweets for multiple hashtags,
# then counts them.
#

import re
from util import store

STREAM_NAME = 'ea_activity'

HASHTAGS = [
    'bf4', 'eae3', 'needforspeed', 'pvzgw',
    'respawn', 'fifa14', 'MaddenNext25',
    'WeAreLive', 'FeelTheFight',
    'EASportsIgnite', 'CommandAndConquer'
]

def make_re(hashtag):
    return re.compile("^%s$" % hashtag, re.IGNORECASE)

REGEXES = {}
for h in HASHTAGS:
    REGEXES[h] = make_re(h)

def counts():
    """ () -> {tag: count}
    Number of Tweets for each title's hashtag.

    With MR's "Compare API", one can do this:
    http://dev.massrelevance.com/docs/api/v1.0/compare/
    But only so long as each hashtag has its own stream.

    Since we have all these hashtags in a single stream,
    we'll need to collect the Tweets and perform our own counts.
    """
    counts = {}
    for name, rex in REGEXES.iteritems():
        counts[name] = store.count_hashtags(STREAM_NAME, rex)
    return counts

