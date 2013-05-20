from django.db import models as m

from www.social import linkedin

from ...providers.linkedin import parsers, User
from ..protocols import oauth
from . import Backend

class User(Profile):
    class Meta:
        proxy = True

    @property
    def AVATAR_URL(self):
        return self.pictureUrl


class Backend(Backend):
    def init(self, **creds):
        self.consumer = linkedin.Consumer(**creds)
        authority = self.consumer.authority()
        self.protocol = oauth.protocol(authority=authority)

    def authenticate(self, oauth_token, oauth_token_secret, oauth_expires_in,
            oauth_authorization_expires_in):
        from .. import parsers
        token = Token(key=oauth_token, secret=oauth_token_secret)
        api = self.consumer.api(token=token)

        data = api.get_profile()
        profile = parsers.import_profile(data)
        #XXX this probably wont work, as the relationship is to the groxy, not
        # the concrete model
        if profile.token:
            profile.token.delete()

        token.user = profile
        token.save()
        return token.user


class Token(oauth.AbstractToken):
    user = m.OneToOneField(User, null=True)

    class Meta:
        app_label = 'linkedin'

