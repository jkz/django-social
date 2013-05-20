from django.db import models as m

from www.social import soundcloud
from ..protocols import oauth2
from ..providers.soundcloud import models
from . import Backend

from django.conf import settings

PARAMS = PROVIDERS.get('soundcloud', {}).get('auth_params', {})

class User(models.User):
    class Meta:
        proxy = True

    @property
    def AVATAR_URL(self):
        return self.avatar_url

if not 'display' in PARAMS:
    PARAMS['display'] = 'popup'
if not 'response_type' in PARAMS:
    PARAMS['response_type'] = 'code'
if not 'scope' in PARAMS:
    PARAMS['scope'] = 'non-expiring'

class Protocol(oauth2.Protocol):
    def request(self, request, **kwargs):
        params = PARAMS.copy()
        params.update(kwargs)
        return super().request(request, **params)


class Backend(Backend):
    def init(self, **creds):
        self.consumer = soundcloud.Consumer(**creds)
        authority = self.consumer.authority()
        self.protocol = Protocol(authority=authority)

    def authenticate(self, access_token, scope):
        token = Token(key=access_token, scope=scope, activated=True)
        api = self.consumer.api(token=token)

        data = api.me()
        user = User.importer.put(**data)
        if user.token:
            user.token.delete()

        token.user = user
        token.save()
        return user


class Token(oauth2.AbstractToken):
    scope = m.TextField()
    user = m.OneToOneField(User, null=True)

    activated = m.BooleanField(default=False)

    class Meta:
        app_label = 'soundcloud'

