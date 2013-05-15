import pytest
import hashtags as ht

@pytest.fixture
def tweets():
    return [
        {
            'id_str': '1',
            'text': " Doesn't matter what the text is. ",
            'entities': {
                'hashtags': [
                    {'text': 'fOO'},
                    {'text': 'Bar'}
                ]
            }
        },
        {
            'id_str': '2',
            'text': "Some other text.",
            'entities': {
                'hashtags': []
            }
        },
        {
            'id_str': '3',
            'text': "More text.",
            'entities': {
                'hashtags': [
                    {'text': 'foo'},
                    {'text': 'blurfl'}
                ]
            }
        }
    ]

def test_get_hashtags(tweets):
    tweet = tweets[0]
    assert ht.get_hashtags(tweet) == ['foo', 'bar']
    
def test_has_hashtag(tweets):
    tweet = tweets[0]
    assert ht.has_hashtag(tweet, 'foo') == True

def get_ids(tweets):
    return [t['id_str'] for t in tweets]

def test_filter_by_hashtag(tweets):
    ts = ht.filter_by_hashtag(tweets, 'foo')
    assert get_ids(ts) == ['1', '3']
    ts = ht.filter_by_hashtag(tweets, 'blurfl')
    assert get_ids(ts) == ['3']
    ts = ht.filter_by_hashtag(tweets, 'quux')
    assert get_ids(ts) == []

    
