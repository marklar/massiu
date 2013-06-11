import time
import re
import simplejson as json
import web
from web import form

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
import nfs.photos
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


from mdb_session import MongoStore
from pymongo import MongoClient
import mdb_users as users


UI_URLS = (
    '/', 'Index',
    '/api', 'API',

    '/login',   'UiLogin',
    '/logout',  'UiLogout',
    '/user/create', 'CreateUser',

    '/static/(.*)', 'static',

    '/ui/usp_quotes/([^/]*)/(.*)',     'UiUspQuotes',
    '/ui/usp_quotes/([^/]*)',          'UiUspQuotesIndex',

    '/ui/messages/EA',           'UiSorryDude',
    '/ui/messages/ea',           'UiSorryDude',
    '/top_secret/messages/ea',   'UiEaMessages',

    '/ui/messages/pvz',        'UiPvzMessages',
    '/ui/message/(.*)/(.*)',   'UiDeleteMessage',

    '/ui/stats/nfs',           'UiNfsGameStats',
    '/ui/stats/origin',        'UiStatsOrigin',

    '/ui/caching/clear',      'ClearCache',
    '/ui/caching/prefetch',   'Prefetch'
)

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


web.config.debug = False
app = web.application(URLS, globals())
db = util.store.get_db()
session = web.session.Session(app, MongoStore(db, 'sessions'))
users.session = session
users.collection = db.users

#----------

USER = 'Gozer'
PSWD = 'GiantSlor'
class CreateUser:
    def GET(self):
        users.collection.remove({'username': USER})
        users.register(username=USER, password=users.pswd(PSWD))
        return 'user %s created' % USER

class UiLogin:
    login_form = form.Form(
        form.Textbox('username', form.notnull),
        form.Password('password', form.notnull),
        form.Button('Login'))
    def GET(self):
        f = self.login_form()
        return render.login(f, None)
    def POST(self):
        f = self.login_form()
        if not f.validates():
            return render.login(f, 'Please fill in both fields.')
        else:
            user = users.authenticate(f.d.username, f.d.password)
            if user:
                users.login(user)
                i = web.input()
                raise web.seeother(i.next)
            else:
                return render.login(f, 'Does not authenticate.')

class UiLogout:
    def POST(self):
        users.logout()
        raise web.seeother('/')

#----------

class UiSorryDude:
    def GET(self):
        return """
<html>
<head></head>
<body style="font-family:arial">
<h2>Sorry, dude.</h2>
<p>
  This URL is now a
  <a href="http://www.youtube.com/watch?v=cPQcnjlwtE4">Road to Nowhere</a>.
</p>
</body>
</html>"""

#----------

class UiDeleteMessage:
    def POST(self, brand, id_str):
        _id = ObjectId(id_str)
        if 'brand' == 'ea':
            ea.messages.delete_message(_id)
        else:
            pvz.messages.delete_message(_id)
        raise web.seeother('/ui/messages/' + brand)

#----------

class Prefetch:
    def GET(self):
        self.pre_fetch()
        raise web.seeother('/')

    def POST(self):
        self.pre_fetch()
        raise web.seeother('/')

    def pre_fetch(self):
        classes = [
            Bf4Highlights,
            EaActivity, EaFbLikes, EaFeatured,
            SportsFeaturedEASports, SportsFeaturedFIFA,
            SportsFeaturedMadden, SportsFeaturedNBA,
            SportsFeaturedUFC,
            NfsFeatured,
            PvzPhotos, PvzFeatured
        ]
        for c in classes:
            c().POST()

class ClearCache:
    def POST(self):
        util.store.clear_cache()
        raise web.seeother('/')

#-----------------------------

class static:
  def GET(self, name):
    return open('static/%s' % name)


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
    @users.login_required
    def GET(self):
        return render.index()

class API:
    @users.login_required
    def GET(self):
        return render.api(ENDPOINTS, TITLE_2_LINK_N_HREF)

#----------

def re_cache(obj, f, *args):
    util.store.rm_cached(obj, *args)
    res = f(*args)
    util.store.put_cached(res, obj, *args)

def w_cache(obj, f, *args):
    """
    Attempt to pull from cache.
    If not there, gather response, add to cache, and return it.
    """
    cached = util.store.get_cached(obj, *args)
    if cached is not None:
        return w_msg(cached)
    else:
        res = f(*args)
        util.store.put_cached(res, obj, *args)
        return w_msg(res)

def w_msg(x):
    """
    Wrap response in object including info about possible show message.
    """
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
    return j_out(res)

def j_out(x):
    """ Output proper utf-8 json. """
    web.header('Content-Type','application/json; charset=utf-8')
    return json.dumps(x, ensure_ascii=False, encoding='utf-8', indent=4)

#-- BF4 --

