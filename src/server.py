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
import ea.message
import nfs.leaderboard
import pvz.photos
import pvz.featured
import sports.usp
import sports.featured
import util.usp
import util.featured
import util.store


render = web.template.render('templates/')

UI_URLS = (
    '/', 'Index',
    '/api', 'API',

    '/ui/usp_quotes/([^/]*)/(.*)',     'UiUspQuotes',
    '/ui/usp_quotes/([^/]*)',          'UiUspQuotesIndex',

    '/ui/messages/([^/]*)',       'UiMessages',

    '/ui/stats/nfs',           'UiStatsNFS',
    '/ui/stats/origin',        'UiStatsOrigin',
)


class UiUspQuotes:
    quote_form = form.Form(
        form.Textbox('name',
                     form.notnull,
                     size="100",
                     description='Name'
                 ),
        form.Textbox('image',
                     form.notnull,
                     form.regexp('^http://', "Must start with 'http://'."),
                     size="100",
                     description='Profile Image URL'
                 ),
        form.Textarea('quote',
                      form.notnull,
                      maxlength="140",
                      description='Quote (<= 140 chars)'
                  )
    )

    def GET(self, brand, usp):
        form = self.quote_form()
        quotes = util.usp.get_quotes(brand, usp)['quotes']
        return render.usp_quotes(brand, usp, quotes, form)

    def POST(self, brand, usp):
        get_url = '/'.join(['/ui/usp_quotes', brand, usp])

        # DELETE?
        try:
            delete_id = web.input().delete_id
        except AttributeError:
            delete_id = None
        if delete_id is not None:
            util.usp.delete_quote(delete_id)
            raise web.seeother(get_url)

        # POST
        form = self.quote_form()
        if not form.validates():
            # FAILURE
            quotes = util.usp.get_quotes(brand, usp)['quotes']
            return render.usp_quotes(brand, usp, quotes, form)
        else:
            # SUCCESS
            util.usp.insert_quote(
                brand, usp,
                form.d.quote, form.d.name, form.d.image
            )
            raise web.seeother(get_url)

class UiUspQuotesIndex:
    BRAND_2_USPS = {
        'BF4': [
            'Frostbite 3',
            'Commander Mode',
            'Amphibious Assault',
            'Levolution',
            'All-Out War'
        ],
        'Sports': [
            'FIFA',
            'Madden',
            'NBA',
            'UFC'
        ]
    }
    def GET(self, brand):
        return render.usp_quotes_index(brand, self.BRAND_2_USPS)

class UiMessages:
    def GET(self, brand):
        return render.messages(brand)

class UiStatsNFS:
    def GET(self):
        return render.nfs_stats()

def num_box(name, desc):
    return form.Textbox(
        name,
        form.notnull,
        form.regexp('^\s*\d+\s*$', "Digits only, please."),
        size="10",
        description=desc
    )

class UiStatsOrigin:
    data_form = form.Form(
        num_box('logins', 'Total number of logins'),
        num_box('gamers', 'Total number of gamers'),
        num_box('games_today', 'Number of games played today'))

    def GET(self):
        form = self.data_form()
        stats_list = util.store.get_origin_data()
        return render.origin_highlights(stats_list, form)

    def POST(self):
        form = self.data_form()
        if not form.validates():
            # FAILURE
            stats_list = util.store.get_origin_data()
            return render.origin_highlights(stats_list, form)
        else:
            # SUCCESS
            KEYS = ['logins', 'gamers', 'games_today']
            util.store.put_origin_data(dict([(k, int(form[k].value))
                                             for k in KEYS]))
            raise web.seeother('/ui/stats/origin')

API_URLS = (
    # BF4
    '/api/bf4/highlights.json',         'Bf4Highlights',
    # bf4 - usp
    '/api/bf4/usp/all.json',                  'Bf4UspAll',
    '/api/bf4/usp/frostbite3.json',           'Bf4UspFrostbite3',
    '/api/bf4/usp/commander_mode.json',       'Bf4UspCommanderMode',
    '/api/bf4/usp/amphibious_assault.json',   'Bf4UspAmphibiousAssault',
    '/api/bf4/usp/levolution.json',           'Bf4UspLevolution',
    '/api/bf4/usp/all_out_war.json',          'Bf4UspAllOutWar',

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
    '/api/sports/featured/ea_sports.json',  'SportsFeaturedEASports',
    '/api/sports/featured/fifa.json',       'SportsFeaturedFIFA',
    '/api/sports/featured/madden.json',     'SportsFeaturedMadden',
    '/api/sports/featured/nba.json',        'SportsFeaturedNBA',
    '/api/sports/featured/ufc.json',        'SportsFeaturedUFC',

    # NFS
    # '/api/nfs/leaderboard',     'NfsLeaderboard',
    '/api/nfs/featured.json',        'NfsFeatured',

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
        return render.index()

class API:
    def GET(self):
        return render.api(ENDPOINTS, TITLE_2_LINK_N_HREF)

j = lambda x: json.dumps(x)

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

#-----------------
# begin
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

class EaFeatured:
    def GET(self):
        # TODO - RETURN TO THIS:
        # return j(util.featured.get_all_featured('ea'))
        return j(bogus_get_featured('ea', 'eae3'))

#-----------------
# end
#-----------------

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
        return j(util.featured.get_all_featured('ea'))

# ---
# It may seem silly to have all these doing the same thing,
# but we want an explicit list of URLs in order to display endpoints.
# ---

class SportsFeatured:
    def GET(self, brand):
        return j(sports.featured.get(brand))

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
        return j(util.featured.get_all_featured('nfs'))

#-- PVZ --

class PvzPhotos:
    def GET(self):
        """ TODO """
        return j(pvz.photos.photos())

class PvzFeatured:
    def GET(self):
        return j(pvz.featured.get())

#-- ORIGIN --

class Origin:
    def GET(self):
        st = util.store.get_origin_data()[0]
        del st['_id']
        return j(st)


if __name__ == "__main__": 
    app = web.application(URLS, globals())
    app.run()  

    
