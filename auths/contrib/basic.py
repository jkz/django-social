from django.db import models as m
from django.utils.translation import ugettext as _
from django.contrib.auth.models import AbstractBaseUser

from authlib import basic

from . import errors

class Provider(basic.Provider):
    def auth_request(self, request, callback_url):
        return self.get_redirect_url(callback_url=callback_url)

    def auth_callback(self, request):
        #XXX: This might have to be GET
        if not 'username' in request.POST:
            raise errors.Error(_("No username provided in post!"))
        if not 'password' in request.POST:
            raise errors.Error(_("No password provided in post!"))
        #XXX: We could want to be explicit here
        return request.POST


class Consumer(basic.Consumer):
    provider = Provider()

    def get_user(self, username, password=None):
        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            return User.objects.create_user(username, password=password)
        else:
            if user.check_password(password):
                return user

    def get_token(self, user):
        return user


class TokenModel(AbstractBaseUser, basic.TokenInterface):
    consumer = None

    username = m.TextField(primary_key=True)

    USERNAME_FIELD = 'username'

    class Meta:
        abstract = True


class User(TokenModel):
    consumer = Consumer()

