import web
from web import form

render = web.template.render('templates/')

def num_box(name, desc):
    return form.Textbox(
        name,
        form.notnull,
        form.regexp('^\s*\d+\s*$', "Digits only, please."),
        size="10",
        description=desc)

def num_str_box(name, desc):
    return form.Textbox(
        name,
        form.notnull,
        size="12",
        description=desc)
