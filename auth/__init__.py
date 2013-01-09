"""
Authapp provides an interface for authentication modules.
"""

class Interface:
    """
    The interface of an auth app.
    """
    def auth_request(self, request, callback_url):
        """
        Return an HttpResponse object which authenticates a user
        and redirects back to given callback_url.
        """
        raise NotImplementedError

    def auth_callback(self, request):
        """
        Return an authenticated user object for credentials provided
        in the request or None
        """
        raise NotImplementedError
