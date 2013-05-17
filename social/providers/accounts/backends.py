from django.contrib.auth.backends import ModelBackend
from django.utils.translation import ugettext as _

from . import models
from . import errors

class AccountBackend(ModelBackend):
    """
    Base class for Account authentication backend. This allows multiple
    account sources to authenticate to a single user.

    Arguments:
    :child - a user object from any source
    :parent - the session user object (either authenticated or anonymous)
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
