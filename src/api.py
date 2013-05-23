import web
import json

import bf4.highlights
import bf4.usp
import ea.activity
import ea.featured
import ea.likes
import nfs.leaderboard
import nfs.featured
import pvz.photos
import pvz.featured
import sports.usp
import sports.featured

render = web.template.render('templates/')

URLS = (
    '/', 'Index',

    '/bf4/highlights',      'Bf4Highlights',
    '/bf4/usp',             'Bf4Usp',

    '/ea/activity',         'EaActivity',
    '/ea/featured',         'EaFeatured',
    '/ea/fb_likes',         'EaFbLikes',

    '/sports/usp',          'SportsUsp',
    '/sports/featured',     'SportsFeatured',

    # Do we want a separate endpoint for each hashtag?
    # Or just a single endpoint returning all of them?
    # '/sports/featured/feel_the_fight', 

    '/nfs/leaderboard',     'NfsLeaderboard',
    '/nfs/featured',        'NfsFeatured',

    '/pvz/photos',          'PvzPhotos',
    '/pvz/featured',        'PvzFeatured'
)

ENDPOINTS = [URLS[i] for i in range(2, len(URLS)-1, 2)]

j = lambda x: json.dumps(x)

class Index:
    def GET(self):
        return render.index(ENDPOINTS)

class Bf4Highlights:
    def GET(self):
        return j(bf4.highlights.highlights())

class Bf4Usp:
    """
    Canned data for now.
    Add more endpoints, one per USP?
    """
    def GET(self):
        return j(bf4.usp.get_all())

class EaActivity:
    def GET(self):
        return j(ea.activity.counts())

class EaFeatured:
    def GET(self):
        return j(ea.featured.get_ea())

class EaFbLikes:
    def GET(self):
        return j(ea.likes.get_likes())

class SportsUsp:
    def GET(self):
        """ TODO """
        return j(sports.usp.all_usps())

class SportsFeatured:
    def GET(self):
        """ TODO """
        return j(sports.featured.get_all())

class NfsLeaderboard:
    def GET(self):
        return j(nfs.leaderboard.top_times(5))

class NfsFeatured:
    def GET(self):
        """ TODO """
        return j(nfs.featured.featured())

class PvzPhotos:
    def GET(self):
        """ TODO """
        return j(pvz.photos.photos())

class PvzFeatured:
    def GET(self):
        """ TODO """
        return j(pvz.featured.featured())


if __name__ == "__main__": 
    app = web.application(URLS, globals())
    app.run()  

    
