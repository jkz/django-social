from django.db import models as m

import auths.contrib.oauth as oauth
import sociallib.linkedin as linkedin

from utils.fields import DefaultTextField

from .objects import Profile

'''
class App(oauth.App, linkedin.App):
    name = 'Linkedin'

    company = DefaultTextField()
    application_name = DefaultTextField()
    description = DefaultTextField()
    website = DefaultTextField()
    icon = DefaultTextField()
    callback_url = DefaultTextField()

    users = m.ManyToManyField(Profile, through='Token', related_name='apps')

    class Meta:
        app_label = 'linkedin'

    def __unicode__(self):
        return 'linkedin_app(%s)' % self.pk

    def authenticate(self, oauth_token, oauth_token_secret):
        try:
            return self.tokens.get(key=oauth_token, secret=oauth_token_secret).user
        except Token.DoesNotExist:
            return None
'''
class Provider(linkedin.Provider, oauth.Provider):
    pass

class Consumer(linkedin.Consumer):
    Provider = Provider

    def get_token(self, user):
        return Token.objects.get(user=user)

    def get_user(self, oauth_token, oauth_token_secret, oauth_expires_in,
            oauth_authorization_expires_in):
        from .. import parsers
        token = Token(key=oauth_token, secret=oauth_token_secret)
        token.consumer = self
        data = token.api.get_profile()
        profile = parsers.import_profile(data)
        try:
            self.get_token(profile).delete()
        except Token.DoesNotExist:
            pass
        token.user = profile
        token.save()
        return profile

class Token(oauth.AbstractToken):
    user = m.OneToOneField(Profile, null=True)

    class Meta:
        app_label = 'linkedin'

Profile.AVATAR_URL = property(lambda self: self.pictureUrl)
