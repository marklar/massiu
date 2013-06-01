import web
from web import form
from datetime import datetime, timedelta

import util.store
from ui_util import render, num_box


class UiShowMessages:
    message_form = form.Form(
        form.Textarea('text',
                      form.notnull,
                      maxlength="150",
                      description='Message (<= 150 chars)'),
        num_box('delay_secs',    'Delay until display (in SECONDS)'),
        num_box('duration_secs', 'Duration (in SECONDS)'))

    def get_messages(self, brand):
        return {
            'active':  list(util.store.get_active_messages(brand)),
            'future':  list(util.store.get_future_messages(brand)),
            'expired': list(util.store.get_expired_messages(brand))
        }

    def make_start_time(self, delay_secs):
        return datetime.now() + timedelta(seconds = delay_secs)

    def make_end_time(self, start_time, duration_secs):
        return start_time + timedelta(seconds = duration_secs)

    def GET(self, brand):
        return render.messages(
            brand,
            self.get_messages(brand),
            self.message_form(),
            datetime.now())

    def POST(self, brand):
        form = self.message_form()
        now = datetime.now()
        if not form.validates():
            return render.messages(
                brand,
                self.get_messages(brand),
                form,
                now)
        else:
            # SUCCESS
            delay_secs = int(form['delay_secs'].value)
            duration_secs = int(form['duration_secs'].value)
            start_time = self.make_start_time(delay_secs)
            end_time = self.make_end_time(start_time, duration_secs)
            message = {
                'text': form['text'].value,
                'delay_secs': delay_secs,
                'duration_secs': duration_secs,
                'created_at': now,
                'start_time': start_time,
                'end_time': end_time
            }
            util.store.put_message(brand, message)
            raise web.seeother('/ui/messages/' + brand)
