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

from util import store

FAKE_BRAND_LOGO = 'http://example.com/bf4.png'

FAKE_QUOTES = [
    {
        'profile_image': 'http://example.com/bob.jpg',
        'name': 'Bob Smith',
        'quote': "In the realm of online combat, Battlefield 4 provides thrills that few games can match."
    },
    
    {
        'profile_image': 'http://example.com/chris.jpg',
        'name': 'Chris Waters',
        'quote': "Battlefield 4 is a thrilling action game that immerses you in the chaos of combat like never before."
    },
    
    {
        'profile_image': 'http://example.com/jim.jpg',
        'name': 'Jim Jones',
        'quote': "Battlefield 4 boasts a fast-paced and thrilling campaign, as well as some of the most immersive and exciting multiplayer action ever seen on consoles."
    }
]


def get_all():
    return [
        frostbite3(),
        commander_mode(),
        amphibious_assault(),
        levolution(),
        all_out_war()
    ]

def frostbite3():
    return {
        'brand_logo': FAKE_BRAND_LOGO,
        'usp': 'Frostbite 3',
        'quotes': FAKE_QUOTES
    }

def commander_mode():
    return {
        'brand_logo': FAKE_BRAND_LOGO,
        'usp': 'Commander Mode',
        'quotes': FAKE_QUOTES
    }

def amphibious_assault():
    return {
        'brand_logo': FAKE_BRAND_LOGO,
        'usp': 'Amphibious Assault',
        'quotes': FAKE_QUOTES
    }

def levolution():
    return {
        'brand_logo': FAKE_BRAND_LOGO,
        'usp': 'Levolution',
        'quotes': FAKE_QUOTES
    }

def all_out_war():
    return {
        'brand_logo': FAKE_BRAND_LOGO,
        'usp': 'All-Out War',
        'quotes': FAKE_QUOTES
    }
