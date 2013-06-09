# from gevent import monkey; monkey.patch_all()
# import gevent
# from gevent.pywsgi import WSGIServer
import time
import web
from web import form
import json
import re

# Add src to py path.
import sys
import os
this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_dir)
from bson.objectid import ObjectId

import bf4.highlights
import bf4.usp
import ea.activity
import ea.likes
import ea.messages
import nfs.leaderboard
import pvz.photos
import pvz.featured
import pvz.messages
import sports.usp
import sports.featured
import util.featured
from util import my_time
import util.store

from ui_util import render
from ui_ea_messages import UiEaMessages
from ui_pvz_messages import UiPvzMessages
from ui_usp_quotes import UiUspQuotes, UiUspQuotesIndex
from ui_stats import UiStatsOrigin, UiNfsGameStats

UI_URLS = (
    '/', 'Index',
    '/api', 'API',

    '/static/(.*)', 'static',

    '/ui/usp_quotes/([^/]*)/(.*)',     'UiUspQuotes',
    '/ui/usp_quotes/([^/]*)',          'UiUspQuotesIndex',

    '/ui/messages/ea',         'UiEaMessages',
    '/ui/messages/pvz',        'UiPvzMessages',
    '/ui/message/(.*)/(.*)',       'UiDeleteMessage',

    '/ui/stats/nfs',           'UiNfsGameStats',
    '/ui/stats/origin',        'UiStatsOrigin',

    '/ui/prefetching/start',  'StartPrefetching',
    '/ui/caching/clear',      'ClearCache'
)

class UiDeleteMessage:
    def POST(self, brand, id_str):
        _id = ObjectId(id_str)
        if 'brand' == 'ea':
            ea.messages.delete_message(_id)
        else:
            pvz.messages.delete_message(_id)
        raise web.seeother('/ui/messages/' + brand)

def w_cache(obj, f, *args):
    cached = util.store.get_cached(obj, *args)
    if cached is not None:
        # print 'Cached!'
        return j(cached)
    else:
        # print 'NOT cached.'
        res = f(*args)
        util.store.put_cached(res, obj, *args)
        return j(res)

def cache():
    classes = [
        Bf4Highlights, EaActivity, EaFbLikes, EaFeatured,
        SportsFeaturedEASports, SportsFeaturedFIFA,
        SportsFeaturedMadden, SportsFeaturedNBA,
        SportsFeaturedUFC,
        NfsFeatured,
        PvzPhotos, PvzFeatured
    ]
    for c in classes:
        c().GET()

prefetchlet = None
is_prefetching_on = False
counter = 0
PERIOD_SECS = 60

def turn_on_caching():
    """ Cache slow queries every PERIOD_SECS seconds. """
    global counter
    while True:
        cache()
        counter += 1
        time.sleep(PERIOD_SECS)

class StartPrefetching:
    def POST(self):
        global is_prefetching_on, prefetchlet
        if is_prefetching_on:
            raise web.seeother('/')
        else:
            is_prefetching_on = True
            # prefetchlet = gevent.spawn(turn_on_caching)
            raise web.seeother('/')

class StopPrefetching:
    """ Not implemented yet. """
    def POST(self):
        global is_prefetching_on, prefetchlet
        if is_prefetching_on:
            prefetchlet.kill()
        raise web.seeother('/')

class ClearCache:
    def POST(self):
        util.store.clear_cache()
        raise web.seeother('/')


class static:
  def GET(self, name):
    return open('static/%s' % name)

