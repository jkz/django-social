import auths.contrib.oauth2 as oauth2
import sociallib.soundcloud as soundcloud

from django.db import models as m

from utils.fields import DefaultTextField

from .objects import User

'''
class App(oauth2.App, soundcloud.App):
    name = 'Soundcloud'

    description = DefaultTextField()
    website = DefaultTextField()

    icon = DefaultTextField()

    users = m.ManyToManyField(User, through='Token', related_name='apps')

    class Meta:
        app_label = 'soundcloud'

    def __unicode__(self):
        return 'soundcloud_app(%s)' % self.pk
'''

class Provider(soundcloud.Provider, oauth2.Provider):
    def auth_request(self, *args, **kwargs):
        return super(Provider, self).auth_request(*args,
                display='popup', response_type='code', scope='non-expiring',
                **kwargs)

    def auth_callback(self, request):
        try:
            code = request.GET['code']
        except KeyError:
            raise soundcloud.Error("Code missing in request")

        callback_url = request.build_absolute_uri(request.path)

        creds = self.exchange_code(code, callback_url,
                grant_type='authorization_code')

        if 'error' in creds:
            #TODO proper error class
            raise Exception(creds['error'])
        return creds

class Consumer(soundcloud.Consumer):
    Provider = Provider

    def get_token(self, user):
        return Token.objects.get(user=user)

    def get_user(self, access_token, scope):
        token = Token.objects.create(key=access_token, scope=scope)
        token.consumer = self
        token.activated = True
        data = token.api.me()
        user = User.importer.put(**data)
        try:
            self.get_token(user).delete()
        except Token.DoesNotExist:
            pass
        token.user = user
        token.save()
        return user


class Token(oauth2.AbstractToken):
    scope = m.TextField()
    user = m.OneToOneField(User, null=True)

    activated = m.BooleanField(default=False)

    class Meta:
        app_label = 'soundcloud'

User.AVATAR_URL = property(lambda self: self.avatar_url)
