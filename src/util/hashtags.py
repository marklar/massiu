#
# Functions related to tweets' hashtags.
#

import re

def make_re(hashtag):
    return re.compile("^%s$" % hashtag, re.IGNORECASE)

def get_hashtags(tweet):
    return [tag['text'].lower()
            for tag in tweet['entities']['hashtags']]

def has_hashtag(tweet, hashtag):
    """ Tweet, String -> Boolean """
    return hashtag in get_hashtags(tweet)

def filter_by_hashtag(tweets, hashtag):
    return filter(lambda t: has_hashtag(t, hashtag),
                  tweets)

def show_tweets(tweets):
    """ Just for debugging purposes. """
    print 'How many tweets?'
    print len(tweets)
    print ''
    print 'hashtags:'
    for tw in tweets:
        hts = get_hashtags(tw)
        print hts
        # if len(hts) == 0:
        if True:
            print tw
            print ''
    print ''

