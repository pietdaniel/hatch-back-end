from flask import Response
import tweepy
import json
from neuhatch import app


def get_base_auth(callback=None):
    return tweepy.OAuthHandler(
        app.config['CONSUMER_KEY'],
        app.config['CONSUMER_SECRET'],
        callback=callback)


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
