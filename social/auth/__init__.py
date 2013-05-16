"""
Provides the functions for 3rd party authentication.
"""
from .views import connect, callback, disconnect

from django.conf import settings
from django.utils.translation import ugettext as _


# Default settings

settings.AUTHS = getattr(settings, 'AUTHS', {})

if not hasattr(settings, 'AUTH_DEFAULT_PROVIDER'):
    # Use first key in AUTHS as default provider
    #
    # Heads up! This is undeterministic behaviour with multiple keys
    try:
        settings.AUTH_DEFAULT_PROVIDER = AUTHS.keys()[0]
    except IndexError:
        raise Exception(_("No auth provider specified"))


settings.LOGIN_URL = getattr(settings, 'LOGIN_URL', '/connect/')
settings.LOGOUT_URL = getattr(settings, 'LOGOUT_URL', '/disconnect/')
settings.LOGIN_CALLBACK_URL = getattr(settings, 'LOGIN_CALLBACK_URL', '/connected/')
settings.LOGIN_REDIRECT_URL = getattr(settings, 'LOGIN_REDIRECT_URL', '/')


if not hasattr(settings, 'DEFAULT_AVATAR_URL'):
    settings.DEFAULT_AVATAR_URL = 'http://placehold.it/200/'


# Derived settings
if 'auths.backends.UserBackend' in settings.AUTHENTICATION_BACKENDS:
    settings.USE_AUTH_USER = settings.AUTH_DEFAULT_PROVIDER == 'basic'
    settings.USE_AUTH_ACCOUNT = False
    #TODO set AUTH_USER_MODEL
elif 'auths.backends.AccountBackend' in settings.AUTHENTICATION_BACKENDS:
    settings.USE_AUTH_USER = True
    settings.USE_AUTH_ACCOUNT = True
    settings.AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auths.User')
else:
    raise Exception(_("Backend missing in AUTHENTICATION_BACKENDS"))

