from django.db import models as m

import auths.contrib.oauth as oauth
import sociallib.tumblr as tumblr

from utils.fields import DefaultTextField

from .objects import User

'''
class App(oauth.App, tumblr.App):
    name = 'Tumblr'

    oauth_host = 'www.tumblr.com'
    request_token_path = '/oauth/request_token'
    access_token_path = '/oauth/access_token'

    authorize_uri = 'http://tumblr.com/oauth/authorize'


    description = DefaultTextField()
    website = DefaultTextField()
    icon = DefaultTextField()
    callback_url = DefaultTextField()

    users = m.ManyToManyField(User, through='Token', related_name='apps')

    class Meta:
        app_label = 'tumblr'

    def __unicode__(self):
        return 'tumblr_app(%s)' % self.pk

    def authenticate(self, oauth_token, oauth_token_secret):
        try:
            return self.tokens.get(key=oauth_token, secret=oauth_token_secret).user
        except KeyError:
            # Invalid credential params
            return None
        except Token.DoesNotExist:
            return None
'''

class Provider(tumblr.Provider, oauth.Provider):
    pass

class Consumer(tumblr.Consumer):
    Provider = Provider

    def get_token(self, user):
        return Token.objects.get(user=user)

    def get_user(self, oauth_token, oauth_token_secret):
        from .. import parsers
        token = Token.objects.create(key=oauth_token, secret=oauth_token_secret)
        token.consumer = self
        data = token.api.get_user()
        user = parsers.import_user(data['response']['user'])
        try:
            self.get_token(user).delete()
        except Token.DoesNotExist:
            pass
        token.user = user
        token.save()
        return user

class Token(oauth.AbstractToken):
    user = m.OneToOneField(User, null=True)

    class Meta:
        app_label = 'tumblr'

User.AVATAR_URL = property(User.avatar)
