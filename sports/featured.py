
from util.featured import get_all_featured

STREAM_PREFIX = 'sports_'

TITLE_2_HASHTAG = {
    'ufc':        'FeelTheFight',
    'fifa':       'FIFA14',
    'ea_sports':  'EASportsIgnite',
    'madden':     'MaddenNext25',
    'nba':        'WeAreLive'
}

def get(title):
    return get_all_featured(get_root(title))

def get_root(title):
    return (STREAM_PREFIX + TITLE_2_HASHTAG[title]).lower()
