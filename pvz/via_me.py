import re
import requests
from bs4 import BeautifulSoup

def get_pic_from_tweet(tweet):
    url = tweet['entities']['urls'][0]['expanded_url']
    m = re.search('via\.me', url)
    if m is None:
        return None
    else:
        return get_pic_from_url(url)

def get_pic_from_url(url):
    """ example url: 'http://via.me/-cpr104s' """
    resp = requests.get(url)
    html = resp.text
    return get_pic_from_html(html)

#---------------------------

BOGUS_RE = re.compile(
    r'<!-- RadiumOne code begin -->.*<!-- RadiumOne code end -->',
    flags=re.DOTALL)

def get_pic_from_html(html):
    html = re.sub(BOGUS_RE, '', html)
    soup = BeautifulSoup(html)
    div = soup.find(class_="main_pic_container")
    return div.find('img')['src']

if __name__ == '__main__':
    # import doc
    # print get_pic_from_html(doc.html)
    url = 'http://via.me/-cpr104s'
    print get_pic_from_url(url)
