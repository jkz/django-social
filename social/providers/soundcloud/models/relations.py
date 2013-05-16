from django.db import models as m

from .objects import User, Track
from utils.fields import TimestampField
from utils.models import QuerySetManager

class PlaybackManager(m.Manager):
    def put(self, track, user, new):
        if new:
            old = track.playbacks.filter(user=user).sum()
            difference = int(new) - old
            if difference:
                track.playbacks.create(user=user, count=difference)


class Playback(m.Model):
    user = m.ForeignKey(User, related_name='playbacks')
    track = m.ForeignKey(Track, related_name='playbacks')
    timestamp = TimestampField()
    count = m.IntegerField()

    objects = QuerySetManager()
    parser = PlaybackManager()

    class Meta:
        app_label = 'soundcloud'

    def __unicode__(self):
        return '%sx %s by %s' % (self.count, unicode(self.track),
                unicode(self.user))

    class QuerySet(m.query.QuerySet):
        def sum(self):
            return self.aggregate(m.Sum('count'))['count__sum'] or 0

class FavoriteManager(m.Manager):
    def put(self, track, user, is_favorite):
        if is_favorite:
            track.favorites.get_or_create(user=user)
        else:
            track.favorites.filter(user=user).delete()

class Favorite(m.Model):
    user = m.ForeignKey(User, related_name='favorites')
    track = m.ForeignKey(Track, related_name='favorites')
    timestamp = TimestampField()

    objects = m.Manager()
    parser = FavoriteManager()

    class Meta:
        app_label = 'soundcloud'

    def __unicode__(self):
        return '%s favorites %s' % (unicode(self.user), unicode(self.track))

