import django.db.models as m

from django.utils import CustomUser

class User(CustomUser):
    session_key = m.TextField(primary_key=True)

    USERNAME_FIELD = 'session_key'

    def __str__(self):
        return 'Anonymous User {}'.format(self.pk)

