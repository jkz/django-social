# Make this module a wrapper around authlib.oauth2
from authlib.oauth import *

import django.db.models as m
from django.shortcuts import redirect

from authlib import oauth2

from utils.fields import TimestampField


#TODO: the callback_url system is shaky (and has TMI atm)
def CALLBACK_KEY(request):
    return request.namespace + '_oauth2_callback_url'

class Token(m.Model, oauth2.Token):
    key = m.TextField(primary_key=True)
    created_time = TimestampField()
    last_modified = m.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class App(m.Model, oauth2.App):
    key = m.TextField(primary_key=True)
    secret = m.TextField()

    class Meta:
        abstract = True

    def auth_request(self, request, callback_url, **kwargs):
        # Callback url is saved so it can be passed to an exchange_code call.
        request.session[CALLBACK_KEY(request)]= callback_url
        return redirect(self.oauth2().request_code(callback_url, **kwargs))

    def auth_callback(self, request):
        if request.GET.get('error'):
            raise oauth2.Error('oauth2', request.GET.get('error_description'))

        code = request.GET.get('code')
        if not code:
            raise oauth2.Error('oauth2', "Code missing in request!")

        # Retrieve the callback url that was saved, otherwise build it
        callback_url = request.session.get(
                CALLBACK_KEY(request),
                request.get_host() + request.path)

        creds = self.oauth2().exchange_code(code, callback_url, **kwargs)
        return self.process_creds(**creds)

    def process_credentials(self, **creds):
        raise NotImplementedError

