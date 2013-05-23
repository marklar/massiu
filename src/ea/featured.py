#------------------
# Featured tweets

# More may be added later.
# Use fetch.meta() to get keywords for stream meta-info.
#
# There are two MR streams:
#   - ea_featured
#   - ea_starred  -- take precedence
#

from util.featured import get_all_featured

STREAM_ROOT = 'ea'

def get_ea():
    return get_all_featured(STREAM_ROOT)
