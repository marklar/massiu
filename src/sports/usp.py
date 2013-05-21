#
# FIFA, Madden, NBA, UFC
#
# VH: "info coming from EA this week"
#

def all_usps():
    return [fifa_usp(), madden_usp(), nba_usp(), ufc_usp()]

#---------------------

def fifa_usp():
    return {
        'name': 'fifa',
        'brand_logo': 'http://example.com/fifa.png',
        'usp': 'Some selling point text.',
        'quotes': [
            {
                'profile_image': 'http://example.com/some-dude.jpg',
                'name': 'Some Dude',
                'quote': "It's great."
            },
            {
                'profile_image': 'http://example.com/other-dude.jpg',
                'name': 'Other Dude',
                'quote': "It's freakin' great."
            }
        ]
    }

def madden_usp():
    return {
        'name': 'madden',
        'brand_logo': 'http://example.com/madden.png',
        'usp': 'Some selling point text.',
        'quotes': [
            {
                'profile_image': 'http://example.com/nobody-dude.jpg',
                'name': 'Nobody Dude',
                'quote': "It's rad.."
            }
        ]
    }

def nba_usp():
    return {
        'name': 'nba',
        'brand_logo': 'http://example.com/nba.png',
        'usp': 'Some selling point text.',
        'quotes': [
            {
                'profile_image': 'http://example.com/mireia.jpg',
                'name': 'Mireia Aixala',
                'quote': "Que maco!"
            },
            {
                'profile_image': 'http://example.com/pedro.jpg',
                'name': 'Pedro Almodovar',
                'quote': "Que guay!"
            },
            {
                'profile_image': 'http://example.com/leonor.jpg',
                'name': 'Leonor Watling',
                'quote': "Excellent!"
            }
        ]
    }

def ufc_usp():
    return {
        'name': 'ufc',
        'brand_logo': 'http://example.com/ufc.png',
        'usp': 'Some selling point text.',
        'quotes': [
            {
                'profile_image': 'http://example.com/obama.jpg',
                'name': 'Barack Obama',
                'quote': "I dig it."
            }
        ]
    }

