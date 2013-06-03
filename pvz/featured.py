
from util import featured

STREAM_ROOT_NAME = 'pvz'

def get():
    return featured.get_all_featured(STREAM_ROOT_NAME)
