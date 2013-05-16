from django.db import models as m
from django.utils.translation import ugettext as _
import django.contrib.auth.models as auth

import www.auth
from www.auth import basic

from auths import errors

from . import Protocol

class Protocol(Protocol):
    def request(self, request, callback_url):
        return self.get_redirect_url(callback_url=callback_url)

    def callback(self, request):
        if not 'username' in request.REQUEST:
            raise errors.Error(_("No username provided in request!"))
        if not 'password' in request.REQUEST:
            raise errors.Error(_("No password provided in request!"))
        return {'username': request.REQUEST['username'],
                'password': request.REQUEST['password']}


class TokenManager(auth.BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class AbstractToken(auth.AbstractBaseUser, basic.TokenInterface):
    consumer = None

    username = m.TextField(primary_key=True)

    USERNAME_FIELD = 'username'

    objects = TokenManager()

    class Meta:
        abstract = True


class Token(auth.AbstractUser):
    consumer = Consumer()
