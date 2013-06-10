import requests
import json

DEF_HEADERS = {
    # 'Accept-Encoding': 'gzip',
    'Accept-Charset': 'utf-8'
}

def get_data(url, payload):
    """
    :: String, Dict -> Response data
    Make a request to MR.
    Assume it succeeds.
    Return the result data.
    """
    resp = requests.get(url, params = payload, headers = DEF_HEADERS)
    return json.loads(resp.text)
