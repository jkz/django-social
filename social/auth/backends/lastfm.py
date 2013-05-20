from django.db import models as m

from utils.fields import DefaultTextField

from www.social import lastfm
from ...providers.lastfm import models
from .. import protocols
from . import Backend

class User(models.User):
    class Meta:
        proxy = True

    @property
    def AVATAR_URL(self):
        return (self.image_medium
                or self.image_small
                or self.image_large
                or self.image_extralarge)


class Protocol(protocols.Protocol):
    def init(self, authority):
        self.authority = authority

    def request(self, request, redirect_uri, **kwargs):
        return self.authority.auth_request(redirect_url, **kwargs)

    def callback(self, request, **kwargs):
        token = request.GET['token']
        return self.authority.auth_callback(token=token, **kwargs)


class Backend(Backend):
    def init(self, **creds):
        self.consumer = lastfm.Consumer(**creds)
        authority = lastfm.API(consumer=consumer)
        self.protocol = Protocol(authority=authority)

    def authenticate(self, key):
        from .. import parsers
        token, created  = Token.objects.get_or_create(key=key)

        api = lastfm.API(consumer=self.consumer, token=token)
        data = api.get_user()

        user = parsers.import_user(data['user'])
        if user.token:
            user.token.delete()

        token.user = user
        token.save()
        return user


class Token(m.Model):
    key = m.TextField(primary_key=True)
    user = m.ForeignKey(User, null=True, related_name='tokens')

    class Meta:
        app_label = 'lastfm'

