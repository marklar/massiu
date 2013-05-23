import time
from datetime import datetime, timedelta, date
from dateutil import tz

LA_TIME_ZONE = tz.gettz('America/Los_Angeles')

DELTA_1_HOUR = timedelta(hours = 1)
DELTA_1_DAY  = timedelta(days  = 1)
DELTA_1_WEEK = timedelta(weeks = 1)

FORMAT = "%a %b %d %H:%M:%S +0000 %Y"

def make_datetime(date_str):
    """ :: String -> datetime.datetime
    e.g. 'Wed May 15 23:33:42 +0000 2013'
    """
    time_struct = time.strptime(date_str, FORMAT)
    return datetime.fromtimestamp(time.mktime(time_struct), LA_TIME_ZONE)

def timestamp():
    now = los_angeles_now()
    return now.strftime(FORMAT)

def los_angeles_now():
    return datetime.now(LA_TIME_ZONE)
