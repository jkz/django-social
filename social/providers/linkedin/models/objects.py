from django.db import models as m

from utils.fields import DefaultTextField


class Profile(m.Model):
    id = m.TextField(primary_key=True)
    firstName = DefaultTextField()
    lastName = DefaultTextField()
    headline = DefaultTextField()
    apiUrl = DefaultTextField()
    siteUrl = DefaultTextField()
    pictureUrl = DefaultTextField()

    @property
    def name(self):
        return ' '.join((self.firstName, self.lastName))

    def __unicode__(self):
        return self.name or unicode(self.id)

    class Meta:
        app_label = 'linkedin'

