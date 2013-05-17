from django.db import models as m

from .objects import User, Status, Hashtag

from utils.models import QuerySetModel, RequestQuerySet

class Mention(m.Model):
    user = m.ForeignKey(User, related_name='mentions')
    status = m.ForeignKey(Status, related_name='mentions')

    class Meta:
        unique_together = ('user', 'status')
        app_label = 'twitter'


    def __str__(self):
        return '{} in {}'.format(self.user, self.status)


class HashUse(QuerySetModel):
    hashtag = m.ForeignKey(Hashtag, related_name='statuses')
    status = m.ForeignKey(Status, related_name='hashtags')

    class Meta:
        unique_together = ('hashtag', 'status')
        app_label = 'twitter'


    def __str__(self):
        return '{} in {}'.format(self.hashtag, self.status)

    class QuerySet(RequestQuerySet): pass


class Follow(m.Model):
    target = m.ForeignKey(User, related_name='followers')
    source = m.ForeignKey(User, related_name='follows')
    created_at = m.DateTimeField(null=True)

    def __str__(self):
        return '{} by {}'.format(self.target, self.source)

    class Meta:
        app_label = 'twitter'

class Retweet(m.Model):
    status = m.ForeignKey(Status, related_name='retweets')
    user = m.ForeignKey(User, related_name='retweets')
    created_at = m.DateTimeField(null=True)

    class Meta:
        app_label = 'twitter'

    def __str__(self):
        return '{} RT: {}'.format(self.user, self.status)
