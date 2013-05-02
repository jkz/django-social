"""
Provides the functions for 3rd party authentication.
"""

from django.contrib import auth
from django.conf import settings
from django.shortcuts import redirect

from django.utils.translation import ugettext as _

from . import errors

#XXX Callback url should be configurable
def build_callback_url(request):
    """
    Return the request uri with 'callback/' tacked to the end. Ensure
    a trailing slash to the request uri.
    """
    scheme = request.META.get('wsgi.url_scheme', 'http')
    host = request.META.get('HTTP_HOST', settings.DOMAIN)
    path = request.path
    if not path.endswith('/'):
        path += '/'
    return '{}://{}{}callback/'.format(scheme, host, path)


def connect(request, callback_url=None):
    """
    Return a redirect url which will initialize an authentication request
    """
    if callback_url is None:
        callback_url = build_callback_url(request)
    redirect_url = request.provider.auth_request(request, callback_url)
    return redirect(redirect_url)


def callback(request):
    """
    Request authorization for a user on the request's client.
    """

    # Connection requires an unauthenticated session for the active client
    if request.user.is_authenticated():
        raise errors.AuthConflict(
                _("Authenticated user already present on this session"))

    # Extract credentials from request
    creds = request.provider.auth_callback(request)

    # Process the extracted credentials
    user = request.consumer.auth_process(**creds)

    if not user:
        raise errors.AuthFailure(_("Could not authenticate credentials!"))

    _user = auth.authenticate(user=user)
    auth.login(request, _user)


def disconnect(request):
    """
    Remove an authenticated user from the session.
    """
    if not request.user.is_authenticated():
        raise Unauthorized(_("You need to be logged in to do that!"))
    auth.logout(request)

