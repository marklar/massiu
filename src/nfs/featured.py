
from util import featured

STREAM_ROOT_NAME = 'nfs'

def get():
    return featured.get_all_featured(STREAM_ROOT_NAME)
