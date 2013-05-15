import pytest
import gather

@pytest.fixture
def tweets():
    return [
        { 'id_str': '1' },  # oldest (comes first)
        { 'id_str': '2' },
        { 'id_str': '3' }   # newest
    ]

def test_get_oldest_id(tweets):
    assert gather.get_oldest_id(tweets) == '1'
    assert gather.get_oldest_id(tweets[1:]) == '2'
    with pytest.raises(IndexError):
        gather.get_oldest_id([])

def test_get_newest_id(tweets):
    assert gather.get_newest_id(tweets) == '3'
    assert gather.get_newest_id(tweets[:-1]) == '2'
    with pytest.raises(IndexError):
        gather.get_newest_id([])

# def test_gone_back_enough(tweets):
#     assert gather.gone_back_enough(None, tweets) == False
#     assert gather.gone_back_enough(None, []) == False
#     assert gather.gone_back_enough('2', []) == False
#     assert gather.gone_back_enough('4', tweets) == False
#     assert gather.gone_back_enough('1', tweets) == True
#     assert gather.gone_back_enough('2', tweets) == True
#     assert gather.gone_back_enough('3', tweets) == True

