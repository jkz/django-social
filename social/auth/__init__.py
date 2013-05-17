"""
Provides the means for 3rd party authentication.
"""
from .views import connect, callback, disconnect

from django.conf import settings as s
from django.utils.translation import ugettext as _

# Default settings
s.LOGIN_URL = getattr(s, 'LOGIN_URL', '/connect/')
s.LOGOUT_URL = getattr(s, 'LOGOUT_URL', '/disconnect/')
s.LOGIN_CALLBACK_URL = getattr(s, 'LOGIN_CALLBACK_URL', '/callback/')
s.LOGIN_REDIRECT_URL = getattr(s, 'LOGIN_REDIRECT_URL', '/')
s.DEFAULT_AVATAR_URL = getattr(s, 'DEFAULT_AVATAR_URL', 'http://placehold.it/200/')
s.USE_ACCOUNTS = getattr(s, 'USE_ACCOUNTS', False)
s.AUTH_USER_MODEL = getattr(s, 'AUTH_USER_MODEL', 'auths.User')
