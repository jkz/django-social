from uuid import uuid4

import django.db.models as m

from django.conf import settings
from django.contrib.auth import models as auth
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class UserManager(auth.BaseUserManager):
    def create_user(self, password=None, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(auth.AbstractBaseUser):
    uuid = m.CharField(unique=True, default=uuid4, max_length=64)
    email = m.EmailField(null=True, unique=True)

    USERNAME_FIELD = 'uuid'

    objects = UserManager()

    def get_account(self, namespace):
        return self.account_set.get(content_type__app_label=namespace)


class AccountManager(m.Manager):
    def get_for_child(self, child):
        content_type = ContentType.objects.get_for_model(child)
        return self.get(content_type=content_type, object_id=child.pk)


class Account(m.Model):
    parent = m.ForeignKey(User, default=User.objects.create_user)
    content_type = m.ForeignKey(ContentType)
    object_id = m.PositiveIntegerField()
    child = generic.GenericForeignKey('content_type', 'object_id')

    objects = AccountManager()

    class Meta:
        unique_together = [('content_type', 'object_id'), ('content_type', 'parent')]

    def __str__(self):
        return '{} as {}'.format(self.parent, self.child)
