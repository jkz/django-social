import django.db.models as m

from www import auth
from www.auth import oauth2

from . import Protocol

class Token(m.Model):
    key = m.TextField(primary_key=True)
    #created_time = m.DateTimeField()
    last_modified = m.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Protocol(Protocol):
    def __init__(self, authority):
        self.authority = authority

    def _callback_session_key(self):
        return '{}_oauth2_callback_session_key'.format(self.authority.connection.host)

    def _secret_session_key(self):
        return '{}_oauth2_secret_session_key'.format(self.authority.connection.host)

    def request(self, request, callback_url, **kwargs):
        # Callback url is saved so it can be passed to an exchange_code call.
        request.session[self._callback_session_key()] = callback_url
        return self.authority.request_code(callback_url, **kwargs)

    def callback(self, request, **kwargs):
        if request.GET.get('error'):
            raise oauth2.Error('oauth2', request.GET.get('error_description'))

        code = request.GET.get('code')
        if not code:
            raise oauth2.Error('oauth2', "Code missing in request!")

        # Retrieve the callback url that was saved, otherwise build it
        callback_url = request.session.get(
                self._callback_session_key(),
                request.build_absolute_uri(request.path))

        return self.authority.exchange_code(code, callback_url, **kwargs)

