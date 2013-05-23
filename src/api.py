import web
import json
import re

import bf4.highlights
import bf4.usp
import ea.activity
import ea.featured
import ea.likes
import ea.message
import nfs.leaderboard
import nfs.featured
import pvz.photos
import pvz.featured
import sports.usp
import sports.featured

render = web.template.render('templates/')

URLS = (
    '/', 'Index',

    # BF4
    '/api/bf4/highlights',         'Bf4Highlights',
    # bf4 - usp
    '/api/bf4/usp/all',                  'Bf4UspAll',
    '/api/bf4/ups/frostbite3',           'Bf4UspFrostbite3',
    '/api/bf4/ups/commander_mode',       'Bf4UspCommanderMode',
    '/api/bf4/ups/amphibious_assault',   'Bf4UspAmphibiousAssault',
    '/api/bf4/ups/levolution',           'Bf4UspLevolution',
    '/api/bf4/ups/all_out_war',          'Bf4UspAllOutWar',    

    # EA
    '/api/ea/fb_likes',         'EaFbLikes',
    '/api/ea/featured',         'EaFeatured',
    '/api/ea/activity',         'EaActivity',
    '/api/ea/message',          'EaMessage',

    # Sports - usp
    '/api/sports/usp/all',             'SportsUspAll',
    '/api/sports/usp/fifa',            'SportsUspFIFA',
    '/api/sports/usp/madden',          'SportsUspMadden',
    '/api/sports/usp/nba',             'SportsUspNBA',
    '/api/sports/usp/ufc',             'SportsUspUFC',
    # Sports - featured
    '/api/sports/featured/all',        'SportsFeaturedAll',
    '/api/sports/featured/ufc',        'SportsFeaturedUFC',
    '/api/sports/featured/fifa',       'SportsFeaturedFIFA',
    '/api/sports/featured/ea_sports',  'SportsFeaturedEASports',
    '/api/sports/featured/madden',     'SportsFeaturedMadden',
    '/api/sports/featured/nba',        'SportsFeaturedNBA',

    # NFS
    # '/api/nfs/leaderboard',     'NfsLeaderboard',
    '/api/nfs/featured',        'NfsFeatured',

    # PVZ
    '/api/pvz/photos',          'PvzPhotos',
    '/api/pvz/featured',        'PvzFeatured',

    # Origin
    # '/origin/',     'Origin',

)

ENDPOINTS = [URLS[i] for i in range(2, len(URLS)-1, 2)]

rex = re.compile("^/api/([^/]*)/(.*)$")
TITLE_2_ENDS = {}
for e in ENDPOINTS:
    m = rex.search(e)
    title = m.group(1)
    rest = m.group(2)
    if title not in TITLE_2_ENDS:
        TITLE_2_ENDS[title] = []
    TITLE_2_ENDS[title].append(rest)


j = lambda x: json.dumps(x)

class Index:
    def GET(self):
        return render.index(ENDPOINTS, TITLE_2_ENDS)

#-- BF4 --

class Bf4Highlights:
    def GET(self):
        return j(bf4.highlights.highlights())

class Bf4UspAll:
    """ Canned data for now. """
    def GET(self):
        return j(bf4.usp.get_all())

class Bf4UspFrostbite3:
    def GET(self):
        return j(bf4.usp.frostbite3())

class Bf4UspCommanderMode:
    def GET(self):
        return j(bf4.usp.commander_mode())

class Bf4UspAmphibiousAssault:
    def GET(self):
        return j(bf4.usp.amphibious_assault())

class Bf4UspLevolution:
    def GET(self):
        return j(bf4.usp.levolution())

class Bf4UspAllOutWar:
    def GET(self):
        return j(bf4.usp.all_out_war())


#-- EA --

class EaActivity:
    def GET(self):
        return j(ea.activity.counts())

class EaMessage:
    def GET(self):
        return j(ea.message.get_most_recent())

class EaFeatured:
    def GET(self):
        return j(ea.featured.get())

class EaFbLikes:
    def GET(self):
        return j(ea.likes.get())

#-- SPORTS --

class SportsUspAll:
    def GET(self):
        return j(sports.usp.all_usps())

class SportsUspFIFA:
    def GET(self):
        return j(sports.usp.fifa())

class SportsUspMadden:
    def GET(self):
        return j(sports.usp.madden())

class SportsUspNBA:
    def GET(self):
        return j(sports.usp.nba())

class SportsUspUFC:
    def GET(self):
        return j(sports.usp.ufc())

class SportsFeaturedAll:
    def GET(self):
        return j(sports.featured.get_all())

class SportsFeaturedUFC:
    def GET(self):
        return j(sports.featured.get('ufc'))

class SportsFeaturedFIFA:
    def GET(self):
        return j(sports.featured.get('fifa'))

class SportsFeaturedEASports:
    def GET(self):
        return j(sports.featured.get('ea_sports'))
    
class SportsFeaturedMadden:
    def GET(self):
        return j(sports.featured.get('madden'))

class SportsFeaturedNBA:
    def GET(self):
        return j(sports.featured.get('nba'))

#-- NFS --

class NfsLeaderboard:
    def GET(self):
        return j(nfs.leaderboard.top_times(5))

class NfsFeatured:
    def GET(self):
        return j(nfs.featured.get())

#-- PVZ --

class PvzPhotos:
    def GET(self):
        """ TODO """
        return j(pvz.photos.photos())

class PvzFeatured:
    def GET(self):
        return j(pvz.featured.get())

#-- ORIGIN --



if __name__ == "__main__": 
    app = web.application(URLS, globals())
    app.run()  

    
