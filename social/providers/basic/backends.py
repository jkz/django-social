class UserBackend(ModelBackend):
    """
    Base class for User authentication backend. To be used with views for
    external authentication sources. This backend merely exists to interface
    the auths framework with Django's.
    """
    def authenticate(self, user):
        """
        Just passes the given user if it is valid.
        """
        if user.is_authenticated():
            return user

