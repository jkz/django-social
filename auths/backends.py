from django.contrib.auth.backends import ModelBackend
from django.utils.translation import ugettext as _

from . import models
from . import errors

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
        if user.is_authenticated():
            return user


class AccountBackend(ModelBackend):
    """
    Base class for Account authentication backend. This allows multiple
    account sources to authenticate to a single user.
    """
    def authenticate(self, child, parent):
        """Return the user's parent and else a new one"""
        try:
            account = models.Account.objects.get_for_child(child)
        except models.Account.DoesNotExist:
            params = {'child': child}
            if parent.is_authenticated():
                params['parent'] = parent
            account = models.Account.objects.create(**params)
        else:
            if parent.is_authenticated() and parent != account.parent:
                raise errors.AuthConflict(
                        _("Account already bound to another User"))
        return account.parent
