"""
Authentication functions which can be used as views.
"""

from django.contrib import auth
from django.conf import settings
from django.shortcuts import redirect

from django.utils.translation import ugettext as _

from . import exceptions
from . import backends

NEXT_SESSION_KEY = '_auth_next'

def _build_callback_url(request):
    """
    Return the configured callback path tacked to scheme and host
    discovered from request object.
    """
    return request.build_absolute_uri(settings.LOGIN_CALLBACK_URL)
    scheme = request.META.get('wsgi.url_scheme', 'http')
    #XXX this could be spoofed, perhaps use django.contrib.sites
    host = request.META.get('HTTP_HOST', request.META.get('SERVER_NAME'))
    return '{}://{}{}'.format(scheme, host, settings.LOGIN_CALLBACK_URL)


def connect(request, callback_url=None, **kwargs):
    """
    Return a redirect url which will initialize an authentication request
    """
    next = request.GET.get('next', None)
    if next is not None:
        request.session[NEXT_SESSION_KEY] = next
    if callback_url is None:
        callback_url = _build_callback_url(request)
    url = backends.protocol().request(request, callback_url, **kwargs)
    return redirect(url)


def callback(request):
    """
    Request authorization for a user on the request's client.
    """
    # Extract credentials from request
    creds = backends.protocol().callback(request)

    # Process extracted credentials
    user = auth.authenticate(**creds)

    if not user or not user.is_authenticated():
        raise exceptions.AuthFailure(_("Could not authenticate credentials!"))

    auth.login(request, user)

    return redirect(request.session.get(NEXT_SESSION_KEY,
        settings.LOGIN_REDIRECT_URL))


def disconnect(request, **kwargs):
    """
    Remove an authenticated user from the session or disconnect an account
    from it if provider is given.
    """

    backends.protocol().logout(request, **kwargs)

    # Redirect to 'next' GET parameter if given, else configured url
    return redirect(request.GET.get('next', settings.LOGIN_REDIRECT_URL))
