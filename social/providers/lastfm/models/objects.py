from functools import partial
from django.db import models as m

from utils.models import ImportModel, CustomUser

DefaultTextField = partial(m.TextField, null=True)
#TODO IntField that calls int() on its argument

class User(ImportModel, CustomUser):
    id = m.BigIntegerField(primary_key=True)
    name = DefaultTextField()
    realname = DefaultTextField()
    url = DefaultTextField()
    image_small = DefaultTextField()
    image_medium = DefaultTextField()
    image_large = DefaultTextField()
    image_extralarge = DefaultTextField()
    country = DefaultTextField()
    gender = DefaultTextField()
    """
    age = DefaultIntegerField()
    subscriber = DefaultIntegerField()
    playcount = DefaultIntegerField()
    playlists = DefaultIntegerField()
    bootstrap = DefaultIntegerField()
    registered = DefaultIntegerField()
    """

    class Meta:
        app_label = 'lastfm'

    def avatar(self):
        return (self.image_medium
                or self.image_small
                or self.image_large
                or self.image_extralarge
                or 'http://placekitten.com/60/')

    USERNAME_FIELD = 'id'

    def get_short_name(self):
        return self.name or str(self)

    def __str__(self):
        return self.realname or self.name or str(self.pk)


class Artist(ImportModel):
    #mbid = m.TextField(primary_key=True, null=True)
    name = m.TextField(unique=True)
    url = DefaultTextField()

    class Meta:
        app_label = 'lastfm'

    def __str__(self):
        return self.name or str(self.pk)


class Track(ImportModel):
    #mbid = m.TextField(unique=True, null=True)
    name = DefaultTextField(unique=True)
    artist = m.ForeignKey(Artist, related_name='tracks')

    def __str__(self):
        return self.name or str(self.pk)

    class Meta:
        app_label = 'lastfm'

