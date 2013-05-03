"""
Provides the middelware necessary to use auths.
"""
from django.conf import settings
from django.utils.importlib import import_module

#XXX: Lazy objects would be nice
class AuthMiddleware:
    """
    Adds a `consumer` and `provider` to the request object.
    These can be used to authenticate with 3rd parties.

    Use multiple authentication providers by
    """
    def process_request(self, request):
        """
        Requires a configuration

        AUTHS = {
            'default': {
                'consumer': 'Consumer', # optional, defaults to 'Consumer'
                'app': 'app_label',     # optional, if request.namespace
                'creds': {
                    ...
                }
            }
        }
        """
        conf = settings.AUTHS.get(getattr(request, 'namespace', 'default'))

        namespace = conf.get('app', getattr(request, 'namespace', None))

        module = import_module(namespace)

        Consumer = getattr(module, conf.get('consumer', 'Consumer'))

        creds = conf.get('creds', {})

        request.consumer = Consumer(**creds)
        request.provider = request.consumer.provider

        if not request.user.is_authenticated():
            return

        request.token = request.consumer.get_token(request.user)

