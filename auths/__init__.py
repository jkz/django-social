"""
Provides the functions for 3rd party authentication.
"""
from .views import connect, callback, disconnect
from .models import User, Account

from django.conf import settings
from django.utils.translation import ugettext as _


# Default settings
settings.AUTHS = getattr(settings, 'AUTHS', {})

# Derived settings
if 'auths.backends.UserBackend' in settings.AUTHENTICATION_BACKENDS:
    settings.AUTH_MULTI = False
elif 'auths.backends.AccountBackend' in settings.AUTHENTICATION_BACKENDS:
    settings.AUTH_MULTI = True
    settings.AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auths.User')
else:
    raise Exception(_("Backend missing in AUTHENTICATION_BACKENDS"))


class Authority:
    """
    The interface for an authentication providing service.
    """
    def auth_request(self, request, callback_url):
        """
        Return an url to redirect an authenticates a user to,
        and redirect back to given callback_url afterwards.
        """
        raise NotImplementedError

    def auth_callback(self, request):
        """
        Return an authenticated user object for credentials provided
        in the request or None
        """
        raise NotImplementedError


class Consumer:
    """
    The interface for an authentication consumer.
    """
    def get_user(self, **creds):
        """
        Process given credentials and return the representing user object.
        """
        raise NotImplementedError

    def get_token(self, uid):
        """
        Get an authorization token for given user.
        """
        raise NotImplementedError

def get_consumer(provider=None):
    params = settings.AUTHS.get(provider or 'default')
    name = params.get('app', provider)
    module = import_module(name)
    creds = params.get('creds', {})
    return module.models.Consumer(**creds)

