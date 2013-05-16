import os
import base64

import auths.contrib.oauth2 as oauth2
import sociallib.facebook as facebook

from django.db import models as m

from utils.fields import DefaultTextField

from .objects import User

STATE_SESSION_KEY = '_facebook_oauth2_state'
CALLBACK_SESSION_KEY = '_facebook_oauth2_callback_url'

'''
class Provider(oauth2.App, facebook.App):
    name = 'Facebook'

    #namespace = DefaultTextField()
    description = DefaultTextField()
    website = DefaultTextField()

    icon = DefaultTextField()

    email_support = DefaultTextField()
    email_contact = DefaultTextField()

    deauthorize_callback_url = DefaultTextField()

    organization_name = DefaultTextField()
    organization_website = DefaultTextField()

    users = m.ManyToManyField(User, through='Token', related_name='apps')

    class Meta:
        app_label = 'facebook'

    def __unicode__(self):
        return 'facebook_app(%s)' % self.pk
'''


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
    Provider = Provider

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

    def get_token(self, user):
        return User.token


class Token(oauth2.AbstractToken):
    user = m.OneToOneField(User, null=True)
    expires = m.IntegerField()
    activated = m.BooleanField(default=False)

    class Meta:
        app_label = 'facebook'


User.AVATAR_URL = property(lambda self: self.picture or
        'https://graph.facebook.com/%s/picture' % self.pk)