API_URLS = (
    # BF4
    '/api/bf4/highlights.json',         'Bf4Highlights',
    # bf4 - usp
    '/api/bf4/usp/frostbite3.json',           'Bf4UspFrostbite3',
    '/api/bf4/usp/commander_mode.json',       'Bf4UspCommanderMode',
    '/api/bf4/usp/amphibious_assault.json',   'Bf4UspAmphibiousAssault',
    '/api/bf4/usp/levolution.json',           'Bf4UspLevolution',
    '/api/bf4/usp/all_out_war.json',          'Bf4UspAllOutWar',

    # EA
    '/api/ea/message.json',          'EaMessage',
    '/api/ea/fb_likes.json',         'EaFbLikes',
    '/api/ea/featured.json',         'EaFeatured',
    '/api/ea/activity.json',         'EaActivity',

    # Sports - usp
    '/api/sports/usp/ignite_human_intelligence.json', 'SportsUspIgniteHI',
    '/api/sports/usp/ignite_true_player_motion.json', 'SportsUspIgniteTPM',
    '/api/sports/usp/ignite_living_worlds.json',      'SportsUspIgniteLW',

    '/api/sports/usp/fifa.json',            'SportsUspFIFA',
    '/api/sports/usp/madden.json',          'SportsUspMadden',
    '/api/sports/usp/nba.json',             'SportsUspNBA',
    '/api/sports/usp/ufc.json',             'SportsUspUFC',

    # Sports - featured
    '/api/sports/featured/ea_sports.json',  'SportsFeaturedEASports',
    '/api/sports/featured/fifa.json',       'SportsFeaturedFIFA',
    '/api/sports/featured/madden.json',     'SportsFeaturedMadden',
    '/api/sports/featured/nba.json',        'SportsFeaturedNBA',
    '/api/sports/featured/ufc.json',        'SportsFeaturedUFC',

    # NFS
    # '/api/nfs/leaderboard',     'NfsLeaderboard',
    '/api/nfs/featured.json',        'NfsFeatured',
    '/api/nfs/game_stats.json',      'NfsGameStats',

    # PVZ
    '/api/pvz/photos.json',          'PvzPhotos',
    '/api/pvz/featured.json',        'PvzFeatured',
    '/api/pvz/message.json',         'PvzMessage',

    # Origin
    '/api/origin/highlights.json',     'Origin'
)

URLS = UI_URLS + API_URLS

ODD_INDICES = range(0, len(API_URLS)-1, 2)
ENDPOINTS = [API_URLS[i] for i in ODD_INDICES]

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


class Index:
    def GET(self):
        global is_prefetching_on, counter
        return render.index(is_prefetching_on, counter)

class API:
    def GET(self):
        return render.api(ENDPOINTS, TITLE_2_LINK_N_HREF)

def j(x):
    msg = ea.messages.get_jsonable_active_msg()
    if msg is not None:
        res = {
            'show_message': True,
            'message': msg,
            'response': x
        }
    else:
        res = {
            'show_message': False,
            'response': x
        }
    return json.dumps(res)

#-- BF4 --

class Bf4Highlights:
    def GET(self):
        return w_cache(self, bf4.highlights.highlights)

class Bf4UspFrostbite3:
    def GET(self):
        return w_cache(self, bf4.usp.frostbite3)

class Bf4UspCommanderMode:
    def GET(self):
        return w_cache(self, bf4.usp.commander_mode)

class Bf4UspAmphibiousAssault:
    def GET(self):
        return w_cache(self, bf4.usp.amphibious_assault)

class Bf4UspLevolution:
    def GET(self):
        return w_cache(self, bf4.usp.levolution)

class Bf4UspAllOutWar:
    def GET(self):
        return w_cache(self, bf4.usp.all_out_war)

#-- EA --

class EaMessage:
    def GET(self):
        obj = ea.messages.get_jsonable_active_msg()
        if obj is None:
            res = {'show_message': False}
        else:
            res = {'show_message': True, 'message': obj}
        return json.dumps(res)

class EaActivity:
    def GET(self):
        return w_cache(self, ea.activity.counts)

class EaFeatured:
    def GET(self):
        return w_cache(self, util.featured.get_all_featured, 'ea')

class EaFbLikes:
    def GET(self):
        return w_cache(self, ea.likes.get)

#-- SPORTS --

