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
    '/api/bf4/highlights.json',         'Bf4Highlights',
    # bf4 - usp
    '/api/bf4/usp/all.json',                  'Bf4UspAll',
    '/api/bf4/ups/frostbite3.json',           'Bf4UspFrostbite3',
    '/api/bf4/ups/commander_mode.json',       'Bf4UspCommanderMode',
    '/api/bf4/ups/amphibious_assault.json',   'Bf4UspAmphibiousAssault',
    '/api/bf4/ups/levolution.json',           'Bf4UspLevolution',
    '/api/bf4/ups/all_out_war.json',          'Bf4UspAllOutWar',

    # EA
    '/api/ea/fb_likes.json',         'EaFbLikes',
    '/api/ea/featured.json',         'EaFeatured',
    '/api/ea/activity.json',         'EaActivity',
    '/api/ea/message.json',          'EaMessage',

    # Sports - usp
    '/api/sports/usp/all.json',             'SportsUspAll',
    '/api/sports/usp/fifa.json',            'SportsUspFIFA',
    '/api/sports/usp/madden.json',          'SportsUspMadden',
    '/api/sports/usp/nba.json',             'SportsUspNBA',
    '/api/sports/usp/ufc.json',             'SportsUspUFC',
    # Sports - featured
    '/api/sports/featured/all.json',        'SportsFeaturedAll',
    '/api/sports/featured/ufc.json',        'SportsFeaturedUFC',
    '/api/sports/featured/fifa.json',       'SportsFeaturedFIFA',
    '/api/sports/featured/ea_sports.json',  'SportsFeaturedEASports',
    '/api/sports/featured/madden.json',     'SportsFeaturedMadden',
    '/api/sports/featured/nba.json',        'SportsFeaturedNBA',

    # NFS
    # '/api/nfs/leaderboard',     'NfsLeaderboard',
    '/api/nfs/featured.json',        'NfsFeatured',

    # PVZ
    '/api/pvz/photos.json',          'PvzPhotos',
    '/api/pvz/featured.json',        'PvzFeatured',

    # Origin
    # '/origin/',     'Origin',

)

ENDPOINTS = [URLS[i] for i in range(2, len(URLS)-1, 2)]

rex = re.compile("^/api/([^/]*)/(.*)\.json$")
TITLE_2_LINK_N_HREF = {}
for e in ENDPOINTS:
    m = rex.search(e)
    title = m.group(1)
    rest = m.group(2)
    if title not in TITLE_2_LINK_N_HREF:
        TITLE_2_LINK_N_HREF[title] = []
    parts = ['api', title, rest + '.json']
    TITLE_2_LINK_N_HREF[title].append((rest, '/'.join(parts)))


j = lambda x: json.dumps(x)

class Index:
    def GET(self):
        return render.index(ENDPOINTS, TITLE_2_LINK_N_HREF)

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

    
