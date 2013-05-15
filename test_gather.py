import pytest
import gather

@pytest.fixture
def tweets():
    return [
        {
            'id': 1,
            'text': " Doesn't matter what the text is. ",
            'entities': {
                'hashtags': [
                    {'text': 'fOO'},
                    {'text': 'Bar'}
                ]
            }
        },
        {
            'id': 2,
            'text': "Some other text.",
            'entities': {
                'hashtags': []
            }
        },
        {
            'id': 3,
            'text': "More text.",
            'entities': {
                'hashtags': [
                    {'text': 'foo'},
                    {'text': 'blurfl'}
                ]
            }
        }
    ]

# def test_get_low_id(tweets):
#     assert gather.get_low_id(tweets) == 1
#     assert gather.get_low_id(tweets[1:]) == 2
#     with pytest.raises(ValueError):
#         gather.get_low_id([])
