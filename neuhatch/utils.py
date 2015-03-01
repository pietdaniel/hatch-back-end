from flask import Response
import tweepy, sys, json
from flask.ext.login import logout_user, logout_user, login_required, current_user
from neuhatch import config, app, db, login_manager

def get_base_auth():
    return tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)

def verify_api(request_token, verifier):
    """
      Returns (username, key, secret)
    """
    auth = get_base_auth()
    # set request token
    auth.request_token = request_token
    # turn request token + verifier into access token + secret
    auth.get_access_token(verifier)
    key = auth.access_token
    secret = auth.access_token_secret
    auth.set_access_token(key, secret)
    # get api
    api = tweepy.API(auth)
    # return username, key, secret
    username = api.me().screen_name
    return (username, key, secret)

def get_user_api(user):
    auth = get_base_auth()
    key = user.access_token
    secret = user.access_token_secret
    auth.set_access_token(key, secret)
    return tweepy.API(auth)

def json_response(data):
    out_json = json.dumps(data)
    return Response(out_json, mimetype='application/json')
