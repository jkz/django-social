from django.contrib.auth.models import AbstractBaseUser
from django.db import models as m

from utils.fields import DefaultTextField

class Object(m.Model):
    id = m.TextField(primary_key=True)
    name = DefaultTextField()
    _type = DefaultTextField()

    class Meta:
        app_label = 'facebook'


class User(Object, AbstractBaseUser):
    USERNAME_FIELD = 'id'

    first_name = DefaultTextField()
    middle_name = DefaultTextField()
    last_name = DefaultTextField()
    gender = DefaultTextField()
    locale = DefaultTextField()
    link = DefaultTextField()
    username = DefaultTextField()
    gender = DefaultTextField()
    timezone = m.IntegerField(null=True)
    updated_time = m.DateTimeField(null=True)
    verified = m.BooleanField(default=False)
    bio = DefaultTextField()
    birthday = m.DateField(null=True)
    email = DefaultTextField()
    hometown = DefaultTextField()
    political = DefaultTextField()
    picture = DefaultTextField()
    quotes = DefaultTextField()
    relationship_status = DefaultTextField()
    religion = DefaultTextField()
    email = DefaultTextField()
    website = DefaultTextField()

    #interested_in = m.ManyToManyField(Object, related_name='interested_by', null=True)
    #location = m.ForeignKey(Object, related_name='inhabitants', null=True)
    #GOTCHA! need to specify object link becauser thinks is pk
    #significant_other = m.OneToOneField(Object, related_name='partner', null=True)
    #languages = m.ManyToManyField(Object, related_name='speakers', null=True)
    #education = m.ManyToManyField(Object, related_name='students', null=True)
    #favorite_athletes = DefaultTextField(Object, related_name='fans')
    #favorite_teams = DefaultTextField(Object, related_name='fans')
    #video_upload_limits
    #third_party_id
    #work

    class Meta:
        app_label = 'facebook'

    def get_full_name(self):
        return ' '.join(getattr(self, attr)
                        for attr in ('first_name', 'middle_name', 'last_name')
                        if getattr(self, attr, False))

    def get_short_name(self):
        return self.first_name or self.username or self.pk

    def __str__(self):
        return self.get_full_name() or self.name or self.username or self.pk

