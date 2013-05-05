"""
Provides the functions for 3rd party authentication.
"""
from .views import connect, callback, disconnect
from .models import User, Account

from django.conf import settings
from django.utils.translation import ugettext as _


if 'auths.backends.UserBackend' in settings.AUTHENTICATION_BACKENDS:
    settings.AUTH_MULTI = False
elif 'auths.backends.AccountBackend' in settings.AUTHENTICATION_BACKENDS:
    settings.AUTH_MULTI = True
    settings.AUTH_USER_MODEL = 'auths.User'
else:
    raise Exception(_("Backend missing in AUTHENTICATION_BACKENDS"))

