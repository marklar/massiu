from gevent import monkey; monkey.patch_all()
import gevent
from gevent.pywsgi import WSGIServer
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

import bf4.highlights
import bf4.usp
import ea.activity
import ea.likes
import nfs.leaderboard
import pvz.photos
import pvz.featured
import sports.usp
import sports.featured
import util.featured
from util import my_time
import util.store

from ui_util import render, num_box
from ui_show_messages import UiShowMessages
from ui_usp_quotes import UiUspQuotes, UiUspQuotesIndex
from ui_stats import UiStatsOrigin, UiNfsGameStats
from util import show_messages

UI_URLS = (
    '/', 'Index',
    '/api', 'API',

    '/static/(.*)', 'static',

    '/ui/usp_quotes/([^/]*)/(.*)',     'UiUspQuotes',
    '/ui/usp_quotes/([^/]*)',          'UiUspQuotesIndex',

    '/ui/show/messages',       'UiShowMessages',

    '/ui/stats/nfs',           'UiNfsGameStats',
    '/ui/stats/origin',        'UiStatsOrigin',

    '/ui/caching/start',      'StartCaching'
)


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

cachelet = None
is_caching_on = False
counter = 0
PERIOD_SECS = 90

def turn_on_caching():
    """ Cache slow queries every PERIOD_SECS seconds. """
    global counter
    while True:
        cache()
        counter += 1
        time.sleep(PERIOD_SECS)

class StartCaching:
    def POST(self):
        global is_caching_on, cachelet
        if is_caching_on:
            raise web.seeother('/')
        else:
            is_caching_on = True
            cachelet = gevent.spawn(turn_on_caching)
            raise web.seeother('/')

class StopCaching:
    """ Not implemented yet. """
    def POST(self):
        global is_caching_on, cachelet
        if is_caching_on:
            cachelet.kill()
        raise web.seeother('/')

class static:
  def GET(self, name):
    return open('static/%s' % name)

API_URLS = (
    '/api/show/message.json',          'ShowMessage',

    # BF4
    '/api/bf4/highlights.json',         'Bf4Highlights',
    # bf4 - usp
    '/api/bf4/usp/frostbite3.json',           'Bf4UspFrostbite3',
    '/api/bf4/usp/commander_mode.json',       'Bf4UspCommanderMode',
    '/api/bf4/usp/amphibious_assault.json',   'Bf4UspAmphibiousAssault',
    '/api/bf4/usp/levolution.json',           'Bf4UspLevolution',
    '/api/bf4/usp/all_out_war.json',          'Bf4UspAllOutWar',

    # EA
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
        global is_caching_on, counter
        return render.index(is_caching_on, counter)

class API:
    def GET(self):
        return render.api(ENDPOINTS, TITLE_2_LINK_N_HREF)

def j(x):
    msg = show_messages.get_jsonable_active_msg()
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

#-- EA & PvZ --
        
class ShowMessage:
    def GET(self):
        obj = show_messages.get_jsonable_active_msg()
        if obj is None:
            res = {'show_message': False}
        else:
            res = {'show_message': True, 'message': obj}
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

class EaActivity:
    def GET(self):
        return w_cache(self, ea.activity.counts)

#-----------------
# begin BOGUS
#-----------------

FEATURED_SUFFIX = '_featured'
STARRED_SUFFIX = '_starred'

def bogus_get_featured(stream_name_root, hashtag):
    """
    Return both starred and featured.
    Remove any from featured that already appear in starred.
    """
    # TODO
    util.store.drop_coll(stream_name_root + STARRED_SUFFIX)
    util.store.drop_coll(stream_name_root + FEATURED_SUFFIX)

    starred = bogus_get_w_tag(stream_name_root + STARRED_SUFFIX)
    featured = bogus_get_w_tag(stream_name_root + FEATURED_SUFFIX)

    # TODO: Limit the number of starred to 5?
    novel_featured = [f for f in featured if f not in starred]

    return {
        'hashtag': '#' + hashtag,
        'starred_tweets': starred,
        'other_tweets': novel_featured
    }

import util.gather
def bogus_get_w_tag(stream_name):
    util.gather.only_new_tweets(stream_name)
    return [util.featured.slim(t) for t in util.store.get_all(stream_name)]

def bogus_ea_featured():
    return [bogus_get_featured('ea', 'eae3')]

class EaFeatured:
    def GET(self):
        # TODO - RETURN TO THIS:
        # return j(util.featured.get_all_featured('ea'))
        # TEMP:
        # return j(bogus_ea_featured())
        return w_cache(self, bogus_ea_featured)

#-----------------
# end BOGUS
#-----------------

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

class NfsGameStats:
    def GET(self):
        return w_cache(self, util.store.get_most_recent_nfs_game_stats)

#-- PVZ --

class PvzPhotos:
    def GET(self):
        """ TODO """
        return j(pvz.photos.photos())

class PvzFeatured:
    def GET(self):
        return w_cache(self, pvz.featured.get)

#-- ORIGIN --

class Origin:
    def GET(self):
        st = util.store.get_origin_data()[0]
        del st['_id']
        return j(st)


if __name__ == '__main__':
    # app = web.application(URLS, globals())
    # app.run()
    app = web.application(URLS, globals()).wsgifunc()
    print 'Serving on 5000...'
    WSGIServer(('', 5000), app).serve_forever()

