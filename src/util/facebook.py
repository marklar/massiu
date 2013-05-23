#
# Facebook "Likes" per account.
# 
# MISSING: EA to enumerate FB accounts.
#

import reqs

def get_likes(username):
    url = 'http://graph.facebook.com/' + username
    resp = reqs.get_data(url, {})
    return {
        'username': get_or_none(resp, 'username'),
        'likes':    get_or_none(resp, 'likes')
    }

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
