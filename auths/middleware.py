"""
Provides the middelware necessary to use auths.
"""
from django.conf import settings
from django.utils.importlib import import_module

from . import consumer

NAMESPACE_SESSION_KEY = '_auth_namespace'

#XXX: Lazy objects would be nice
class AuthMiddleware:
    """
    Adds a `consumer` and `provider` to the request object.
    These can be used to authenticate with 3rd parties.
    """
    def process_request(self, request):
        namespace = request.session.pop(NAMESPACE_SESSION_KEY, None)
        request.consumer = consumer(namespace)
        request.provider = request.consumer.provider

        if not request.user.is_authenticated():
            return

        request.token = request.consumer.get_token(request.user)

