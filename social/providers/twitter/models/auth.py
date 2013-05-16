from django.db import models as m

import auths.contrib.oauth as oauth
import sociallib.twitter as twitter

from utils.fields import DefaultTextField

from .objects import User

class Provider(twitter.Provider, oauth.Provider):
    pass

'''
class App(oauth.App, twitter.App):
    #XXX Are we cool with this?
    ACCESS_TYPES = (
        ('r', "Read only"),
        ('rw', "Read and Write"),
        ('rwa', "Read, Write and Access direct messages"),
    )

    name = 'Twitter'

    secure = True

    description = DefaultTextField()
    website = DefaultTextField()

    icon = DefaultTextField()

    access = m.TextField(choices=ACCESS_TYPES)
    callback_url = DefaultTextField()

    organization_name = DefaultTextField()
    organization_website = DefaultTextField()

    users = m.ManyToManyField(User, through='Token', related_name='apps')

    class Meta:
        app_label = 'twitter'

    def __str__(self):
        return 'twitter_app({})'.format(self.pk)
'''


class Consumer(twitter.Consumer):
    Provider = Provider

    def get_user(self, oauth_token, oauth_token_secret, user_id, screen_name):
        from .. import tasks
        user, created = User.objects.get_or_create(pk=user_id)
        user.screen_name = screen_name
        user.save()
        Token.objects.filter(user=user).exclude(key=oauth_token).delete()
        token = Token(user=user, key=oauth_token, secret=oauth_token_secret)
        token.save()
        tasks.import_user.delay(user.pk, token.pk)
        return user

    def get_token(self, user):
        return user.token


class Token(oauth.AbstractToken):
    user = m.OneToOneField(User, null=True)

    @property
    def userstream(self):
        from .. import streams
        return twitter.UserStream(self.auth, listener=streams.Listener())

    @property
    def statusstream(self):
        from .. import streams
        return twitter.StatusStream(self.auth,
                listener=streams.StatusStreamListener())

    class Meta:
        app_label = 'twitter'


User.AVATAR_URL = property(lambda self:
    'http://api.twitter.com/1/users/profile_image/{}?size=bigger'.format(self.pk))
