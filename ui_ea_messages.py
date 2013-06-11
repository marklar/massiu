import web
from web import form
from datetime import datetime, timedelta
from dateutil import tz

import ea.messages as msgs
from ui_util import render, num_box
from webpy_mongodb_sessions import users

FORMAT = '%b %d %I:%M:%S %p'

LA_TIME_ZONE = tz.gettz('America/Los_Angeles')
def la_now():
    return datetime.now(LA_TIME_ZONE)

class UiEaMessages:
    message_form = form.Form(
        form.Textarea('text',
                      form.notnull,
                      maxlength="150",
                      description='Message (<= 150 chars):'),
        num_box('delay_secs',    'Display in:'),
        num_box('duration_secs', 'Duration (in seconds):'))

    @users.login_required
    def GET(self):
        return render.ea_messages(
            self.get_messages(),
            self.message_form(),
            la_now(),
            FORMAT)

    @users.login_required
    def POST(self):
        form = self.message_form()
        now = la_now()
        if not form.validates():
            # FAILURE
            return render.ea_messages(
                self.get_messages(),
                form,
                now,
                FORMAT)
        else:
            # SUCCESS
            delay_secs = int(form['delay_secs'].value)
            duration_secs = int(form['duration_secs'].value)
            desired_start_time = self.make_start_time(delay_secs)
            msg = {
                'text': form['text'].value,
                'delay_secs': delay_secs,
                'duration_secs': duration_secs,
                'desired_start_time': desired_start_time,
                'created_at': now
            }
            msgs.put_message(msg)
            raise web.seeother('/top_secret/messages/ea')


    def get_messages(self):
        active = msgs.get_active_message()
        if active is None:
            actives = []
        else:
            actives = [active]
        return {
            'active':  actives,
            'future':  list(msgs.get_future_messages()),
            'expired': list(msgs.get_expired_messages())
        }

    def make_start_time(self, delay_secs):
        return self.add_secs(la_now(), delay_secs)

    def add_secs(self, dt, secs):
        return dt + timedelta(seconds = secs)
