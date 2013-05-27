#
# FIFA, Madden, NBA, UFC
#

from util import usp

FAKE_BRAND_LOGO = 'http://example.com/sports.png'
BRAND = 'Sports'

def all_usps():
    return [fifa(), madden(), nba(), ufc()]

# TODO: Fix USPs below.

def fifa():
    return usp.get_quotes(BRAND, 'FIFA')

def madden():
    return usp.get_quotes(BRAND, 'Madden')

def nba():
    return usp.get_quotes(BRAND, 'NBA')

def ufc():
    return usp.get_quotes(BRAND, 'UFC')
