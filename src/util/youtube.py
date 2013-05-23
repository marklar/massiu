
# TODO: Move this into secret file.
#
# For _browser_ apps with referers.
#
# Using a Browser key instead of a Server key because
# we don't have a set IP from which to make queries,
# even for my laptop.
#
# Once we move onto Heroku, we ought to be able to
# switch over to using a Server key instead.
#

import requests
import reqs

from bs4 import BeautifulSoup

BROWSER_API_KEY = 'AIzaSyC3rtngAXLrYBDukCVoD0m9HkUoHJdelos'
SERVER_API_KEY  = 'AIzaSyDmqmxd0uZ3026KoFGhT4eNHiJoaNf2hKE'

# GET https://www.googleapis.com/youtube/analytics/v1/reports?ids=channel%3D%3DBattlefield&start-date=2013-03-01&end-date=2013-03-31&metrics=views%2Ccomments%2CfavoritesAdded%2Clikes%2Cdislikes%2CestimatedMinutesWatched&key={YOUR_API_KEY}

# FIXME
# TODO: Fix me!
def get_analytics(username):
    views = 102975112
    subs = 648840
    return (views, subs)


def newest_get_data(username):
    url = 'http://www.youtube.com/user/' + username + '/videos'
    # payload = {'view': 1}
    payload = {}
    resp = requests.get(url, params = payload)
    soup = BeautifulSoup(resp.text)
    # return soup.find('span')
    return soup.find_all('span', class_='stat-value')
    return soup.find_all('div', class_='stat-entry')

def new_get_data(username):
    url = "https://www.googleapis.com/youtube/analytics/v1/reports"
    metrics = [
        'views',
        'comments',
        'favoritesAdded',
        'likes',
        'dislikes',
        'estimatedMinutesWatched'
    ]
    params = {
        'ids': 'channel%3D%3D' + username,
        'metrics': '%2C'.join(metrics),
        'key': SERVER_API_KEY
    }
    return reqs.get_data(url, params)

if __name__ == '__main__':
    # print new_get_data('Battlefield')
    print newest_get_data('Battlefield')
