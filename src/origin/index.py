#
# TODO: Create a MongoDB collection for this data.
#
# 

from util import store

def accept_form_submission():
    # FIXME
    doc = {
        'logins': 1,
        'gamers': 1,
        'games_today': 1
    }
    store.put_origin_data(doc)


def show_form_for_entering_origin_data():
    """
    Data:
    + total number of logins
    + total number of gamers
    + number of games played today

    Create HTML for form.
    Populate with previous values, if any.
    """
    (logins, gamers, games) = get_data()
    # Move this to api.py so as to use template rendering.


def get_data():
    data = store.get_origin_data()
    if data is not None:
        return (data['logins'], data['gamers'], data['games_today'])
    else:
        return (0, 0, 0)
    
