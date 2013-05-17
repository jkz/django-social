from django.db import models as m

from www.social import twitter

from ...providers.twitter import User
from ..protocols import oauth
from . import Adapter

class User(User):
    class Meta:
        proxy = True

    @property
    def AVATAR_URL(self):
        return 'http://api.twitter.com/1/users/profile_image/{}?size=bigger'.format(self.pk)


class Adapter(Adapter):
    def __init__(self, **creds):
        self.consumer = twitter.Consumer(**creds)
        authority = self.consumer.authority()
        self.protocol = oauth.protocol(authority=authority)

    def authenticate(self, oauth_token, oauth_token_secret, user_id, screen_name):
        from .. import tasks
        user, created = User.objects.get_or_create(pk=user_id)
        user.screen_name = screen_name
        user.save()

        if user.token:
            user.token.delete()

        token = Token(user=user, key=oauth_token, secret=oauth_token_secret)
        token.save()

        tasks.import_user.delay(user.pk, token.pk)
        return user


class Token(oauth.AbstractToken):
    user = m.OneToOneField(User, null=True)

    class Meta:
        app_label = 'twitter'

    #TODO fix streams
    @property
    def userstream(self):
        from .. import streams
        return twitter.UserStream(self.auth, listener=streams.Listener())

    @property
    def statusstream(self):
        from .. import streams
        return twitter.StatusStream(self.auth,
                listener=streams.StatusStreamListener())

