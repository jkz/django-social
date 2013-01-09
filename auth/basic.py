from django.db import models as m
from django.shortcuts import redirect

#XXX Some parent models from this class would be nice
#from authlib import basic

from utils.decorators import require_get

class Token(object):
    #TODO: plain text passwords? ha. ha.
    #      Using django.contrib.auth.User for now, which is probably the best.
    username = m.TextField()
    password = m.TextField()

    class Meta:
        abstract = True

class App(object):
    def auth_request(self, request, callback_url):
        return redirect(self.service.get_redirect_url(callback_url=callback_url))

    @property
    def auth_callback(self):
        #TODO: this should be post
        @require_get('email', "No username provided in post!")
        @require_get('password', "No password provided in post!")
        def func(request, **creds):
            return creds
        return func

