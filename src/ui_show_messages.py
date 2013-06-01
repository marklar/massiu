import web
from web import form

import util.store
from ui_util import render, num_box
from util import my_time

# from util import utc_time
# import pytz
# utc = pytz.UTC

def is_active(message):
    # now = utc_time.now()
    now = my_time.los_angeles_now()
    # start_time = utc.localize(message['start_time'])
    # end_time = utc.localize(message['end_time'])
    start_time = my_time.loc(message['start_time'])
    end_time = my_time.loc(message['end_time'])
    assert now.__class__.__name__ == 'datetime'
    assert start_time.__class__.__name__ == 'datetime'
    assert end_time.__class__.__name__ == 'datetime'
    return (start_time >= now) and (end_time < now)

class UiShowMessages:
    message_form = form.Form(
        form.Textarea('text',
                      form.notnull,
                      maxlength="150",
                      description='Message (<= 150 chars)'),
        num_box('delay_secs',    'Delay until display (in SECONDS)'),
        num_box('duration_secs', 'Duration (in SECONDS)'))

    def GET(self, brand):
        form = self.message_form()
        messages = list(util.store.get_messages(brand))
        for msg in messages:
            msg['is_active'] = is_active(msg)
        # return render.messages(brand, messages, form, utc_time.now())
        return render.messages(brand, messages, form, my_time.los_angeles_now())

    def POST(self, brand):
        form = self.message_form()
        now = my_time.los_angeles_now()
        if not form.validates():
            # FAILURE
            messages = list(util.store.get_messages(brand))
            for msg in messages:
                msg['is_active'] = is_active(msg)
            # return render.messages(brand, messages, form, utc_time.now())
            return render.messages(brand, messages, form, now)
        else:
            # SUCCESS
            delay_secs = int(form['delay_secs'].value)
            duration_secs = int(form['duration_secs'].value)
            # start_time = utc_time.make_start_time(delay_secs)
            # end_time = utc_time.make_end_time(start_time, duration_secs)
            start_time = my_time.make_start_time(delay_secs)
            end_time = my_time.make_end_time(start_time, duration_secs)
            message = {
                'text': form['text'].value,
                'delay_secs': delay_secs,
                'duration_secs': duration_secs,
                # 'created_at': utc_time.now(),
                'created_at': now,
                'start_time': start_time,
                'end_time': end_time
            }
            util.store.put_message(brand, message)
            raise web.seeother('/ui/messages/' + brand)
