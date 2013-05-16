import json
import os
import tweetpony as tp

def get_auth_data():
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        ".auth_data.json")
    if not os.path.exists(path):
        print "No auth data!"
        return False
    with open(path, 'r') as f:
        auth_data = json.loads(f.read())
    return auth_data

def get_api():
    auth_data = get_auth_data()
    if not auth_data:
        return False
    try:
        return tp.API(
            auth_data['consumer_key'],
            auth_data['consumer_secret'],
            auth_data['access_token'],
            auth_data['access_token_secret'])
    except tp.APIError as err:
        print "Auth failed.  Twitter error #%i: %s" % (err.code, err.description)
        return False

def show_user(api):
    user = api.user
    print "Hello, @%s!" % user.screen_name

def get_num_followers(api, username):
    try:
        user = api.get_user(
            screen_name = username,
            include_entities = False
        )
    except tweetpony.APIError as err:
        print "Loading profile Error #%i: %s" % (err.code, err.description)
    else:
        # print "Screen name:", user.screen_name
        # print "Num followers:", user.followers_count
        return user.followers_count

# def tweet(api):
#     text = raw_input("What would you like to tweet? ")
#     try:
#         api.update_status(status = text)
#     except tweetpony.APIError as err:
#         print "Twitter error #%i: %s" % (err.code, err.description)
#     else:
#         print "Yay! Your tweet has been sent!"

api = get_api()
# show_user(api)
get_num_followers(api, 'battlefield')
