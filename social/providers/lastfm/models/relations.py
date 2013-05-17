from django.db import models as m

from .objects import User, Track
from utils.fields import TimestampField
from utils.models import QuerySetModel

class Scrobble(m.Model):
    user = m.ForeignKey(User, related_name='scrobbles')
    track = m.ForeignKey(Track, related_name='scrobbles')
    timestamp = TimestampField()

    class Meta:
        app_label = 'lastfm'


    def __unicode__(self):
        return '%s played %s' % (unicode(self.user), unicode(self.track))


class Love(m.Model):
    user = m.ForeignKey(User, related_name='loves')
    track = m.ForeignKey(Track, related_name='loves')
    timestamp = TimestampField()

    class Meta:
        app_label = 'lastfm'


    def __unicode__(self):
        return '%s loves %s' % (unicode(self.user), unicode(self.track))


class PlayCount(QuerySetModel):
    user = m.ForeignKey(User, related_name='playcounts')
    track = m.ForeignKey(Track, related_name='playcounts')
    timestamp = TimestampField()
    count = m.IntegerField()

    class Meta:
        app_label = 'lastfm'

    def __unicode__(self):
        return '%sx %s by %s' % (self.count, unicode(self.track),
                unicode(self.user))

    class QuerySet(m.query.QuerySet):
        def sum(self):
            return self.aggregate(m.Sum('count'))['count__sum'] or 0

