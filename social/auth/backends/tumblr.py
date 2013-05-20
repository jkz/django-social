from django.db import models as m

from www.social import tumblr

from ...providers.tumblr import parsers, models
from ..protocols import oauth
from . import Backend

class User(models.User):
    class Meta:
        proxy = True

    @property
    def AVATAR_URL(self):
        return self.avatar


class Backend(Backend):
    def init(self, **creds):
        self.consumer = tumblr.Consumer(**creds)
        authority = self.consumer.authority()
        self.protocol = oauth.protocol(authority=authority)

    def authenticate(self, oauth_token, oauth_token_secret):
        from .. import parsers
        token = Token(key=oauth_token, secret=oauth_token_secret)
        api = self.consumer.api(token=token)

        data = api.get_user()
        user = parsers.import_user(data['response']['user'])

        if user.token:
            user.token.delete()

        token.user = user
        token.save()
        return user

class Token(oauth.AbstractToken):
    user = m.OneToOneField(User, null=True)

    class Meta:
        app_label = 'tumblr'

