from django.dispatch import Signal

from . import models as m

data_signal = Signal(providing_args=['data'])

def update_data(obj, data):
    for key in set(data) & set(obj.__dict__):
        setattr(obj, key, data[key])

def import_profile(data):
    profile, created = m.Profile.objects.get_or_create(id=data['id'])
    try:
        data['apiUrl'] = data.pop('apiStandardProfileRequest')['url']
    except KeyError:
        pass
    try:
        data['siteUrl'] = data.pop('siteStandardProfileRequest')['url']
    except KeyError:
        pass
    update_data(profile, data)
    profile.save()
    return profile

