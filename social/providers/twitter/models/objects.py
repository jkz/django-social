from django.contrib.auth.models import AbstractBaseUser
from django.db import models as m

from utils.fields import NullTextField, TimestampField


class User(AbstractBaseUser):
    USERNAME_FIELD = 'id'

    """Twitter user infomation"""
    # Active fields
    id = m.BigIntegerField(primary_key=True)
    id_str = NullTextField()
    name = NullTextField()
    screen_name = NullTextField()
    description = NullTextField()
    profile_image_url = NullTextField()

    # Timestamps
    date_acquired = TimestampField()
    last_update = m.DateTimeField(auto_now=True)

    # Future fields
    """
    protected = m.BooleanField(null=True)
    verified = m.BooleanField(null=True)
    created_at = m.DateTimeField(null=True)
    followers_count = m.PositiveIntegerField(null=True)
    favourites_count = m.PositiveIntegerField(null=True)
    statuses_count = m.PositiveIntegerField(null=True)
    url = m.URLField(verify_exists=False)
    location = m.CharField(max_length=30, blank=True)
    time_zone = m.CharField(max_length=50, blank=True)
    utc_offset = m.IntegerField(null=True)
    """

    def __unicode__(self):
        return ((self.screen_name and '@%s' % self.screen_name)
                or self.name
                or unicode(self.id))

    class Meta:
        app_label = 'twitter'


class Hashtag(m.Model):
    text = m.TextField(primary_key=True)

    def __unicode__(self):
        return '#%s' % self.text

    class Meta:
        app_label = 'twitter'


class Status(m.Model):

    # Active fields
    id = m.BigIntegerField(primary_key=True)
    id_str = NullTextField()
    text = NullTextField()
    retweet_count = m.PositiveIntegerField(null=True, help_text="Upperbounded by 100+")
    created_at = m.DateTimeField(null=True)

    in_reply_to_status_id = m.BigIntegerField(null=True)
    in_reply_to_user_id = m.BigIntegerField(null=True)
    in_reply_to_screen_name = NullTextField(null=True)

    # Timestamps
    first_update = m.DateTimeField(auto_now_add=True)
    last_update = m.DateTimeField(auto_now=True)

    # Connections
    user = m.ForeignKey(User, related_name='statuses', null=True)

    # Future fields
    """
    source = NullTextField(blank=True)
    source_url = m.URLField(verify_exists=False)
    truncated = m.BooleanField(null=True)
    """

    def __unicode__(self):
        return '%s: %s' % (unicode(self.user), self.text)  #TODO: perhaps [:40])

    class Meta:
        app_label = 'twitter'

