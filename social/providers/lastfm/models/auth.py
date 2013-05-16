from django.db import models as m

from utils.fields import DefaultTextField

import sociallib.lastfm as lastfm

from .objects import User


'''
class App(m.Model, lastfm.App):
    api_key = m.TextField(primary_key=True)
    secret = DefaultTextField()

    description = DefaultTextField()
    website = DefaultTextField()
    icon = DefaultTextField()
    callback_url = DefaultTextField()

    users = m.ManyToManyField(User, through='Token', related_name='apps')

    name = 'Last.fm'

    class Meta:
        app_label = 'lastfm'
'''

class Provider(lastfm.API):
    def auth_request(self, request, redirect_uri):
        return super(Provider, self).auth_request(redirect_uri)

    def auth_callback(self, request):
        return super(Provider, self).auth_callback(request.GET.get('token'))


class Consumer(lastfm.Consumer):
    Provider = Provider

    def get_user(self, key):
        from .. import parsers
        token, created  = Token.objects.get_or_create(key=key)
        #if created or not token.user:
        token.consumer = self
        data = token.api.get_user()
        user = parsers.import_user(data['user'])
        #self.tokens.filter(user=user).delete()
        token.user = user
        token.save()
        return user

    def get_token(self, user):
        return user.token

class Token(m.Model, lastfm.TokenInterface):
    key = m.TextField(primary_key=True)
    user = m.ForeignKey(User, null=True, related_name='tokens')

    class Meta:
        app_label = 'lastfm'

