import bf4.counts
from util import gather

gather.all_tweets('ea_activity')
print bf4.counts.num_tweets()
