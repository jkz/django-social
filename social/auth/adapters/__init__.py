"""
This package is supposed to be a clusterfudge of gluecode to bind protocols,
providers and django.
"""

class Adapter:
    """
    The interface for an authentication consumer.
    """

    # This attribute should present a protocol object
    protocol = NotImplemented

    def __init__(self, **creds):
        if not creds:
            params = settings.PROVIDERS.get(provider, {})
            try:
                creds = params['creds']
            except (KeyError, TypeError):
                creds = {}
        self.init(**creds)

    def init(self, **creds):
        pass

    def authenticate(self, **creds):
        """
        Process given credentials and return the representing user object.
        """
        raise NotImplementedError

    def get_user(self, pk):
        """
        Get the user object of this adapter.
        """
        module = import_module(self.__module__)
        try:
            return module.User.objects.get(pk=pk)
        except module.User.DoesNotExist:
            return None


def get_adapter(provider=settings.AUTH_DEFAULT_PROVIDER, **creds):
    """
    Return an adapter object for given provider with credentials defined
    in settings.
    """
    module = import_module(params.get('app',
        '{}.adapters.{}'.format(__name__, provider)))
    return module.Adapter(**creds)

