# Make this module act as a wrapper around authlib.oauth
from www.auth.oauth import *

import django.db.models as m
from django.utils.translation import ugettext as _

from www import auth
from www.auth import oauth

class Token(m.Model):
    """
    Represents an end user of an authenticating service.
    """
    key = m.TextField(primary_key=True)
    secret = m.TextField()
    last_modified = m.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def to_dict(self):
        return {'oauth_token': self.key,
                'oauth_token_secret': self.secret}


class Protocol(Protocol):
    def __init__(self, authority):
        self.authority = authority

    def _secret_session_key(self):
        return '{}_oauth_secret_session_key'.format(self.host)

    def request(self, request, callback_url):
        """
        Request an authentication token and secret, save the secret for later,
        then redirect to an authentication url.
        """
        self.authority.auth.options['oauth_callback'] = callback_url
        data = self.authority.get_request_token()
        if not data['oauth_callback_confirmed'] == 'true':
            raise oauth.Error(_("oauth_callback not confirmed"))

        request.session[self._secret_session_key()] = data['oauth_token_secret']
        return self.authority.get_authorize_url(oauth_token=data['oauth_token'])

    def callback(self, request):
        """
        Return the credentials of an authenticating user.
        """
        try:
            secret = request.session[self._secret_session_key()]
            key = request.GET['oauth_token']
            verifier = request.GET['oauth_verifier']
        except KeyError:
            raise oauth.Error(_("Parameter missing in request!"))
        return self.authority.get_access_token(key, secret, verifier)

