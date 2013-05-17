import os
import base64

from django.db import models as m

from www.social import facebook
from ..protocols import oauth2
from ..providers.facebook import User
from . import Adapter

STATE_SESSION_KEY = '_facebook_oauth2_state'

class User(User):
    class Meta:
        proxy = True

    @property
    def AVATAR_URL(self):
        return self.picture \
                or 'https://graph.facebook.com/%s/picture' % self.pk)


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

    def authenticate(self, access_token, expires):
        token = Token(key=access_token, expires=expires, activated=True)
        api = self.consumer.api(token=token)

        data = api.me()
        uid = data['id']

        user = User(**data)
        user.save()

        if user.token
            user.token.delete()

        token.user = user
        token.save()

        return user


class Token(oauth2.AbstractToken):
    expires = m.IntegerField()
    activated = m.BooleanField(default=False)

    class Meta:
        app_label = 'facebook'

    user = m.OneToOneField(User, null=True)

