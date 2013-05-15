import pytest
import gather

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

def test_get_oldest_id(tweets):
    assert gather.get_oldest_id(tweets) == '3'
    assert gather.get_oldest_id(tweets[:2]) == '2'
    with pytest.raises(ValueError):
        gather.get_oldest_id([])
