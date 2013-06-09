#
# EA - Facebook likes
#
# Accounts:
#   facebook.com/commandandconquer
#   facebook.com/respawn (placeholder until 6/10)
#   facebook.com/battlefield
#   facebook.com/needforspeed
#   facebook.com/ea
#   facebook.com/EASportsMaddenNFL
#   facebook.com/easportsfifa
#   facebook.com/EASPORTSUFC
#   facebook.com/EASPORTSNBA
#   facebook.com/plantsversuszombies
#

import re
from util import facebook

USERNAMES = [
    # 'respawn',               # None - placeholder
    # 'Battlefield',           # None
    'commandandconquer',
    'needforspeed',
    'ea',
    'EASportsMaddenNFL',
    'easportsfifa',
    'EASPORTSUFC',
    'EASPORTSNBA',
    'plantsversuszombies'
]

def get():
    accounts = [facebook.get_likes(n) for n in USERNAMES]
    for a in accounts:
        a['name'] = re.sub('EA SPORTS ', 'EA SPORTS\n', a['name'])
        a['name'] = re.sub('Command \& Conquer', 'Command&Conquer', a['name'])
    accounts.append({
        'username': 'Battlefield',
        'name': 'Battlefield',
        'likes': 4858050
    })
    return accounts
