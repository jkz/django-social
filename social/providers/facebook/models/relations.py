from django.db import models as m
from .objects import Object, User

class Like(m.Model):
    user = m.ForeignKey(User, related_name='likes')
    object = m.ForeignKey(Object, related_name='likes')

    def __str__(self):
        return '{} likes {}'.format(self.user, self.object)
