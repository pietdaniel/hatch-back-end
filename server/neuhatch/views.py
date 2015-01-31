import tweepy, sys
from flask import redirect, session, request, url_for
from neuhatch import config, app

@app.route("/oauth")
def oauth():
    try:
        callback_url = "%s%s" % ("http://localhost:5000", url_for("callback"))
        auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret, callback_url)
        redirect_url = auth.get_authorization_url()
        session['request_token'] = auth.request_token
        return redirect(redirect_url)
    except tweepy.TweepError as e:
        return 'Failed to get request token %s' % e
    except:
        return str(sys.exc_info())


@app.route('/callback')
def callback():
    try:
        auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
        token = session['request_token']
        del session['request_token']
        auth.request_token = token
        verifier = request.args.get('oauth_verifier')
    except:
        return str(sys.exc_info())

    try:
        auth.get_access_token(verifier)
        key = auth.access_token
        secret = auth.access_token_secret
        auth.set_access_token(key, secret)
        api = tweepy.API(auth)
        return str(api.me())
    except:
        return str(sys.exc_info())

def get_default_api():
    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)
    api = tweepy.API(auth)
    return api
