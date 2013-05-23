
from util import my_time

def get_most_recent():
    return create("This is some made-up text for a message.", 600, 30)

def create(text, delay_secs, duration_secs):
    doc = {
        'text': text,
        'delay_secs': delay_secs,
        'duration_secs': duration_secs,
        'created_at': my_time.timestamp()
    }
    return doc

def get_all():
    pass
