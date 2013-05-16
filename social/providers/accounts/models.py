import django.db.models as m

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.importlib import import_module

from .. import basic

class User(basic.User):
    class Meta:
        proxy = True

    def get_account(self, provider):
        return self.account_set.get(content_type__app_label=provider)

    def connected_providers(self):
        return self.account_set.values_list('content_type__app_label', flat=True)

    def unconnected_providers(self):
        return list(set(settings.AUTHS.keys()) -
                set(self.connected_providers()))


class AccountManager(m.Manager):
    def get_for_child(self, child):
        content_type = ContentType.objects.get_for_model(child)
        return self.get(content_type=content_type, object_id=child.pk)


class Account(m.Model):
    """Represents a third party account as part of a composite user"""

    parent = m.ForeignKey(User, default=User.objects.create_user)
    content_type = m.ForeignKey(ContentType)
    object_id = m.TextField()
    child = generic.GenericForeignKey('content_type', 'object_id')

    objects = AccountManager()

    class Meta:
        unique_together = [('content_type', 'object_id'), ('content_type', 'parent')]

    def provider(self):
        return self.content_type.app_label

    def __str__(self):
        return '{} as {}'.format(self.parent, self.child)