class Bf4Highlights:
    def GET(self):
        # return w_cache(*self.f())
        return w_cache(self, bf4.highlights.highlights)
    def POST(self):
        # return re_cache(*self.f())
        return re_cache(self, bf4.highlights.highlights)
    def f(self):
        return (self, bf4.highlights.highlights)

class Bf4UspFrostbite3:
    def GET(self):
        return w_msg(bf4.usp.frostbite3())

class Bf4UspCommanderMode:
    def GET(self):
        return w_msg(bf4.usp.commander_mode())

class Bf4UspAmphibiousAssault:
    def GET(self):
        return w_msg(bf4.usp.amphibious_assault())

class Bf4UspLevolution:
    def GET(self):
        return w_msg(bf4.usp.levolution())

class Bf4UspAllOutWar:
    def GET(self):
        return w_msg(bf4.usp.all_out_war())

#-- EA --

class EaMessage:
    def GET(self):
        obj = ea.messages.get_jsonable_active_msg()
        if obj is None:
            res = {'show_message': False}
        else:
            res = {'show_message': True, 'message': obj}
        return j_out(res)

class EaActivity:
    def GET(self):
        return w_cache(self, ea.activity.counts)
    def POST(self):
        return re_cache(self, ea.activity.counts)

class EaFeatured:
    def GET(self):
        return w_cache(self, util.featured.get_all_featured, 'ea')
    def POST(self):
        return re_cache(self, util.featured.get_all_featured, 'ea')

class EaFbLikes:
    def GET(self):
        return w_cache(self, ea.likes.get)
    def POST(self):
        return re_cache(self, ea.likes.get)

#-- SPORTS --

class SportsUspIgniteHI:
    def GET(self):
        return w_msg(sports.usp.ignite_human_intelligence())

class SportsUspIgniteTPM:
    def GET(self):
        return w_msg(sports.usp.ignite_true_player_motion())

class SportsUspIgniteLW:
    def GET(self):
        return w_msg(sports.usp.ignite_living_worlds())

class SportsUspFIFA:
    def GET(self):
        return w_msg(sports.usp.fifa())

class SportsUspMadden:
    def GET(self):
        return w_msg(sports.usp.madden())

class SportsUspNBA:
    def GET(self):
        return w_msg(sports.usp.nba())

class SportsUspUFC:
    def GET(self):
        return w_msg(sports.usp.ufc())

# ---
# It may seem silly to have all these doing the same thing,
# but we want an explicit list of URLs in order to display endpoints.
# ---

class SportsFeaturedUFC:
    def GET(self):
        return w_cache(self, sports.featured.get, 'ufc')
    def POST(self):
        return re_cache(self, sports.featured.get, 'ufc')

class SportsFeaturedFIFA:
    def GET(self):
        return w_cache(self, sports.featured.get, 'fifa')
    def POST(self):
        return re_cache(self, sports.featured.get, 'fifa')

class SportsFeaturedEASports:
    def GET(self):
        return w_cache(self, sports.featured.get, 'ea_sports')
    def POST(self):
        return re_cache(self, sports.featured.get, 'ea_sports')
    
class SportsFeaturedMadden:
    def GET(self):
        return w_cache(self, sports.featured.get, 'madden')
    def POST(self):
        return re_cache(self, sports.featured.get, 'madden')

class SportsFeaturedNBA:
    def GET(self):
        return w_cache(self, sports.featured.get, 'nba')
    def POST(self):
        return re_cache(self, sports.featured.get, 'nba')

#-- NFS --

# class NfsLeaderboard:
#     def GET(self):
#         return w_msg(nfs.leaderboard.top_times(5))

class NfsFeatured:
    def GET(self):
        return w_cache(self, util.featured.get_all_featured, 'nfs')
    def POST(self):
        return re_cache(self, util.featured.get_all_featured, 'nfs')

def get_nfs_game_stats(prot_n_host):
    return {
        'stats': util.store.get_most_recent_nfs_game_stats(),
        'images': nfs.photos.get_photos(prot_n_host)
    }

class NfsGameStats:
    def GET(self):
        return w_cache(self, get_nfs_game_stats, web.ctx.homedomain)
    def POST(self):
        return re_cache(self, get_nfs_game_stats, web.ctx.homedomain)

#-- PVZ --

class PvzPhotos:
    def GET(self):
        return w_cache(self, pvz.photos.get_photos, 15)
    def POST(self):
        return re_cache(self, pvz.photos.get_photos, 15)

class PvzFeatured:
    def GET(self):
        return w_cache(self, pvz.featured.get)
    def POST(self):
        return re_cache(self, pvz.featured.get)

class PvzMessage:
    def GET(self):
        return w_msg(pvz.messages.get_one())

#-- ORIGIN --

class Origin:
    def GET(self):
        st = util.store.get_origin_data()[0]
        del st['_id']
        return w_msg(st)


if __name__ == '__main__':
    app.run()
