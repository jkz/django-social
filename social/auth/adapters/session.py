"""
A lightweight pluggable authentication module
"""
import django.db.models as m
from django.conf import settings

from ..auth import views
from .. import protocols
from . import Adapter

class SessionUserMiddleware:
    """
    This middleware makes sure there is an authenticated user present on every
    request, by creating a User object for the session_key when needed.
    """
    def process_request(self, request):
        #TODO set some conditions to not create a shitload of session users for
        # robots and jokers
        if not request.user.is_authenticated():
            if not request.session.get(views.PROVIDER_SESSION_KEY, False):
                views.connect(request, provider='session')
                views.callback(request)


class Protocol(protocols.Protocol):
    def request(self, request, callback_url):
        return callback_url

    def callback(self, request):
        return {'session_key': request.session.session_key}


class Adapter(Adapter):
    protocol = Protocol()

    def authenticate(self, session_key):
        return User.objects.get_or_create(key=session_key)[0]


#TODO: these models should be imported conditionally
class User(m.Model):
    session_key = m.TextField(primary_key=True)

    AVATAR_URL = settings.DEFAULT_AVATAR_URL

    def __str__(self):
        return 'Anonymous User {}'.format(self.pk)

