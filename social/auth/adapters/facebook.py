import os
import base64

from www.social import facebook
from ..protocols import oauth2
from ..providers.facebook import User

from django.db import models as m

from utils.fields import DefaultTextField


INSTALLED = 'social.providers.facebook' in settings.INSTALLED_APPS

STATE_SESSION_KEY = '_facebook_oauth2_state'

if INSTALLED:
    class User(User):
        class Meta:
            proxy = True

        @property
        def AVATAR_URL(self):
            return self.picture \
                    or 'https://graph.facebook.com/%s/picture' % self.pk)
else:
    User.AVATAR_URL = property(lambda self: self.picture or
            'https://graph.facebook.com/%s/picture' % self.pk)

class Protocol(oauth2.Protocol):
    def request(self, request, callback_url):
        state = base64.urlsafe_b64encode(os.urandom(30))
        request.session[STATE_SESSION_KEY] = state
        return super().request(request, callback_url)

    def callback(self, request):
        try:
            session_state = request.session.pop(STATE_SESSION_KEY)
        except KeyError:
            raise facebook.Error("State missing in session")
        try:
            request_state = request.GET['state']
        except KeyError:
            raise facebook.Error("State missing in request")
        if session_state != request_state:
            raise facebook.Error("State mismatch")
        return super().callback(request)


class Adapter(Adapter):
    def __init__(self, **creds):
        self.consumer = facebook.Consumer(**creds)
        authority = self.consumer.authority()
        self.protocol = Protocol(authority=authority)

    def get_user(self, access_token, expires):
        token = Token(key=access_token, expires=expires, activated=True)
        api = self.consumer.api(token=token)

        data = api.me()
        uid = data['id']

        # Clear old token
        try:
            Token.objects.get(user_id=uid).delete()
        except Token.DoesNotExist:
            pass

        if INSTALLED:
            user = User(**data)
            user.save()

        token.user_id = uid
        token.save()

        return user if INSTALLED else uid

    def get_token(self, uid):
        return Token.objects.get(user_id=uid)


class Token(oauth2.AbstractToken):
    provider = 'facebook'

    expires = m.IntegerField()
    activated = m.BooleanField(default=False)

    if INSTALLED:
        user = m.OneToOneField(User, null=True)
    else:
        user_id = m.TextField(unique=True)

