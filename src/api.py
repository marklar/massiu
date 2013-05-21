import web
import json

import bf4.highlights
import bf4.usp
import ea.activity
import ea.featured
import nfs.leaderboard
import pvz.photos
import pvz.featured
import nfs.featured

render = web.template.render('templates/')

URLS = (
    '/', 'Index',

    '/bf4/highlights',      'Bf4Highlights',
    '/bf4/usp',             'Bf4Usp',

    '/ea/activity',         'EaActivity',
    '/ea/featured',         'EaFeatured',
    '/ea/fb_likes',         'EaFbLikes',

    '/ea_sports/usp',       'EaSportsUsp',
    '/ea_sports/featured',  'EaSportsFeatured',

    '/nfs/leaderboard',     'NfsLeaderboard',
    '/nfs/featured',        'NfsFeatured',

    '/pvz/photos',          'PvzPhotos',
    '/pvz/featured',        'PvzFeatured'
)

ENDPOINTS = [URLS[i] for i in range(2, len(URLS)-1, 2)]

class Index:
    def GET(self):
        return render.index(ENDPOINTS)

j = lambda x: json.dumps(x)

class Bf4Highlights:
    def GET(self):
        return j(bf4.highlights.highlights())

class Bf4Usp:
    def GET(self):
        return j(bf4.usp.usp())

class EaActivity:
    def GET(self):
        return j(ea.activity.counts())

class EaFeatured:
    def GET(self):
        """ TODO """
        return j(ea.featured.featured())

class EaFbLikes:
    def GET(self):
        """ TODO """
        return j(None)

class EaSportsUsp:
    def GET(self):
        """ TODO """
        return j(None)

class EaSportsFeatured:
    def GET(self):
        """ TODO """
        return j(None)

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

    
