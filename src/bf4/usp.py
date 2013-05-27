#
# USP
#    Display:
#       - USP
#       - related tweets / FB-posts  (moderated)
#    MISSING: EA has to provide criteria for the stream.
#
# They want 5 USPs:
#   1. "Frostbite 3"
#   2. "Commander Mode"
#   3. "Amphibious Assault"
#   4. "Levolution"
#   5. "All-Out War"
#
# For each, the ability to:
#   - assign Tweets to a USP Ribbon element,
#   - enter in quotes (and attributions) manually.
#
# TODO: HOW TO DO THIS?
# Wish to have influencer quotes (e.g. celebrity tweets)
# appear more prominently than users-at-large.
#

from util import usp

FAKE_BRAND_LOGO = 'http://example.com/bf4.png'
BRAND = 'BF4'

def get_all():
    return [
        frostbite3(),
        commander_mode(),
        amphibious_assault(),
        levolution(),
        all_out_war()
    ]

def frostbite3():
    return usp.get_quotes(BRAND, 'Frostbite 3')

def commander_mode():
    return usp.get_quotes(BRAND, 'Commander Mode')

def amphibious_assault():
    return usp.get_quotes(BRAND, 'Amphibious Assault')

def levolution():
    return usp.get_quotes(BRAND, 'Levolution')

def all_out_war():
    return usp.get_quotes(BRAND, 'All-Out War')
