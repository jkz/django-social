"""
Authapp provides an interface for authentication modules.
"""

class Interface:
    """
    The interface of an auth app.
    """
    def auth_request(self, request, callback_url):
        """
        Return an url to redirect an authenticates a user to,
        and redirect back to given callback_url afterwards.
        """
        raise NotImplementedError

    def auth_callback(self, request):
        """
        Return an authenticated user object for credentials provided
        in the request or None
        """
        raise NotImplementedError

    def auth_process(self, **creds):
        """
        Return credentials provided by an authenticating user.
        Called by auth_callback with paramaters returned after redirecting
        a user for authentication. This method could store the credentials in a
        backend.
        """
        return creds
