from flask import redirect, session, request, url_for, make_response
from flask.ext.login import (
    current_user, logout_user, login_user, login_required)
import tweepy
import unicodecsv

import csv
from cStringIO import StringIO
import sys

from neuhatch import app, db, login_manager, utils
from neuhatch.models import User
from neuhatch.crossdomain import crossdomain


"""This module contains the application's routes exposed over HTTP."""


@login_manager.user_loader
def load_user(userid):
    """Return a user by their id. Required by flask.ext.login."""
    return User.query.filter_by(id=userid).first()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return utils.json_response({'message': 'logout succesful'})


@app.route("/users")
@login_required
def users():
    """Return a list of all users."""
    users = User.query.all()
    out = []
    for user in users:
        out.append(user.serialize())
    return utils.json_response(out)


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
        # todo error handling
        print e
        return str(sys.exc_info())


@app.route('/callback')
def callback():
    """Oauth callback.
    Twitter will redirect the user to this route if they authenticate.
    """
    try:
        request_token = session['request_token']
        verifier = request.args.get('oauth_verifier')
        del session['request_token']
    except:
        print("error getting auth verifier or request_token")
        # todo appropriate error handling
        return str(sys.exc_info())

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
def search_for_tweets(query, max_results=1000):
    """Search for Tweets matching the given query.

    Args:
        query - String. A search query.
        max_results - Integer. Max number of tweets to return.

    Returns: a list of Tweets.
    """
    api = utils.get_user_api(current_user)
    COUNT = 100  # Tweets per page
    results = []
    for page in tweepy.Cursor(api.search, q=query, count=COUNT).pages(
            max_results/COUNT):
        results.extend(page)
    return results

@app.route('/search')
@crossdomain(origin='*')
@login_required
def search():
    """Return search results (Tweets) from Twitter for the given query.

    GET /search?q=:query

    Args:
        max_results -- Integer, the most tweets to return
    """
    query = request.args.get('q')
    max_results = request.args.get('max_results', default=100, type=int)

    return utils.json_response([
        tweet._json for tweet in search_for_tweets(query, max_results)
    ])


@app.route('/search.csv')
@crossdomain(origin='*')
@login_required
def search_csv():
    """Return a CSV export of a search query."""
    query = request.args.get('q')
    max_results = request.args.get('max_results', default=100, type=int)

    # TODO: write rows directly to the response (instead of to StringIO)
    stringbuffer = StringIO()
    fieldnames = [
        'author', 'contributors', 'coordinates',
        'created_at', 'destroy', 'entities', 'favorite',
        'favorite_count', 'favorited', 'geo', 'id', 'id_str',
        'in_reply_to_screen_name', 'in_reply_to_status_id',
        'in_reply_to_status_id_str', 'in_reply_to_user_id',
        'in_reply_to_user_id_str', 'lang', 'metadata', 'parse',
        'parse_list', 'place', 'possibly_sensitive', 'retweet',
        'retweet_count', 'retweeted', 'retweeted_status', 'retweets',
        'source', 'source_url', 'text', 'truncated', 'user'
    ]
    writer = unicodecsv.DictWriter(
        stringbuffer, fieldnames, extrasaction='ignore', encoding='utf-8')
    writer.writeheader()
    for tweet in search_for_tweets(query, max_results=1000):
        writer.writerow(tweet.__dict__)
        # writer.writerow([
        #     tweet.author, tweet.contributors, tweet.coordinates,
        #     tweet.created_at, tweet.destroy, tweet.entities,
        #     tweet.favorite, tweet.favorite_count, tweet.favorited,
        #     tweet.geo, tweet.id_str, tweet.in_reply_to_screen_name,
        #     tweet.in_reply_to_status_id,
        #     tweet.in_reply_to_status_id_str,
        #     tweet.in_reply_to_user_id, tweet.in_reply_to_user_id_str,
        #     tweet.lang, tweet.metadata, tweet.parse, tweet.parse_list,
        #     tweet.place, tweet.possibly_sensitive, tweet.retweet,
        #     tweet.retweet_count, tweet.retweeted,
        #     tweet.retweeted_status, tweet.retweets, tweet.source,
        #     tweet.source_url, tweet.text, tweet.truncated, tweet.user
        # ])
    response = make_response(stringbuffer.getvalue())
    response.mimetype = 'text/csv'
    stringbuffer.close()
    return response
