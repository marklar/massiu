import time
from datetime import datetime, timedelta, date
from dateutil import tz

LA_TIME_ZONE = tz.gettz('America/Los_Angeles')
UTC_TIME_ZONE = tz.gettz('Europe/London')

DELTA_1_HOUR = timedelta(hours = 1)
DELTA_1_DAY  = timedelta(days  = 1)
DELTA_1_WEEK = timedelta(weeks = 1)

FORMAT = '%a %b %d %H:%M:%S +0000 %Y'

# --- make times ---

def make_datetime(date_str):
    """ :: String -> datetime.datetime
    e.g. 'Wed May 15 23:33:42 +0000 2013'
    """
    time_struct = time.strptime(date_str, FORMAT)
    # return datetime.fromtimestamp(time.mktime(time_struct), LA_TIME_ZONE)
    return datetime.fromtimestamp(time.mktime(time_struct), UTC_TIME_ZONE)

def loc(dt):
    return dt.replace(tzinfo=LA_TIME_ZONE)

def los_angeles_now():
    return datetime.now(LA_TIME_ZONE)

def make_start_time(delay_secs):
    return loc(los_angeles_now() + timedelta(seconds = delay_secs))

def make_end_time(start_time, duration_secs):
    return loc(start_time + timedelta(seconds = duration_secs))

# --- make strings ---

def timestamp():
    now = los_angeles_now()
    return make_timestamp(now)

def make_timestamp(dt):
    return dt.strftime(FORMAT)
