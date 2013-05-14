from uuid import uuid4

import django.db.models as m

from django.conf import settings
from django.contrib.auth import models as auth
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.importlib import import_module

if settings.AUTH_MULTI:
    class UserManager(auth.BaseUserManager):
        def create_user(self, password=None, **extra_fields):
            user = self.model(**extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

    class User(auth.AbstractBaseUser):
        """
        A user object to which third party accounts can be bound.
        """
        uuid = m.CharField(unique=True, default=uuid4, max_length=64)
        email = m.EmailField(null=True, unique=True)

        USERNAME_FIELD = 'uuid'

        objects = UserManager()

        def get_account(self, namespace):
            return self.account_set.get(content_type__app_label=namespace)

        def connected_namespaces(self):
            return self.account_set.values_list('content_type__app_label', flat=True)

        def unconnected_namespaces(self):
            return list(set(settings.AUTHS.keys()) - set(self.connected_namespaces()))


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

        def namespace(self):
            return self.content_type.app_label

        def __str__(self):
            return '{} as {}'.format(self.parent, self.child)

# Add all token models from user providers to this models file. The models
# have their provider's name camelcased.
def camelcase(s):
    return ''.join(map(str.capitalize, s.split('_')))

for provider in settings.AUTHS:
    module = import_module('auths.providers.' + provider)
    model = module.Token
    model._meta.app_label = 'auths'
    model.__name__ = camelcase(provider)
    globals()[model.__name__] = model
