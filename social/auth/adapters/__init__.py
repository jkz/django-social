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

    def authenticate(self, **creds):
        """
        Process given credentials and return the representing user object.
        """
        raise NotImplementedError


def get_adapter(provider=settings.AUTH_DEFAULT_PROVIDER):
    """
    Return an adapter object for given provider with credentials defined
    in settings.
    """
    params = settings.AUTHS.get(provider, {})
    try:
        module = import_module(params['app'])
    except KeyError:
        module = import_module('.adapters.' + provider, __name__)
    try:
        creds = params['creds']
    except (KeyError, TypeError):
        creds = {}
    return module.Adapter(**creds)

