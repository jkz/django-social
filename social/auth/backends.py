from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.utils.translation import ugettext as _

from . import models
from . import errors
from . import adapters

class UserBackend(ModelBackend):
    """
    This backend takes user objects through Django's authentication
    internals. The actual authentication should be done prior to invoking it.
    """
    def authenticate(self, user):
        """
        Just passes the given user if it is valid.
        """
        if user.is_authenticated():
            return user

# Add an authentication
for provider in settings.PROVIDERS:
    globals()[provider] = adapters.get_adapter(provider)
