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
    'BF4',
    'EAE3',
    'NeedForSpeed',
    'PvZGW',
    'Titanfall',
    'FIFA14',
    'MaddenNext25',
    'WeAreAlive',
    'FeelTheFight',
    'EASPORTSIGNITE',
    'CommandAndConquer'
]

MAP_FN = """
function() {
    var tags = [
        'bf4', 'eae3', 'needforspeed', 'pvzgw', 'titanfall',
        'fifa14', 'maddennext25', 'wearelive', 'feelthefight',
        'easportsignite', 'commandandconquer'
    ];
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

def counts():
    results = store.get_db()[STREAM_NAME].map_reduce(MAP_FN, REDUCE_FN, 'xyz')
    tag_2_count = [(r['_id'], int(r['value']))
                   for r in results.find()]
    dico = dict(tag_2_count)
    v = val_or_0
    new_dico = {}
    for t in HASHTAGS:
        new_dico['#' + t] = v(dico, t.lower())
    return new_dico
