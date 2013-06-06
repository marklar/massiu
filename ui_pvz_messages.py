import web
from web import form

import pvz.messages
from ui_util import render

class UiPvzMessages:
    message_form = form.Form(
        form.Textarea('text',
                      form.notnull,
                      maxlength="150",
                      description='Message (<= 150 chars):'))

    def GET(self):
        return render.pvz_messages(
            pvz.messages.get_all(),
            self.message_form())

    def POST(self):
        form = self.message_form()
        if not form.validates():
            # FAILURE
            return render.pvz_messages(
                pvz.messages.get_all(),
                form)
        else:
            # SUCCESS
            msg = { 'text': form['text'].value }
            pvz.messages.put_message(msg)
            raise web.seeother('/ui/messages/pvz')
