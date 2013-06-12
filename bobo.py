from datetime import datetime, tzinfo
from dateutil import tz

LA_TIME_ZONE = tz.gettz('America/Los_Angeles')
UTC_TIME_ZONE = tz.gettz('Europe/London')

# dt = datetime.utcnow()
# print dt
# print dt.utcoffset()

dt = datetime.now(LA_TIME_ZONE)

# FORMAT = '%a %b %d %H:%M:%S %Y'
FORMAT = '%b %d %H:%M:%S'
print dt.strftime(FORMAT)
