import json
import os
import tweetpony as tp

# global
global_api = None

def get_auth_data():
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        "../.auth_data.json")
    if not os.path.exists(path):
        print "No auth data!"
        return False
    with open(path, 'r') as f:
        auth_data = json.loads(f.read())
    return auth_data

def create_api():
    auth_data = get_auth_data()
    # print auth_data
    if not auth_data:
        return None
    try:
        return tp.API(
            auth_data['consumer_key'],
            auth_data['consumer_secret'],
            auth_data['access_token'],
            auth_data['access_token_secret'])
    except tp.APIError as err:
        # print "Auth failed.  Twitter error #%i: %s" % (err.code, err.description)
        return None

def get_api():
    global global_api
    if global_api is None:
        global_api = create_api()
    return global_api

def get_screen_name():
    api = get_api()
    user = api.user
    return user.screen_name

def get_num_followers(screen_name):
    api = get_api()
    try:
        user = api.get_user(
            screen_name = screen_name,
            include_entities = False
        )
    except tp.APIError as err:
        # print "Loading profile Error #%i: %s" % (err.code, err.description)
        return None
    else:
        return user.followers_count

# def tweet(api):
#     text = raw_input("What would you like to tweet? ")
#     try:
#         api.update_status(status = text)
#     except tweetpony.APIError as err:
#         print "Twitter error #%i: %s" % (err.code, err.description)
#     else:
#         print "Yay! Your tweet has been sent!"

# show_user(api)
# get_num_followers('battlefield')
