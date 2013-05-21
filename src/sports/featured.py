#
# VH: "one for each of the titles needs created" ??
# 

from util.featured import featured

# could simplify this by changing the name of the 'ignite' stream
HASHTAGS = [
    'FeelTheFight',
    'FIFA14',
    'EASportsIgnite',
    'MaddenNext25',
    'WeAreLive'
]

def foo(hashtag):
    return lambda: featured('sports_' + hashtag.lower(), '#' + hashtag)

# stream_name, hashtag
feel_the_fight = foo('FeelTheFight')
fifa_14        = foo('FIFA14')
ignite         = foo('EASportsIgnite')
madden_next_25 = foo('MaddenNext25')
we_are_alive   = foo('WeAreLive')

FNS = [feel_the_fight, fifa_14, ignite, madden_next_25, we_are_alive]

def get_all():
    return [f() for f in FNS]