class SportsUspIgniteHI:
    def GET(self):
        return w_cache(self, sports.usp.ignite_human_intelligence)

class SportsUspIgniteTPM:
    def GET(self):
        return w_cache(self, sports.usp.ignite_true_player_motion)

class SportsUspIgniteLW:
    def GET(self):
        return w_cache(self, sports.usp.ignite_living_worlds)

class SportsUspFIFA:
    def GET(self):
        return w_cache(self, sports.usp.fifa)

class SportsUspMadden:
    def GET(self):
        return w_cache(self, sports.usp.madden)

class SportsUspNBA:
    def GET(self):
        return w_cache(self, sports.usp.nba)

class SportsUspUFC:
    def GET(self):
        return w_cache(self, sports.usp.ufc)

# ---
# It may seem silly to have all these doing the same thing,
# but we want an explicit list of URLs in order to display endpoints.
# ---

class SportsFeaturedUFC:
    def GET(self):
        return w_cache(self, sports.featured.get, 'ufc')

class SportsFeaturedFIFA:
    def GET(self):
        return w_cache(self, sports.featured.get, 'fifa')

class SportsFeaturedEASports:
    def GET(self):
        return w_cache(self, sports.featured.get, 'ea_sports')
    
class SportsFeaturedMadden:
    def GET(self):
        return w_cache(self, sports.featured.get, 'madden')

class SportsFeaturedNBA:
    def GET(self):
        return w_cache(self, sports.featured.get, 'nba')

#-- NFS --

class NfsLeaderboard:
    def GET(self):
        return j(nfs.leaderboard.top_times(5))

class NfsFeatured:
    def GET(self):
        return w_cache(self, util.featured.get_all_featured, 'nfs')

# NFS stats - they've requested to change the use of the photos to display the top winners from the tournaments - there will be two top cops and two top racers.  to do this, I suggested it could work like this:
# 1) images will be tweeted from @needforspeed account with the hashtags #topcop #topracer. 
# 2) we will setup mass relevance to pull all photos with those hashtags
# 3) cms will push content to visualization 
# 4) visualization will show most recent two images from each group

# 'https://si0.twimg.com/profile_images/2281988491/8oz02frum9e7hm8l6eq7.jpeg',

# NEW NEW NEW
# the visualization needs to pull in the latest two photos tweeted by the @needforspeed account with the hashtags: #NFSRivalsTopCops and #NFSRivalsTopRacers

def get_nfs_game_stats():
    stats = util.store.get_most_recent_nfs_game_stats()
    return {
        'stats': stats,
        # TODO: Include *real* images data.
        'images': {
            'topcop': [
                'http://si0.twimg.com/profile_images/1129466536/fcb.png',
                'http://si0.twimg.com/profile_images/1048074687/cara_messi.jpg'],
            'topracer': [
                'http://si0.twimg.com/profile_images/3222338434/bbdc41334f3db7b1349fc9d97362b284.jpeg',
                'http://si0.twimg.com/profile_images/1719423111/perfil_twitter2.jpg'
            ]
        }
    }

class NfsGameStats:
    def GET(self):
        return w_cache(self, get_nfs_game_stats)

#-- PVZ --

class PvzPhotos:
    def GET(self):
        # return j(pvz.photos.get_photos(4))
        return w_cache(self, pvz.photos.get_photos, 15)

class PvzFeatured:
    def GET(self):
        return w_cache(self, pvz.featured.get)

class PvzMessage:
    def GET(self):
        return j(pvz.messages.get_one())

#-- ORIGIN --

class Origin:
    def GET(self):
        st = util.store.get_origin_data()[0]
        del st['_id']
        return j(st)


if __name__ == '__main__':
    app = web.application(URLS, globals())
    app.run()
    # app = web.application(URLS, globals()).wsgifunc()
    # print 'Serving on 5000...'
    # port = int(sys.argv[1])
    # WSGIServer(('', port), app).serve_forever()

