import requests
import time

NUM_MINUTES = 3
HOST = 'http://polar-caverns-8587.herokuapp.com'
# HOST = 'http://localhost:5000'

TO_FETCH = [
    '/api/bf4/highlights.json',

    '/api/ea/fb_likes.json',
    '/api/ea/featured.json',
    '/api/ea/activity.json',

    '/api/sports/featured/ea_sports.json',
    '/api/sports/featured/fifa.json',
    '/api/sports/featured/madden.json',
    '/api/sports/featured/nba.json',
    '/api/sports/featured/ufc.json',

    '/api/nfs/featured.json',
    '/api/nfs/game_stats.json',

    '/api/pvz/photos.json',
    '/api/pvz/featured.json'
]

def pre_fetch():
    for path in TO_FETCH:
        url = HOST + path
        requests.post(url)
        print url

if __name__ == '__main__':
    while True:
        pre_fetch()
        for i in range(0, NUM_MINUTES * 2):
            print '.'
            time.sleep(30)
