from django.contrib.auth.backends import ModelBackend

class UserBackend(ModelBackend):
    """
    Base class for User authentication backend. To be used with views for
    external authentication sources. This backend merely exists to interface
    the auths framework with Django's.
    """
    def authenticate(self, user):
        """
        Just passes the given user. This backend exists as a complement to the
        AccountBackend.
        """
        if user and user.is_authenticated():
            return user

