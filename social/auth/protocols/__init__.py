"""
This package contains authentications protocols.
"""

class Protocol:
    """
    The interface for an authority that provides authentication hooks.
    """
    def request(self, request, callback_url):
        """
        Return a url which will initiate the authentication flow. Afterwards,
        the user should be redirected to the callback_url.
        """
        raise NotImplementedError

    def callback(self, request):
        """
        Complete an authentication flow and return the resulting credentials.
        """
        raise NotImplementedError

