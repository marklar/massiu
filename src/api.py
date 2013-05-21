import web
import json

import bf4_highlights
import bf4_usp
import ea_activity
import ea_featured
import nfs_leaderboard
import pvz_photos
import pvz_featured
import nfs_featured

render = web.template.render('templates/')

urls = (
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

ENDPOINTS = [
    '/bf4/highlights',
    '/bf4/usp',

    '/ea/activity',
    '/ea/featured',
    '/ea/fb_likes',

    '/ea_sports/usp',
    '/ea_sports/featured',

    '/nfs/leaderboard',
    '/nfs/featured',

    '/pvz/photos',
    '/pvz/featured'
]

class Index:
    def GET(self):
        return render.index(ENDPOINTS)

j = lambda x: json.dumps(x)

class Bf4Highlights:
    def GET(self):
        return j(bf4_highlights.highlights())

class Bf4Usp:
    def GET(self):
        return j(bf4_usp.usp())

class EaActivity:
    def GET(self):
        return j(ea_activity.counts())

class EaFeatured:
    def GET(self):
        """ TODO """
        return j(ea_featured.featured())

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
        return j(nfs_leaderboard.top_times())

class NfsFeatured:
    def GET(self):
        """ TODO """
        return j(nfs_featured.featured())

class PvzPhotos:
    def GET(self):
        """ TODO """
        return j(pvz_photos.photos())

class PvzFeatured:
    def GET(self):
        """ TODO """
        return j(pvz_featured.featured())


if __name__ == "__main__": 
    app = web.application(urls, globals())
    app.run()  

    
