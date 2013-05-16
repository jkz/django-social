"""
Authentication functions which can be used as views.
"""

from django.contrib import auth
from django.conf import settings
from django.shortcuts import redirect

from django.utils.translation import ugettext as _
from django.utils.importlib import import_module

from . import errors
from . import models
from . import adapters

PROVIDER_SESSION_KEY = '_auth_provider'
NEXT_SESSION_KEY = '_auth_next'


def _build_callback_url(request):
    """
    Return the configured callback path tacked to scheme and host
    discovered from request object.
    """
    scheme = request.META.get('wsgi.url_scheme', 'http')
    #XXX this could be spoofed, perhaps use django.contrib.sites
    host = request.META.get('HTTP_HOST')
    return '{}://{}{}'.format(scheme, host, settings.LOGIN_CALLBACK_URL)


def connect(request, callback_url=None, provider=settings.AUTH_DEFAULT_PROVIDER):
    """
    Return a redirect url which will initialize an authentication request
    """
    request.session[PROVIDER_SESSION_KEY] = provider
    next = request.GET.get('next', None)
    if next is not None:
        request.session[NEXT_SESSION_KEY]
    if callback_url is None:
        callback_url = _build_callback_url(request)
    adapter = adapters.get_adapter(provider)
    redirect_url = adapter.protocol.request(request, callback_url)
    return redirect(redirect_url)


def callback(request):
    """
    Request authorization for a user on the request's client.
    """
    # Connection requires an unauthenticated session for active client
    #TODO determine what should happen here, coded out for now
    if False and request.user.is_authenticated():
        raise errors.AuthConflict(
                _("Authenticated user already present on this session"))

    provider = request.session.pop(PROVIDER_SESSION_KEY, False)
    if not provider:
        raise errors.Error(_("No authentication provider in session"))

    adapter = adapters.get_adapter(provider)

    # Extract credentials from request
    creds = adapter.protocol.callback(request)

    # Process extracted credentials
    user = adapter.authenticate(**creds)

    if not user:
        raise errors.AuthFailure(_("Could not authenticate credentials!"))

    # Invoke configured authentication backend
    if settings.USE_ACCOUNTS:
        _user = auth.authenticate(child=user, parent=request.user)
    else:
        _user = auth.authenticate(user=user)


    auth.login(request, _user)

    return redirect(request.session.get(NEXT_SESSION_KEY,
            settings.LOGIN_REDIRECT_URL))


def disconnect(request, provider=None):
    """
    Remove an authenticated user from the session or disconnect an
    account from it if provider is given.
    """
    #XXX We might want this to fail silently
    if False and not request.user.is_authenticated():
        raise errors.Unauthorized(_("You need to be logged in to do that!"))

    # Remove account of given provider from authenticated user
    if settings.USE_ACCOUNTS and provider:
        try:
            request.user.get_account(provider).delete()
        except models.Account.DoesNotExist:
            pass

    # Remove authenticated user from session
    else:
        auth.logout(request)

    # Redirect to 'next' GET parameter if given, else configured url
    return redirect(request.GET.get('next', settings.LOGIN_REDIRECT_URL))
