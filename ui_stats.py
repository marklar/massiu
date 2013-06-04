import web
from web import form
from ui_util import num_box, render

import util.store

class UiStatsOrigin:
    data_form = form.Form(
        num_box('logins', 'Total number of logins'),
        num_box('gamers', 'Total number of gamers'),
        num_box('games_today', 'Number of games played today'))

    def GET(self):
        form = self.data_form()
        stats_list = list(util.store.get_origin_data())
        return render.origin_highlights(stats_list, form)

    def POST(self):
        form = self.data_form()
        if not form.validates():
            # FAILURE
            stats_list = list(util.store.get_origin_data())
            return render.origin_highlights(stats_list, form)
        else:
            # SUCCESS
            KEYS = ['logins', 'gamers', 'games_today']
            util.store.put_origin_data(dict([(k, int(form[k].value))
                                             for k in KEYS]))
            raise web.seeother('/ui/stats/origin')


# Total Takedowns
# Total distance driven 
# Total Racer Speed Points Banked
# Total Racers busted by Cops

class UiNfsGameStats:
    data_form = form.Form(
        num_box('takedowns', 'Total Takedowns'),
        num_box('miles',     'Total Miles Driven (in K)'),
        num_box('speed',     'Total Racer Speed Points Banked'),
        num_box('busts',     'Total Racers Busted by Cops'))

    def GET(self):
        form = self.data_form()
        stats_list = list(util.store.get_nfs_game_stats())
        return render.nfs_stats(stats_list, form)

    def POST(self):
        form = self.data_form()
        if not form.validates():
            # FAILURE
            stats_list = list(util.store.get_nfs_game_stats())
            return render.nfs_stats(stats_list, form)
        else:
            # SUCCESS
            KEYS = ['takedowns', 'miles', 'speed', 'busts']
            util.store.put_nfs_game_stats(dict([(k, int(form[k].value))
                                                for k in KEYS]))
            raise web.seeother('/ui/stats/nfs')
