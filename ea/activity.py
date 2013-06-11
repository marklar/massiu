from util import store
from util import hashtags
from util import fetch
import string

TAG_2_STREAM = {
    'BF4': 'bf4_highlights',
    'EAE3': 'ea_featured',
    'PvZGW': 'pvz_featured',
    'FIFA14': 'sports_fifa14_featured',
    'Titanfall': 'titanfall_activity',
    'WeAreLive': 'sports_wearelive_featured',
    'NeedForSpeed': 'nfs_featured',
    'MaddenNext25': 'sports_maddennext25_featured',
    'FeelTheFight': 'sports_feelthefight_featured',
    'EASPORTSIGNITE': 'sports_easportsignite_featured',
    'CommandAndConquer': 'command_and_conquer_activity'
}

def counts():
    return dict([(k, get_daily_count(v))
                 for k,v in TAG_2_STREAM.iteritems()])

def get_daily_count(stream):
    metadata = fetch.meta(stream)
    # hourly = metadata['activity']['hourly']['total'][0]
    daily = metadata['activity']['daily']['total'][0]
    return daily

#
# Uses a single MR stream ('ea_activity')
# to gather tweets for multiple hashtags,
# then counts the tweets per hashtag.
#

HASHTAGS = [
    'BF4',
    'EAE3',
    'NeedForSpeed',
    'PvZGW',
    'Titanfall',
    'FIFA14',
    'MaddenNext25',
    'WeAreLive',
    'FeelTheFight',
    'EASPORTSIGNITE',
    'CommandAndConquer'
]

STREAM_NAME = 'ea_activity'

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

def old_counts():
    results = store.get_db()[STREAM_NAME].map_reduce(MAP_FN, REDUCE_FN, 'xyz')
    tag_2_count = [(r['_id'], int(r['value']))
                   for r in results.find()]
    dico = dict(tag_2_count)
    v = val_or_0
    new_dico = {}
    for t in HASHTAGS:
        new_dico['#' + t] = v(dico, t.lower())
    return new_dico
