#
# Hashtags have changed.
# '#bf4' is the only one remaining.
# Blow away old version of this collection and start anew.
#

import re
import store

#-----------
# Activity  

ACTIVITY_STREAM_NAME = 'ea_activity'

OLD_EA_HASHTAGS = ['pvz2e3', 'bf4', 'fifa', 'madden',
               'ufc', 'nba', 'respawn', 'nfs']

EA_HASHTAGS = ['bf4', 'eae3', 'needforspeed', 'pvzgw']
EA_HASHTAGS_W_HASH = ['#' + s for s in EA_HASHTAGS]

def make_re(hashtag):
    return re.compile("^%s$" % hashtag, re.IGNORECASE)

EA_REGEXES = {}
for h in EA_HASHTAGS:
    EA_REGEXES[h] = make_re(h)

def ea_counts():
    """ () -> {tag: count}
    Number of Tweets for each title's hashtag.

    With MR's "Compare API", one can do this:
    http://dev.massrelevance.com/docs/api/v1.0/compare/
    But only so long as each hashtag has its own stream.

    Since we have all these hashtags in a single stream,
    we'll need to collect the Tweets and perform our own counts.
    """
    counts = {}
    for name, rex in EA_REGEXES.iteritems():
        counts[name] = store.count_hashtags(ACTIVITY_STREAM_NAME, rex)
    return counts

#------------------
# Featured tweets

# More may be added later.
# Use fetch.meta() to get keywords for stream meta-info.
EA_FEATURED_HASHTAGS = ['eae3']
