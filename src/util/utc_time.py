import time
from datetime import datetime, timedelta

from dateutil import tz
LA_TIME_ZONE = tz.gettz('America/Los_Angeles')

# import pytz
# utc = pytz.UTC

# --- make times ---

def now():
    return utc.localize(datetime.utcnow())

def make_start_time(delay_secs):
    return add_secs(now(), delay_secs)

def make_end_time(start_time, duration_secs):
    return add_secs(start_time, duration_secs)

def add_secs(dt, secs):
    # return (dt + timedelta(seconds = secs)).replace(tzinfo=pytz.UTC)
    return utc.localize(dt + timedelta(seconds = secs))
