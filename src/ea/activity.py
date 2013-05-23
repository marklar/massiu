#
# Uses a single MR stream ('ea_activity')
# to gather tweets for multiple hashtags,
# then counts them.
#

from util import store
from util import hashtags

STREAM_NAME = 'ea_activity'

HASHTAGS = [
    'bf4', 'eae3', 'NeedForSpeed', 'pvzgw',
    'respawn', 'fifa14', 'MaddenNext25',
    'WeAreLive', 'FeelTheFight',
    'EASportsIgnite', 'CommandAndConquer'
]

TAG_W_REGEX = [(h, hashtags.make_re(h)) for h in HASHTAGS]

def counts():
    """ () -> {tag: count}
    Number of Tweets for each title's hashtag.

    With MR's "Compare API", one can do this:
    http://dev.massrelevance.com/docs/api/v1.0/compare/
    But only so long as each hashtag has its own stream.

    Since we have all these hashtags in a single stream,
    we'll need to collect the Tweets and perform our own counts.
    """
    tag_2_count = [('#' + name, store.count_hashtag(STREAM_NAME, rex))
                   for name, rex in TAG_W_REGEX]
    return dict(tag_2_count)
