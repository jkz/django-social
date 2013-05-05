"""
Provides the functions for 3rd party authentication.
"""
from .views import connect, callback, disconnect

from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils.importlib import import_module


if not 'auths.middleware.AuthMiddleware' in settings.MIDDLEWARE_CLASSES:
    raise Exception(_("AuthMiddleware missing in MIDDLEWARE_CLASSES"))

if not 'auths.backends.UserBackend' in settings.AUTHENTICATION_BACKENDS:
    raise Exception(_("UserBackend missing in AUTHENTICATION_BACKENDS"))

def get_consumer(namespace=None):
    params = settings.AUTHS.get(namespace or 'default')
    name = params.get('app', namespace)
    module = import_module(name)
    creds = params.get('creds', {})
    return module.models.Consumer(**creds)

