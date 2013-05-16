"""
This package contains authentications protocols.
"""

class Protocol:
    """
    The interface for an authority that provides authentication hooks.
    """
    def request(self, request, callback_url):
        """
        Return an url to redirect an authenticates a user to,
        and redirect back to given callback_url afterwards.
        """
        raise NotImplementedError

    def callback(self, request):
        """
        Return credentials dict (to pass to consumer.get_user) for
        authenticating user or None.
        """
        raise NotImplementedError

