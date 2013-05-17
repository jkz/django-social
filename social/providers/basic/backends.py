from django.contrib.auth.backends import ModelBackend

class UserBackend(ModelBackend):
    """
    This backend allows non-Django-native authentication flows to tie into the
    contrib.auth framework.
    """
    def authenticate(self, user):
        """
        Just passes the given user if it is valid.
        """
        if user.is_authenticated():
            return user

