import web
from web import form
from datetime import datetime, timedelta

import util.show_messages as msgs
from ui_util import render, num_box


class UiShowMessages:
    message_form = form.Form(
        form.Dropdown('brand',
                      [('EA', 'EA'), ('PvZ', 'Pvz')]),
        form.Textarea('text',
                      form.notnull,
                      maxlength="150",
                      description='Message (<= 150 chars)'),
        num_box('delay_secs',    'Delay until display (in SECONDS)'),
        num_box('duration_secs', 'Duration (in SECONDS)'))

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

    def GET(self):
        return render.messages(
            self.get_messages(),
            self.message_form(),
            datetime.now())

    def POST(self):
        form = self.message_form()
        now = datetime.now()
        if not form.validates():
            # FAILURE
            return render.messages(
                self.get_messages(),
                form,
                now)
        else:
            # SUCCESS
            delay_secs = int(form['delay_secs'].value)
            duration_secs = int(form['duration_secs'].value)
            desired_start_time = self.make_start_time(delay_secs)
            msg = {
                'brand': form['brand'].value,
                'text': form['text'].value,
                'delay_secs': delay_secs,
                'duration_secs': duration_secs,
                'desired_start_time': desired_start_time,
                'created_at': now
            }
            msgs.put_message(msg)
            raise web.seeother('/ui/show/messages')


    def make_start_time(self, delay_secs):
        return self.add_secs(datetime.now(), delay_secs)

    def add_secs(self, dt, secs):
        return dt + timedelta(seconds = secs)
