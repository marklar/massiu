#
# Uses a single MR stream ('ea_activity')
# to gather tweets for multiple hashtags,
# then counts the tweets per hashtag.
#

from util import store
from util import hashtags
import string

STREAM_NAME = 'ea_activity'

HASHTAGS = [
    'bf4', 'eae3', 'NeedForSpeed', 'pvzgw',
    'respawn', 'fifa14', 'MaddenNext25',
    'WeAreLive', 'FeelTheFight',
    'EASportsIgnite', 'CommandAndConquer'
]
# LOW_HASHTAGS = [h.lower() for h in HASHTAGS]

MAP_FN = """
function() {
    var tags = [
        'bf4', 'eae3', 'needforspeed', 'pvzgw', 'respawn',
        'fifa14', 'maddennext25', 'wearelive', 'feelthefight',
        'easportsignite', 'commandandconquer'
    ]
    var t;
    this.entities.hashtags.forEach(function(tag) {
        t = tag.text.toLowerCase();
        if (tags.indexOf(t) > -1) {
            emit(t, 1);
        }
    });
}
"""

REDUCE_FN = """
function(_, values) {
    var tot = 0;
    values.forEach(function(v) {
        tot += v;
    });
    return tot;
}
"""

def val_or_0(dico, key):
    try:
        v = dico[key]
        del dico[key]
        return v
    except KeyError:
        return 0

def new_counts():
    results = store.get_db()[STREAM_NAME].map_reduce(MAP_FN, REDUCE_FN, 'xyz')
    tag_2_count = [(r['_id'], int(r['value']))
                   for r in results.find()]
    dico = dict(tag_2_count)
    v = val_or_0
    new_dico = {}
    for t in HASHTAGS:
        new_dico['#' + t] = v(dico, t.lower())
    return new_dico


def counts():
    """ () -> {tag: count}
    Number of Tweets for each title's hashtag.

    With MR's "Compare API", one can do this:
    http://dev.massrelevance.com/docs/api/v1.0/compare/
    But only so long as each hashtag has its own stream.

    Since we have all these hashtags in a single stream,
    we'll need to collect the Tweets and perform our own counts.
    """
    tag_2_count = [
        ('#' + h, store.count_hashtag(STREAM_NAME, h))
        for h in HASHTAGS
    ]
    return dict(tag_2_count)
