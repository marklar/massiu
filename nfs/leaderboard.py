#
# Pull leaderboard tweets from MongoDB.
# Extract name, time pairs from text:
#     "<name>: <mins>:<secs>.<fractions>"
# Make ordered list, based on times.
#
# Question: Maybe it's <hours>:<mins>:<secs> without fractions?
#

import re
from util import store

STREAM_NAME = 'nfs_leaderboard'

FAKE_TWEETS = [
    {'text': " Random Dude : 2:32.10  "},
    {'text': " Joan Maragall : 4:32.10  "},
    {'text': " Andres Iniesta : 5:32.10  "},
    {'text': " Dani Alves : 1:32.10  "},
    {'text': " Xavi : 3:32.10  "},
    {'text': " Sergi Busquets : 8:32.10  "},
    {'text': " Artur Mas : 0:32.10  "}
]

def top_times(num):
    """
    :: Int -> [{'name': ..., 'time_str': ...}]
    """
    # FIXME!!!
    #?? gather.only_new_tweets(STREAM_NAME)
    # tweets = store.get_all(STREAM_NAME)
    tweets = FAKE_TWEETS
    return select_top_times(num, tweets)

#--------------------------

regex = re.compile(
    r"""^\s*
        ([^:]+)        # name - no colons
        :              # colon separator
        \s*
        (              # time...
         (\d+)         # minutes
         :          
         (\d+.\d+)     # seconds
        )              # ...time
        \s*$""",
    re.X)

def get_name_and_time(tweet):
    m = regex.match(tweet['text'])
    name = m.group(1).strip()
    time_str = m.group(2)
    mins = int(m.group(3))
    secs = float(m.group(4))
    return {
        'name': name,
        'time_str': time_str,
        'secs': (mins * 60) + secs   # for comparisons
    }

def select_top_times(num, tweets):
    """
    :: Int, [Tweet] -> [{'name': ..., 'time_str': ...}]
    """
    names_w_times = (get_name_and_time(t) for t in tweets)
    by_time = lambda a: a['secs']
    ordered = sorted(names_w_times, key=by_time)[0:num]
    for t in ordered:
        del t['secs']
    return ordered

# print top_times(3)
