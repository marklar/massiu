import requests
import time
import sys

NUM_MINUTES = 2
HOST = 'http://polar-caverns-8587.herokuapp.com'
# HOST = 'http://localhost:5000'

def pre_fetch():
    url = HOST + '/ui/caching/prefetch'
    print url
    requests.post(url)

def tick(i):
    c = '|' if (i+1) % 6 == 0 else '.'
    sys.stdout.write(c)
    sys.stdout.flush()

if __name__ == '__main__':
    while True:
        try:
            pre_fetch()
            for i in range(0, NUM_MINUTES * 12):
                time.sleep(5)
                tick(i)
            print ''
        except requests.exceptions.ConnectionError as e:
            print str(e)
            print 'retrying in 15 secs...'
            time.sleep(15)
