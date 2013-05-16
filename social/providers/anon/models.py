"""
A lightweight pluggable authentication module
"""
import django.db.models as m

class User(m.Model):
    #XXX: Make this configurable
    AVATAR_URL = 'http://placekitten.com/200/'

    def __str__(self):
        return 'Anonymous User {}'.format(self.pk)


class Consumer(object):
    def get_user(self, session_key):
        token, created = self.tokens.get_or_create(key=session_key)
        if created:
            user = User.objects.create()
            token.user = user
            token.save()
        return token.user

    def get_token(self, uid):
        return Token.objects


class Provider(object):
    def auth_request(self, request, callback_url):
        return callback_url

    def auth_callback(self, request):
        return {'session_key': request.session.session_key}


class Token(m.Model):
    session_key = m.TextField(primary_key=True)
    user = m.OneToOneField(User, null=True)
    #consumer = m.ForeignKey(Consumer, related_name='tokens')

    def __str__(self):
        return 'Token of {}'.format(self.user)

