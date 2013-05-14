import os
import base64

import auths.contrib.oauth2 as oauth2
from ..protocols import oauth2
import sociallib.facebook as facebook

from django.db import models as m

from utils.fields import DefaultTextField

from .objects import User

ACTIVE = 'social.providers.facebook' in settings.INSTALLED_APPS

STATE_SESSION_KEY = '_facebook_oauth2_state'
CALLBACK_SESSION_KEY = '_facebook_oauth2_callback_url'

class Provider(facebook.Provider, oauth2.Provider):
    def auth_request(self, request, callback_url):
        state = base64.urlsafe_b64encode(os.urandom(30))
        request.session[STATE_SESSION_KEY] = state
        #request.session[CALLBACK_SESSION_KEY] = callback_url
        return super(Provider, self).auth_request(request, callback_url,
                state=state)
        return self.request_code(callback_url, state=state)

    def auth_callback(self, request):
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
        return super(Provider, self).auth_callback(request)
        try:
            code = request.GET['code']
        except KeyError:
            raise facebook.Error("Code missing in request")
        callback_url = request.session.pop(
                CALLBACK_SESSION_KEY,
                request.build_absolute_uri(request.path))
        return self.exchange_code(code, callback_url)



class Consumer(facebook.Consumer):
    def get_user(self, access_token, expires):
        token = Token(key=access_token, expires=expires, activated=True)
        token.consumer = self
        data = token.api.me()
        user = User(**data)
        user.save()
        Token.objects.filter(user=user).exclude(key=access_token).delete()
        token.user = user
        token.save()
        return user

    def get_token(self, uid):
        return Token.objects.get(user_id=uid)


class Token(oauth2.AbstractToken):
    provider = 'facebook'

    expires = m.IntegerField()
    activated = m.BooleanField(default=False)

    if ACTIVE:
        user = m.OneToOneField(facebook.User, null=True)

        class Meta:
            app_label = 'facebook'
    else:
        user_id = m.TextField(unique=True)


User.AVATAR_URL = property(lambda self: self.picture or
        'https://graph.facebook.com/%s/picture' % self.pk)
