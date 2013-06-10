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

def num_str_box(name, desc, max_len=4):
    return form.Textbox(
        name,
        form.notnull,
        size=str(max_len),
        maxlength=str(max_len),
        description=desc)
