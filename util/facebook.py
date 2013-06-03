#
# Facebook "Likes" per account.
# 
# MISSING: EA to enumerate FB accounts.
#

import reqs

URL_ROOT = 'http://graph.facebook.com/'
KEYS = ['name', 'username', 'likes']

def get_likes(username):
    resp = reqs.get_data(URL_ROOT + username, {})
    return dict([(k, get_or_none(resp, k))
                 for k in KEYS])

#----------------

def get_or_none(dico, key):
    if key in dico:
        return dico[key]
    else:
        return None

if __name__ == '__main__':
    """ don't work: ['respawn', 'battlefield'] """
    usernames = [
        'respawn',               # None - placeholder
        'battlefield',           # None
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
    for u in usernames:
        print u
        print get_likes(u)
