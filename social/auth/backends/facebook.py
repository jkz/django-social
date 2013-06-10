import os
import base64

from django.db import models as m

from www.social import facebook
from ..protocols import oauth2
from ...providers.facebook import models
from . import Backend

STATE_SESSION_KEY = '_facebook_oauth2_state'

class ProxyUser(models.User):
    class Meta:
        proxy = True
        app_label = 'facebook'

    @property
    def AVATAR_URL(self):
        return (self.picture
                or 'https://graph.facebook.com/{}/picture'.format(self.pk))
User = ProxyUser


class Protocol(oauth2.Protocol):
    def direct(self, request):
        creds = {}
        for key_in, key_out in [
                ('accessToken', 'access_token'),
                ('expiresIn', 'expires')]:

            try:
                creds[key_out] = request.POST[key_in]
            except KeyError:
                raise facebook.Error("{} missing in POST".format(key_in))
        return creds


    def request(self, request, callback_url):
        state = str(base64.urlsafe_b64encode(os.urandom(30)))
        request.session[STATE_SESSION_KEY] = state
        return super(Protocol, self).request(request, callback_url, state=state)

    def callback(self, request):
        try:
            session_state = request.session.pop(STATE_SESSION_KEY)
        except KeyError:
            raise facebook.Error("State missing in session")
        try:
            request_state = request.GET['state']
        except KeyError:
            raise facebook.Error("State missing in request")
        #if session_state != request_state:
        #    raise facebook.Error("State mismatch")
        return super(Protocol, self).callback(request)


class Backend(Backend):
    def init(self, **creds):
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

        try:
            user.token.delete()
        except Token.DoesNotExist:
            pass

        token.user = user
        token.save()

        return user


class Token(oauth2.Token):
    expires = m.IntegerField()
    activated = m.BooleanField(default=False)

    class Meta:
        app_label = 'facebook'

    user = m.OneToOneField(User, null=True)

from django.db.models.loading import register_models
register_models('facebook', User, Token)
