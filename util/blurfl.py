import fetch
import simplejson as json

# obj = fetch.meta('ea_activity')
# obj = fetch.meta('bf4_highlights')
obj = fetch.meta('titanfall_activity')
print json.dumps(obj, indent=4)

