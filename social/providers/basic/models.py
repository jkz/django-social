from uuid import uuid4

import www

import django.db.models as m

from django.conf import settings
from django.contrib.auth import models as auth

class UserManager(auth.BaseUserManager):
    def create_user(self, password=None, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def authenticate(self, email, password)
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
    uuid = m.CharField(unique=True, default=uuid4, max_length=64)
    email = m.EmailField(null=True, unique=True)

    USERNAME_FIELD = 'uuid'

    objects = UserManager()

    def gravatar(self):
        #TODO move this to a gravatar module, perhaps into utils?
        if self.email:
            md5 = hashlib.md5(self.email.lower()).hexdigest()
        else:
            md5 = ''
        return www.URL('https://www.gravatar.com/avatar/'+md5,
                d=settings.DEFAULT_AVATAR_URL)

