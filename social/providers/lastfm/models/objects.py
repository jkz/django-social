from functools import partial
from django.db import models as m

DefaultTextField = partial(m.TextField, null=True)
#TODO IntField that calls int() on its argument

class User(m.Model):
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

    @property
    def AVATAR_URL(self):
        return (self.image_medium
                or self.image_small
                or self.image_large
                or self.image_extralarge
                or 'http://placekitten.com/60/')

    def __unicode__(self):
        return self.realname or self.name or unicode(self.pk)

    class Meta:
        app_label = 'lastfm'


class Artist(m.Model):
    #mbid = m.TextField(primary_key=True, null=True)
    name = m.TextField(unique=True)
    url = DefaultTextField()

    class Meta:
        app_label = 'lastfm'

    def __unicode__(self):
        return self.name or unicode(self.pk)


class Track(m.Model):
    #mbid = m.TextField(unique=True, null=True)
    name = DefaultTextField(unique=True)
    artist = m.ForeignKey(Artist, related_name='tracks')

    def __unicode__(self):
        return self.name or unicode(self.pk)

    class Meta:
        app_label = 'lastfm'

