from django.db import models as m

from utils.models import ExternalModel
from utils.fields import (DefaultTextField as DTF, DefaultIntegerField,
        DefaultBooleanField, TimestampField)

DefaultTextField = lambda *a, **kw: DTF(null=True, *a, **kw)

class User(ExternalModel):
    id = m.TextField(primary_key=True)
    permalink = DefaultTextField()
    username = DefaultTextField()
    uri = DefaultTextField()
    permalink_url = DefaultTextField()
    avatar_url = DefaultTextField()
    country = DefaultTextField()
    full_name = DefaultTextField()
    city = DefaultTextField()
    description = DefaultTextField()
    discogs = DefaultTextField()
    myspace = DefaultTextField()
    website = DefaultTextField()
    website = DefaultTextField()
    #online = BooleanField()
    track_count = DefaultIntegerField()
    playlist_count = DefaultIntegerField()
    followers_count = DefaultIntegerField()
    followings_count = DefaultIntegerField()
    public_favorites_count = DefaultIntegerField()
    plan = DefaultTextField()
    private_tracks_count = DefaultIntegerField()
    private_playlists_count = DefaultIntegerField()
    primary_email_confirmed = DefaultBooleanField()

    class Meta:
        app_label = 'soundcloud'

    def __unicode__(self):
        return self.full_name or self.username or self.id


class Track(ExternalModel):
    id = m.TextField(primary_key=True)
    #created_at = TimestampField()  #m.DateTimeField() #format "2009/08/13 18:30:10 +0000"
    user = m.ForeignKey(User, related_name='tracks', null=True)
    title = DefaultTextField()

    '''
    # Is created by FK already
    #user_id = DefaultTextField()
    permalink = DefaultTextField()
    permalink_url = DefaultTextField()
    uri = DefaultTextField()
    sharing = DefaultTextField()
    embeddable_by = DefaultTextField()  #"all", "me", or "none"
    purchase_url = DefaultTextField()
    artwork_url = DefaultTextField()
    description = DefaultTextField()
    label = m.ForeignKey(User, related_name='labeled_tracks', null=True)
    duration = DefaultIntegerField()
    genre = DefaultTextField()
    shared_to_count = DefaultTextField()
    tag_list = DefaultTextField()
    # Is created by FK already
    #label_id = DefaultIntegerField()
    label_name = DefaultTextField()
    license = DefaultTextField()
    release = DefaultIntegerField()
    release_day = DefaultIntegerField()
    release_month = DefaultIntegerField()
    release_year = DefaultIntegerField()
    streamable = DefaultBooleanField()
    downloadable = DefaultBooleanField()
    state = DefaultTextField()
    track_type = DefaultTextField()
    waveform_url = DefaultTextField()
    download_url = DefaultTextField()
    stream_url = DefaultTextField()
    video_url = DefaultTextField()
    bpm = DefaultTextField()
    commentable = DefaultTextField()
    isrc = DefaultTextField()
    key_signature = DefaultTextField()
    comment_count = DefaultTextField()
    download_count = DefaultTextField()
    playback_count = DefaultTextField()
    favoritings_count = DefaultTextField()
    original_format = DefaultTextField()
    original_content_size = DefaultTextField()
    created_with = m.ForeignKey(User, related_name='created_tracks', null=True)
    user_favorite = DefaultTextField() #auth only
    '''

    class Meta:
        app_label = 'soundcloud'

    def __unicode__(self):
        return self.title or unicode(self.id)

class Comment(ExternalModel):
    id = m.TextField(primary_key=True)
    #created_at = TimestampField()
    body = DefaultTextField()
    timestamp = DefaultIntegerField()
    uri = DefaultTextField()
    user = m.ForeignKey(User, related_name='comments', null=True)
    track = m.ForeignKey(Track, related_name='comments', null=True)

    class Meta:
        app_label = 'soundcloud'

    def __unicode__(self):
        return 'Comment by %s on %s' % (unicode(self.user), unicode(self.track))

