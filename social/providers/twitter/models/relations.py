from django.db import models as m

from .objects import User, Status, Hashtag

from utils.models import QuerySetModel, RequestQuerySet

class Mention(m.Model):
    user = m.ForeignKey(User, related_name='mentions')
    status = m.ForeignKey(Status, related_name='mentions')

    class Meta:
        unique_together = ('user', 'status')
        app_label = 'twitter'


    def __unicode__(self):
        return '%s in %s' % (unicode(self.user), unicode(self.status))


class HashUse(QuerySetModel):
    hashtag = m.ForeignKey(Hashtag, related_name='statuses')
    status = m.ForeignKey(Status, related_name='hashtags')

    class Meta:
        unique_together = ('hashtag', 'status')
        app_label = 'twitter'


    def __unicode__(self):
        return '%s in %s' % (unicode(self.hashtag), unicode(self.status))

    class QuerySet(RequestQuerySet): pass


class Follow(m.Model):
    target = m.ForeignKey(User, related_name='followers')
    source = m.ForeignKey(User, related_name='follows')
    created_at = m.DateTimeField(null=True)

    def __unicode__(self):
        return '%s by %s' % (unicode(self.target), unicode(self.source))

    class Meta:
        app_label = 'twitter'

class Retweet(m.Model):
    status = m.ForeignKey(Status, related_name='retweets')
    user = m.ForeignKey(User, related_name='retweets')
    created_at = m.DateTimeField(null=True)

    class Meta:
        app_label = 'twitter'

