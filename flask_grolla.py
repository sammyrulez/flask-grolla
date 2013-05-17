from flask_oauth import OAuth
from flask import session, request,url_for,app, flash,redirect

oauth = OAuth()

twitter = None
twitter_token_getter = None
twitter_token_setter = None
twitter_after_auth = None

def twitter_session_token_getter():
    return session.get('twitter_token')

def twitter_session_token_setter(resp):
    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )

def twitter_session_after_auth(resp):
    session['twitter_user'] = resp['screen_name']

def twitter(consumer_key,consumer_secret,token_getter=twitter_session_token_getter,token_setter=twitter_session_token_setter,after_auth = None):
    twitter = oauth.remote_app('twitter',
        base_url='https://api.twitter.com/1/',
        request_token_url='https://api.twitter.com/oauth/request_token',
        access_token_url='https://api.twitter.com/oauth/access_token',
        authorize_url='https://api.twitter.com/oauth/authenticate',
        consumer_key=consumer_key,
        consumer_secret=consumer_secret
    )
    twitter_token_getter = token_getter
    twitter_token_setter = token_setter
    twitter_after_auth = after_auth


@twitter.tokengetter
def get_twitter_token(token=None):
    return twitter_token_getter()

@app.route('/twitter-login')
def login():
    return twitter.authorize(callback=url_for('twitter_authorized',
        next=request.args.get('next') or request.referrer or None))


@app.route('/twitter-authorized')
@twitter.authorized_handler
def twitter_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    twitter_token_setter(resp)
    if twitter_after_auth :
        twitter_after_auth(resp)

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)