#
# FIFA, Madden, NBA, UFC
#
# VH: "info coming from EA this week"
#

def all_usps():
    return [fifa(), madden(), nba(), ufc()]

#---------------------

def fifa():
    return {
        'brand': {
            'name': 'FIFA',
            'logo': 'http://cms.com/img/fifa.png'
        },
        'usp': 'Some selling point text.',
        'quotes': [
            {
                'text': "It's great.",
                'person': {
                    'name': 'Some Dude',
                    'image': 'http://cms.com/img/some-dude.jpg'
                },
            },
            {
                'text': "It's freakin' great.",
                'person': {
                    'name': 'Other Dude',
                    'image': 'http://cms.com/img/other-dude.jpg'
                }
            }
        ]
    }

def madden():
    return {
        'brand': {
            'name': 'Madden',
            'logo': 'http://cms.com/img/madden.png'
        },
        'usp': 'Some selling point text.',
        'quotes': [
            {
                'text': "It's rad.",
                'person': {
                    'name': 'Nobody Dude',
                    'image': 'http://cms.com/img/nobody-dude.jpg'
                }
            }
        ]
    }

def nba():
    return {
        'brand': {
            'name': 'NBA',
            'logo': 'http://cms.com/img/nba.png'
        },
        'usp': 'Some selling point text.',
        'quotes': [
            {
                'text': "Que maco!",
                'person': {
                    'name': 'Mireia Aixala',
                    'image': 'http://cms.com/img/mireia.jpg'
                }
            },
            {
                'text': "Que guay!",
                'person': {
                    'name': 'Pedro Almodovar',
                    'image': 'http://cms.com/img/pedro.jpg'
                }
            },
            {
                'text': "Excellent!",
                'person': {
                    'name': 'Leonor Watling',
                    'image': 'http://cms.com/img/leonor.jpg'
                }
            }
        ]
    }

def ufc():
    return {
        'brand': {
            'name': 'UFC',
            'logo': 'http://cms.com/img/ufc.png'
        },
        'usp': 'Some selling point text.',
        'quotes': [
            {
                'text': "I dig it.",
                'person': {
                    'name': 'Barack Obama',
                    'profile': 'http://cms.com/img/obama.jpg'
                }
            }
        ]
    }

