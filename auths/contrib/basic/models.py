from django.db import models as m
from django.utils.translation import ugettext as _
import django.contrib.auth.models as auth

from authlib import basic

from auths import errors

class Provider(basic.Provider):
    def auth_request(self, request, callback_url):
        return self.get_redirect_url(callback_url=callback_url)

    def auth_callback(self, request):
        #XXX: This should be POST
        if not 'username' in request.GET:
            raise errors.Error(_("No username provided in post!"))
        if not 'password' in request.GET:
            raise errors.Error(_("No password provided in post!"))
        #XXX: We could want to be explicit here
        return request.GET


class Consumer(basic.Consumer):
    provider = Provider()

    def get_user(self, username, password=None):
        try:
            user = self.Token.objects.get_by_natural_key(username)
        except self.Token.DoesNotExist:
            return self.Token.objects.create_user(username, password=password)
        else:
            if user.check_password(password):
                return user

    def get_token(self, user):
        return user


class TokenManager(auth.BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username)
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

Consumer.Token = Token
