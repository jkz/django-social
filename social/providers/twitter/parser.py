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

def convert_timestamp(timestamp):
    return dateutil.parser.parse(timestamp)
    return datetime.datetime.strptime(timestamp, '%a %b %d %H:%M:%S +0000 %Y')


def update_data(obj, data):
    for key in set(data) & set(obj.__dict__):
        val = data[key]
        # Convert timestamp fields from UTC to unix
        if type(obj._meta.get_field(key)) == DateTimeField:
            val = convert_timestamp(val)
        setattr(obj, key, val)

def import_follow(data):
    target = import_user(data['target'])
    source = import_user(data['source'])
    follow, created = m.Follow.objects.get_or_create(
            target=target, source=source,
            created_at=convert_timestamp(data['created_at']))
    return follow

def import_retweet(data):
    user = import_user(data['user'])
    status = import_status(data['source'])
    retweet, created = m.Retweet.objects.get_or_create(
            user=user, status=status,
            created_at=convert_timestamp(data['created_at']))
    return retweet

def import_event(data):
    return dict(
        follow=import_follow,
        retweet=import_retweet
    )[data['event']](data)


def import_mention(data, status):
    user = import_user(data)
    mention, created = m.Mention.objects.get_or_create(user=user, status=status)
    return mention

def import_hashtag(data, status):
    hashtag, created = m.Hashtag.objects.get_or_create(pk=data['text'].lower())
    hashuse, created = m.HashUse.objects.get_or_create(hashtag=hashtag, status=status)
    return hashuse

def import_entities(data, status):
    return [import_mention(mention, status) for mention in data['user_mentions']] \
         + [import_hashtag(hashtag, status) for hashtag in data['hashtags']]

def import_user(data):
    user, created = m.User.objects.get_or_create(id=data['id'])
    update_data(user, data)
    user.save()
    return user

def import_status(data):
    user = import_user(data.pop('user'))
    status, created = user.statuses.get_or_create(id=data['id'])
    update_data(status, data)
    status.save()
    if 'entities' in data:
        return [status] + import_entities(data['entities'], status)
    return [status]


def _import_data(data):
    if not hasattr(data, '__iter__'):
        return
    elif 'disconnect' in data:
        return
    # A user stream event
    elif 'event' in data:
        return import_event(data)
    # A status has a user field
    elif 'user' in data:
        return import_status(data)
    # A user has a status field
    elif 'status' in data:
        return import_user(data)
    # Import a list of entries one by one
    elif isinstance(data, list):
        return [_import_data(entry) for entry in data]


def import_data(data):
    return data_signal.send(__name__, data=_import_data(data))

def shouter(data, **kwargs):
    print data
data_signal.connect(shouter)
