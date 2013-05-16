"""
# Parses twitter dates stored in json # from twitter-python
def parse_datetime(string):
    # Set locale for date parsing
    locale.setlocale(locale.LC_TIME, 'C')

    # We must parse datetime this way to work in python 2.4
    date = datetime(*(time.strptime(string, '%a %b %d %H:%M:%S +0000 %Y')[0:6]))

    # Reset locale back to the default setting
    locale.setlocale(locale.LC_TIME, '')
    return date
"""
import datetime
import dateutil.parser

from django.db.models.fields import DateTimeField
from django.dispatch import Signal

from . import models as m

data_signal = Signal(providing_args=['data'])

def listify(obj):
    return obj if isinstance(obj, list) else [obj]

def convert_timestamp(timestamp):
    return dateutil.parser.parse(timestamp)
    return datetime.datetime.strptime(timestamp, '%a %b %d %H:%M:%S +0000 %Y')


def update_data(obj, data):
    for key in set(data) & set(obj._meta.get_all_field_names()):
        val = data[key]
        # Convert timestamp fields from UTC to unix
        if isinstance(obj._meta.get_field(key), DateTimeField):
            val = convert_timestamp(val)
        setattr(obj, key, val)


def import_images(data, obj):
    for image in data:
        setattr(obj, 'image_' + image['size'], image['#text'])

def import_user(data):
    user, created = m.User.objects.get_or_create(id=data['id'])
    import_images(data.pop('image', []), user)
    update_data(user, data)
    user.save()
    return user

def import_users(json):
    for data in listify(json.get('user', [])):
        import_data(data)

def import_artist(data):
    print data
    artist, created = m.Artist.objects.get_or_create(name=data['name'])
    update_data(artist, data)
    artist.save()
    return artist

def import_artists(json):
    for data in listify(json.get('artist', [])):
        import_artist(data)

def import_playcount(track, user, new):
    if new:
        old = track.playcounts.filter(user=user).sum()
        difference = int(new) - old
        if difference:
            track.playcounts.create(user=user, count=difference)

def import_love(track, user):
    track.loves.objects.get_or_create(user=user)


def import_track(json, user=None):
    for data in listify(json.get('track', [])):
        artist = import_artist(data.pop('artist'))
        track, created = artist.tracks.get_or_create(name=data['name'])
        update_data(track, data)
        track.save()
        if user:
            count = data.get('userplaycounts', data.get('playcount'))
            if count:
                import_playcount(track, user, count)

            loved = data.get('userloved', False)
            if loved:
                import_love(track, user)


def import_scrobble(data):
    pass

def import_album(data):
    pass

def import_library(data, user):
    import_artists(data.pop('artists', {}))
    import_album(data.pop('albums', {}))
    import_track(data.pop('tracks', {}), user)

def import_data(data):
    if not hasattr(data, '__iter__'):
        return
    import_track(data)
    import_artists(data)
    import_users(data)

