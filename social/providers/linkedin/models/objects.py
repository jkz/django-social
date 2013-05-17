from django.db import models as m

from utils.models import ImportModel, CustomUser
from utils.fields import DefaultTextField


class Profile(ImportModel, CustomUser):
    id = m.TextField(primary_key=True)
    firstName = DefaultTextField()
    lastName = DefaultTextField()
    headline = DefaultTextField()
    apiUrl = DefaultTextField()
    siteUrl = DefaultTextField()
    pictureUrl = DefaultTextField()

    class Meta:
        app_label = 'linkedin'

    USERNAME_FIELD = 'id'

    def get_full_name(self):
        return ' '.join(getattr(self, attr)
                        for attr in ('firstName', 'lastName')
                        if getattr(self, attr, False))

    def __str__(self):
        return self.get_full_name() or str(self.id)

