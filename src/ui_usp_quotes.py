import web
from web import form
import util.usp
from ui_util import render

APP = "http://polar-caverns-8587.herokuapp.com"
DEF_PROFILE_IMAGE = APP + "/static/default_profile.jpeg"

class UiUspQuotes:
    quote_form = form.Form(
        form.Textbox('name',
                     form.notnull,
                     size="100",
                     description='Name'),
        form.Textbox('image',
                     form.notnull,
                     form.regexp('^http://', "Must start with 'http://'."),
                     value=DEF_PROFILE_IMAGE,
                     size="100",
                     description='Profile Image URL'),
        form.Textarea('quote',
                      form.notnull,
                      maxlength="140",
                      description='Quote (<= 140 chars)'))

    def GET(self, brand, usp):
        form = self.quote_form()
        quotes = list(util.usp.get_quotes(brand, usp)['quotes'])
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
            quotes = list(util.usp.get_quotes(brand, usp)['quotes'])
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
            'IGNITE: Human Intelligence',
            'IGNITE: True Player Motion',
            'IGNITE: Living Worlds',
            'FIFA 14 Is Alive',
            'Madden: See It. Feel It. Live It.',
            'NBA',
            'UFC: Feel the Fight'
        ]
    }
    def GET(self, brand):
        return render.usp_quotes_index(brand, self.BRAND_2_USPS)

