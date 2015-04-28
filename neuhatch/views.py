from flask import redirect, session, request, url_for, make_response
from flask.ext.login import (
    current_user, logout_user, login_user, login_required)
from cStringIO import StringIO
from neuhatch import app, db, login_manager, utils
from neuhatch.models import User

import sys
import tweepy
import unicodecsv

"""This module contains the application's routes exposed over HTTP."""

@login_manager.user_loader
def load_user(userid):
    """Return a user by their id. Required by flask.ext.login."""
    return User.query.filter_by(id=userid).first()

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(app.config['FRONTEND'], code=302)

@app.route("/oauth")
def oauth():
    """Start the oauth login process."""
    if not current_user.is_anonymous():
        return redirect(url_for('user'))

    try:
        auth = utils.get_base_auth(
            callback=(app.config['HOSTNAME'] + url_for('callback')))
        authorization_url = auth.get_authorization_url()
        session['request_token'] = auth.request_token
        return redirect(authorization_url)
    except tweepy.TweepError as e:
        return 'Failed to get request token %s' % e
    except Exception as e:
        return 'Failed with error %s' % e

@app.route('/callback')
def callback():
    """Oauth callback.
    Twitter will redirect the user to this route if they authenticate.
    """
    try:
        request_token = session['request_token']
        verifier = request.args.get('oauth_verifier')
        del session['request_token']
    except Exception as e:
        print("error getting auth verifier or request_token")
        return 'Failed with error %s' % e

    username, key, secret = utils.verify_api(request_token, verifier)

    user = User.query.filter_by(username=username).first()

    # create user if first time
    if user is None:
        user = User(username, key, secret)
        print("Creating user %s: %s" % (username, user,))
        db.session.add(user)
        db.session.commit()

    print("Logging in user %s" % user)
    login_user(user)

    return redirect(app.config['FRONTEND'], code=302)

@app.route('/user')
@login_required
def user():
    """Return the logged in user."""
    return utils.json_response({
        'id': current_user.id,
        'username': current_user.username
    })

@login_required
def search_for_tweets(query, max_results=1000, per_page=10):
    """Search for Tweets matching the given query.

    Args:
        query - String. A search query.
        max_results - Integer. Max number of tweets to return.

    Returns: a list of Tweets.
    """
    api = utils.get_user_api(current_user)
    results = []
    for page in tweepy.Cursor(api.search, q=query, count=per_page).pages(max_results / per_page):
        results.extend(page)
    return results


@app.route('/search')
@login_required
def search():
    """Return search results (Tweets) from Twitter for the given query.

    GET /search?q=:query

    Args:
        max_results -- Integer, the most tweets to return
    """
    query = request.args.get('q')
    max_results_param = request.args.get('max_results', default=100, type=int)
    max_results_multiplier = min(max_results_param / 100, 10)
    max_results = max_results_multiplier * 100

    return utils.json_response([
        tweet._json for tweet in search_for_tweets(query, max_results=max_results)
    ])

@app.route('/search.csv')
@login_required
def search_csv():
    """Return a CSV export of a search query."""
    query = request.args.get('q')
    response = make_response(build_csv(query))
    response.mimetype = 'text/csv'
    return response

def build_csv(query):
    ## TODO: write rows directly to the response (instead of to StringIO)
    max_results_param = request.args.get('max_results', default=100, type=int)
    max_results_multiplier = min(max_results_param / 100, 10)
    max_results = max_results_multiplier * 100

    stringbuffer = StringIO()
    fieldnames = [
        'author', 'contributors', 'coordinates',
        'created_at', 'destroy', 'favorite',
        'favorite_count', 'favorited', 'geo', 'id', 'id_str',
        'in_reply_to_screen_name', 'in_reply_to_status_id',
        'in_reply_to_status_id_str', 'in_reply_to_user_id',
        'in_reply_to_user_id_str', 'lang', 'metadata', 'parse',
        'parse_list', 'place', 'possibly_sensitive', 'retweet',
        'retweet_count', 'retweeted', 'retweeted_status', 'retweets',
        'source', 'source_url', 'text', 'truncated', 'user'
    ]
    writer = unicodecsv.DictWriter(stringbuffer, fieldnames, extrasaction='ignore', encoding='utf-8')
    writer.writeheader()

    for tweet in search_for_tweets(query, max_results=max_results):
        del tweet.__dict__['entities']
        author = tweet.__dict__['author']
        tweet.__dict__['author'] = "%s (@%s)" % (author.name, author.screen_name)
        user = tweet.__dict__['user']
        tweet.__dict__['user'] = "%s (@%s)" % (user.name, user.screen_name)
        writer.writerow(tweet.__dict__)

    try:
      return stringbuffer.getvalue()
    finally:
      stringbuffer.close()
