#
# USP
#    Display:
#       - quote
#       - related tweets / FB-posts  (moderated)
#    MISSING: EA has to provide criteria for the stream.

from util import store

def usp():
    """
    ToDo:
        Pull this content from Mongo.
        Store pics and be able to serve the raw bits.
    """
    return {
        'brand_logo': None,
        'usp': 'online multiplayer!',
        'quotes': [
            {
                'profile_image': None,
                'name': 'Bob Smith',
                'quote': "In the realm of online combat, Battlefield 4 provides thrills that few games can match."
            },

            {
                'profile_image': None,
                'name': 'Chris Waters',
                'quote': "Battlefield 4 is a thrilling action game that immerses you in the chaos of combat like never before."
            },

            {
                'profile_image': None,
                'name': 'Jim Jones',
                'quote': "Battlefield 4 boasts a fast-paced and thrilling campaign, as well as some of the most immersive and exciting multiplayer action ever seen on consoles."
}
        ]
    }

