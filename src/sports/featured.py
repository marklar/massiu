
from util.featured import get_all_featured

STREAM_ROOTS = [
    'sports_' + s.lower()
    for s in [
        'FeelTheFight',
        'FIFA14',
        'EASportsIgnite',
        'MaddenNext25',
        'WeAreLive'
    ]
]

def get_all():
    return [get_all_featured(sr) for sr in STREAM_ROOTS]
