import pytest
import store

@pytest.fixture
def tweets():
    return [
        {u'id': 1234, u'text': u'foo'},
        {u'id': 2345, u'text': u'bar'}
    ]

@pytest.fixture
def repeated_tweets():
    return [
        {u'id': 1234, u'text': u'foo'},
        {u'id': 1234, u'text': u'foo'},
        {u'id': 2345, u'text': u'bar'},
        {u'id': 2345, u'text': u'bar'},
        {u'id': 2345, u'text': u'bar'}
    ]

def test_with_db_ids(tweets):
    expected_ids = [1234, 2345]
    new_ids = [t['_id'] for t in store.with_db_ids(tweets)]
    assert new_ids == expected_ids

#----------
# The following tests require MongoDB to be running.
#----------

COLLECTION_NAME = 'test_collection'

def drop():
    store.get_db()[COLLECTION_NAME].drop()

def test_put(tweets):
    drop()
    store.put(COLLECTION_NAME, tweets)
    with_ids = store.with_db_ids(tweets)
    assert list(store.get_all(COLLECTION_NAME)) == with_ids
    drop()

def test_put_repeated(repeated_tweets, tweets):
    drop()
    store.put(COLLECTION_NAME, repeated_tweets)
    with_ids = store.with_db_ids(tweets)
    assert list(store.get_all(COLLECTION_NAME)) == with_ids
    drop()

