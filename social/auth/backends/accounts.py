from django.conf import settings
from django.contrib import auth

from ..providers.accounts import models
from .. import errors
from .. import protocols
from .. import backends

PROVIDER_SESSION_KEY = '_auth_provider'

class Protocol(protocols.Protocol):
    def request(self, request, callback_url,
            provider=settings.AUTH_DEFAULT_PROVIDER, **kwargs):
        request.session[PROVIDER_SESSION_KEY] = provider
        return backends.backend(provider).request(request, callback_url, **kwargs)

    def callback(self, request):
        provider = request.session.pop(PROVIDER_SESSION_KEY, False)
        if not provider:
            raise errors.Error(_("No authentication provider in session"))

        backend = backends.backend(provider)

        # Extract credentials from request
        creds = backend.protocol.callback(request)

        # Process extracted credentials
        user = backend.authenticate(**creds)

        if not user:
            raise errors.AuthFailure(_("Could not authenticate credentials!"))

        return {'child': user, 'parent': request.user}

    def logout(self, request, provider=None):
        if request.user.is_authenticated():
            if provider:
                request.user.get_account(provider).delete()
            else:
                auth.logout(request)


class Backend(Backend):
    """
    Base class for Account authentication backend. This allows multiple
    account sources to authenticate to a single user.

    Arguments:
    :child - a user object from any source
    :parent - the session user object (either authenticated or anonymous)
    """
    def authenticate(self, child, parent):
        """Return the user's parent and else a new one"""
        try:
            account = models.Account.objects.get_for_child(child)
        except models.Account.DoesNotExist:
            params = {'child': child}
            if parent.is_authenticated():
                params['parent'] = parent
            account = models.Account.objects.create(**params)
        else:
            if parent and parent.is_authenticated() and parent != account.parent:
                raise errors.AuthConflict(
                        _("Account already bound to another User"))
        return account.parent
