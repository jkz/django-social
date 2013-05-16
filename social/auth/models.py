from uuid import uuid4

import django.db.models as m

from django.conf import settings
from django.contrib.auth import models as auth
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.importlib import import_module

if settings.USE_AUTH_USER:
    class UserManager(auth.BaseUserManager):
        def create_user(self, password=None, **extra_fields):
            user = self.model(**extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

        def authenticate(self, email, password=None)
            if email:
                try:
                    user = self.model.objects.get(email=email)
                except self.model.DoesNotExist:
                    pass
                else:
                    if user.check_password(password):
                        return user
            return None

    class User(auth.AbstractBaseUser):
        """
        A user object to which third party accounts can be bound.
        """
        uuid = m.CharField(unique=True, default=uuid4, max_length=64)
        email = m.EmailField(null=True, unique=True)

        USERNAME_FIELD = 'uuid'

        objects = UserManager()

        def AVATAR_URL(self):
            #TODO move this to a gravatar module, perhaps into utils?
            if self.email:
                md5 = hashlib.md5(self.email.lower()).hexdigest()
            else:
                md5 = ''
            return www.URL('https://www.gravatar.com/avatar/'+md5,
                    d=settings.DEFAULT_AVATAR_URL)

        if settings.USE_AUTH_ACCOUNT:
            def get_account(self, provider):
                return self.account_set.get(content_type__app_label=provider)

            def connected_providers(self):
                return self.account_set.values_list('content_type__app_label', flat=True)

            def unconnected_providers(self):
                return list(set(settings.AUTHS.keys()) -
                        set(self.connected_providers()))

if settings.USE_AUTH_ACCOUNT:
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


# Add all token models from user providers to this models file. The models
# have their provider's name camelcased.
def camelcase(s):
    return ''.join(map(str.capitalize, s.split('_')))

for provider in settings.AUTHS:
    #TODO this probably does not work right yet
    module = import_module('.adapters.' + provider, __name__.rpartition('.')[0])
    model = module.Token
    model._meta.app_label = 'auth'
    model.__name__ = camelcase(provider)
    globals()[model.__name__] = model
