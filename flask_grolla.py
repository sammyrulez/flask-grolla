from flask_oauth import OAuth
from flask import session, request,url_for, flash,redirect
from functools import partial

oauth = OAuth()

class TwitterViewHolder(object):

    def __init__(self,twitter_oauth,token_setter,after_auth = None):
        self.twitter=twitter_oauth
        self.token_setter=token_setter
        self.after_auth = after_auth

    def twitter_login(self):
        return self.twitter.authorize(callback=url_for('twitter_authorized',next=request.args.get('next') or request.referrer or None))





    def twitter_authorized(self,resp):
        next_url = request.args.get('next') or url_for('index')
        if resp is None:
            flash(u'You denied the request to sign in.')
            return redirect(next_url)

        self.twitter_token_setter(resp)
        if self.twitter_after_auth:
            self.twitter_after_auth(resp)

        flash('You were signed in as %s' % resp['screen_name'])
        return redirect(next_url)



def twitter_session_token_getter(token = None):
    return session.get('twitter_token')

def twitter_session_token_setter(resp):
    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )

def twitter_session_after_auth(resp):
    session['twitter_user'] = resp['screen_name']




class TwitterAuth(object):

    def __init__(self,app ,consumer_key,consumer_secret,token_getter=twitter_session_token_getter,token_setter=twitter_session_token_setter,after_auth = None):
        self.twitter = oauth.remote_app('twitter',
            base_url='https://api.twitter.com/1/',
            request_token_url='https://api.twitter.com/oauth/request_token',
            access_token_url='https://api.twitter.com/oauth/access_token',
            authorize_url='https://api.twitter.com/oauth/authenticate',
            consumer_key=consumer_key,
            consumer_secret=consumer_secret
        )

        viewholder = TwitterViewHolder(self.twitter,token_setter,after_auth)


        self.twitter.tokengetter_func = token_getter
        self.twitter.authorized_handler_func = viewholder.twitter_authorized

        login_route = u'/twitter-login'
        app.add_url_rule(
            login_route,
            u'twitter_login',  # this is the name used for url_for
            partial(viewholder.twitter_login),
        )
        auth_route = u'/twitter-authorized'
        app.add_url_rule(
            auth_route,
            u'twitter_authorized',  # this is the name used for url_for
            partial(viewholder.twitter_authorized),
        )








