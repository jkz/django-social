# Make this module a wrapper around authlib.oauth2
from authlib.oauth import *

import django.db.models as m

from authlib import oauth2

class AbstractToken(m.Model, oauth2.Token):
    key = m.TextField(primary_key=True)
    #created_time = m.DateTimeField()
    last_modified = m.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractConsumer(m.Model, oauth2.App):
    key = m.TextField(primary_key=True)
    secret = m.TextField()

    class Meta:
        abstract = True

    def auth_process(self, **creds):
        return creds


class Provider(oauth.Provider):
    def secret_session_key(self):
        return '{}_oauth2_secret_session_key'.format(self.host)

    def auth_request(self, request, callback_url, **kwargs):
        # Callback url is saved so it can be passed to an exchange_code call.
        request.session[self.secret_session_key()] = callback_url
        return self.request_code(callback_url, **kwargs)

    def auth_callback(self, request, **kwargs):
        if request.GET.get('error'):
            raise oauth2.Error('oauth2', request.GET.get('error_description'))

        code = request.GET.get('code')
        if not code:
            raise oauth2.Error('oauth2', "Code missing in request!")

        # Retrieve the callback url that was saved, otherwise build it
        callback_url = request.session.get(
                self.secret_session_key(),
                request.get_host() + request.path)

        return self.exchange_code(code, callback_url, **kwargs)

