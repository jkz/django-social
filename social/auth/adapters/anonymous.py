"""
A lightweight pluggable authentication module
"""
import django.db.models as m
from django.conf import settings

from ...providers.anonymous import models
from .. import protocols
from . import Adapter

class User(models.User):
    class Meta:
        proxy = True

    AVATAR_URL = settings.DEFAULT_AVATAR_URL


class Protocol(protocols.Protocol):
    def request(self, request, callback_url):
        return callback_url

    def callback(self, request):
        return {'session_key': request.session.session_key}


class Adapter(Adapter):
    protocol = Protocol()

    def authenticate(self, session_key):
        return User.objects.get_or_create(key=session_key)[0]


