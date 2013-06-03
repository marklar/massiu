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

from util import facebook

USERNAMES = [
    # 'respawn',               # None - placeholder
    # 'battlefield',           # None
    'OfficialBattlefield4',
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
    return [facebook.get_likes(n) for n in USERNAMES]
