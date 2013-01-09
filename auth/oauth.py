# Make this module act as a wrapper around authlib.oauth
from authlib.oauth import *

import django.db.models as m

import authlib.oauth as oauth

class Token(m.Model, oauth.Token):
    """
    Represents an end user of an auhtenticating service.
    """
    key = m.TextField(primary_key=True)
    secret = m.TextField()

    class Meta:
        abstract = True
        unique_together = [('user', 'app')]

    def to_dict(self):
        return {'oauth_token': self.key,
                'oauth_token_secret': self.secret}


class App(m.Model, oauth.App):
    key = m.TextField(primary_key=True)
    secret = m.TextField()

    class Meta:
        abstract = True

    @property
    def oauth_session_key(self):
        return '%s_oauth_session_key' % self._meta.app_label

    def auth_request(self, request, callback_url):
        """
        Request an authentication token and secret, save the secret for later,
        then redirect to an authentication url.
        """
        provider = self.oauth()
        provider.auth.options['oauth_callback'] = callback_url
        data = provider.get_request_token()
        if not data['oauth_callback_confirmed'] == 'true':
            raise oauth.Error('oauth_callback not confirmed')

        request.session[self.oauth_session_key] = data['oauth_token_secret']
        return redirect(provider.get_authorize_url(oauth_token=data['oauth_token']))

    def auth_callback(self, request):
        """
        Return the credentials of an authenticating user.
        """
        try:
            secret = request.session[self.oauth_session_key]
            key = request.GET['oauth_token']
            verifier = request.GET['oauth_verifier']
        except KeyError:
            raise oauth.Error("Parameter missing in request!")
        provider = self.oauth()
        token, query = provider.get_access_token(key, secret, verifier)
        return self.process_access_token(token, **query)

    def process_creds(self, oauth_token, **query):
        return oauth_token

