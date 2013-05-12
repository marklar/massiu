#
# Pull leaderboard tweets from MongoDB.
# Extract name, time pairs from text:
#     "<name>: <mins>:<secs>.<fractions>"
# Make ordered list, based on times.
#

import re
import store

regex = re.compile("^\s*([^:]+):\s*((\d+):(\d+.\d+))\s*$")
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

def top_times(num, tweets):
    names_w_times = (get_name_and_time(t) for t in tweets)
    by_time = lambda a: a['secs']
    ordered = sorted(names_w_times, key=by_time)[0:num]
    for t in ordered:
        del t['secs']
    return ordered

#-------------------


# tweets = store.get_all('pvz')
tweets = [
    {'text': " Aaaa Wong : 2:32.10  "},
    {'text': " Bbbb Wong : 4:32.10  "},
    {'text': " Cccd Wong : 5:32.10  "},
    {'text': " Dddd Wong : 1:32.10  "},
    {'text': " Eeee Wong : 3:32.10  "},
    {'text': " Ffff Wong : 8:32.10  "},
    {'text': " Gggg Wong : 0:32.10  "}
]

print top_times(2, tweets)
