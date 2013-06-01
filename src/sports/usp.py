#
# FIFA, Madden, NBA, UFC
#

from util import usp

FAKE_BRAND_LOGO = 'http://example.com/sports.png'
BRAND = 'Sports'

# def all_usps():
#     return [fifa(), madden(), nba(), ufc()]

def ignite_human_intelligence():
    return usp.get_quotes(BRAND, 'IGNITE: Human Intelligence')

def ignite_true_player_motion():
    return usp.get_quotes(BRAND, 'IGNITE: True Player Motion')

def ignite_living_worlds():
    return usp.get_quotes(BRAND, 'IGNITE: Living Worlds')

def fifa():
    return usp.get_quotes(BRAND, 'FIFA 14 Is Alive')

def madden():
    return usp.get_quotes(BRAND, 'Madden: See It. Feel It. Live It.')

def nba():
    # TODO: Fix this USP.
    return usp.get_quotes(BRAND, 'NBA')

def ufc():
    return usp.get_quotes(BRAND, 'UFC: Feel the Fight')
