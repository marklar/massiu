import pytest
import nfs_leaderboard as lb

@pytest.fixture
def tweets():
    return [
        {'text': " Aaaa Wong : 2:32.10  "},
        {'text': " Bbbb Wong : 4:32.10  "},
        {'text': " Cccd Wong : 5:32.10  "},
        {'text': " Dddd Wong : 1:32.10  "},
        {'text': " Eeee Wong : 3:32.10  "},
        {'text': " Ffff Wong : 8:32.10  "},
        {'text': " Gggg Wong : 0:32.10  "}
    ]

def test_get_name_and_time(tweets):
    tweet = tweets[0]
    expected = {
        'name': 'Aaaa Wong',
        'time_str': '2:32.10',
        'secs': 152.1
    }
    assert lb.get_name_and_time(tweet) == expected


def test_select_top_names(tweets):
    expected = [
        {'name': 'Gggg Wong', 'time_str': '0:32.10'},
        {'name': 'Dddd Wong', 'time_str': '1:32.10'}
    ]
    assert lb.select_top_times(2, tweets) == expected
