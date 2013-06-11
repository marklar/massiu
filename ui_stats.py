import web
from web import form
from ui_util import num_str_box, render

import util.store
from webpy_mongodb_sessions import users

class UiStatsOrigin:
    data_form = form.Form(
        num_str_box('logins', 'Total number of logins'),
        num_str_box('gamers', 'Total number of gamers'),
        num_str_box('games_today', 'Number of games played today'))

    @users.login_required
    def GET(self):
        form = self.data_form()
        stats_list = list(util.store.get_origin_data())
        return render.origin_highlights(stats_list, form)

    @users.login_required
    def POST(self):
        form = self.data_form()
        if not form.validates():
            # FAILURE
            stats_list = list(util.store.get_origin_data())
            return render.origin_highlights(stats_list, form)
        else:
            # SUCCESS
            KEYS = ['logins', 'gamers', 'games_today']
            util.store.put_origin_data(dict([(k, form[k].value)
                                             for k in KEYS]))
            raise web.seeother('/ui/stats/origin')


# Total Takedowns
# Total distance driven 
# Total Racer Speed Points Banked
# Total Racers busted by Cops

class UiNfsGameStats:
    data_form = form.Form(
        num_str_box('takedowns', 'Total Takedowns'),
        num_str_box('miles',     'Total Distance Driven'),
        num_str_box('speed',     'Total Racer Speed Points Banked'),
        num_str_box('busts',     'Total Racers Busted by Cops'))

    @users.login_required
    def GET(self):
        form = self.data_form()
        stats_list = list(util.store.get_nfs_game_stats())
        return render.nfs_stats(stats_list, form)

    @users.login_required
    def POST(self):
        form = self.data_form()
        if not form.validates():
            # FAILURE
            stats_list = list(util.store.get_nfs_game_stats())
            return render.nfs_stats(stats_list, form)
        else:
            # SUCCESS
            KEYS = ['takedowns', 'miles', 'speed', 'busts']
            util.store.put_nfs_game_stats(dict([(k, form[k].value)
                                                for k in KEYS]))
            raise web.seeother('/ui/stats/nfs')
