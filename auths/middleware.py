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

        AUTH_CONF = {
            'consumer': 'ConsumerClass', # optional, defaults to 'Consumer'
            'provider': 'ProviderClass', # optional, defaults to 'Provider'
            'app': 'app_label',          # optional, if request.namespace
            'creds': {
                ...
            }
        }
        """
        conf = settings.AUTH_CONF.get(getattr(request, 'namespace', 'default'))

        module = import_module(conf.get('app', request.namespace))

        Consumer = getattr(module, conf.get('consumer', 'Consumer'))
        Provider = getattr(module, conf.get('provider', 'Provider'))

        request.consumer = Consumer(**conf.creds)
        request.provider = Provider(request.consumer)

'''
class TokenMiddleware:
        if not user.is_authenticated():
            return

        request.token = request.consumer.get_token(request.user)
'''

