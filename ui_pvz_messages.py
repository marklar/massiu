import web
from web import form

import pvz.messages
from ui_util import render

class UiPvzMessages:
    message_form = form.Form(
        form.Textarea('text',
                      form.notnull,
                      maxlength="150",
                      description='Message (<= 150 chars):'),
        form.Textbox('cta',
                     form.notnull,
                     size="40",
                     description='Code'))

    def GET(self):
        return render.pvz_messages(
            list(pvz.messages.get_all()),
            self.message_form())

    def POST(self):
        form = self.message_form()
        if not form.validates():
            # FAILURE
            return render.pvz_messages(
                list(pvz.messages.get_all()),
                form)
        else:
            # SUCCESS
            msg = {
                'text': form['text'].value,
                'cta': form['cta']. value
            }
            pvz.messages.put_message(msg)
            raise web.seeother('/ui/messages/pvz')
