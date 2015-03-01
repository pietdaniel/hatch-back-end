import tweepy, sys, json
from flask import redirect, session, request, url_for, jsonify, Response, request
from flask.ext.login import logout_user, login_user, login_required, current_user
from neuhatch import config, app, db, login_manager
from neuhatch.models import User
from neuhatch.crossdomain import crossdomain

@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()


@app.route("/users")
def users():
    users = User.query.all()
    out = []
    for user in users:
        out.append(user.serialize())
    return json.dumps(out)


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
        print("error getting auth verifier or request_token")
        return str(sys.exc_info())

    auth.get_access_token(verifier)
    key = auth.access_token
    secret = auth.access_token_secret
    auth.set_access_token(key, secret)

    api = tweepy.API(auth)
    username = api.me().screen_name
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username, key, secret)
        print("Creating user %s: %s" % (username, user,))
        db.session.add(user)
        db.session.commit()
    print("Logging in user %s" % user)
    login_user(user)

    return redirect(config.hostname)


@app.route('/user')
@login_required
def user():
    return str((current_user.id, current_user.access_token, current_user.access_token_secret))


@app.route('/search')
@crossdomain(origin='*')
@login_required
def search():
    user = User.query.filter_by(username="test").first()

    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    key = auth.access_token
    secret = auth.access_token_secret
    auth.set_access_token(key, secret)
    api = tweepy.API(auth)

    query = request.args.get('q')

    results = api.search(q=query)
    output = []
    for result in results:
        output.append(result._json)
    out_json = json.dumps(output)
    return Response(out_json, mimetype="application/json")
