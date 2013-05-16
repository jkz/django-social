import json

import acua
import stories

from ..models import Object, User
from ..shortcuts import JESSE_ZWAAN, PAGE_TAB

def require_model(model):
    def wrapper(func):
        def funk(obj, data):
            if isinstance(obj, basestring):
                obj = model.objects.get(pk=obj)
            return func(obj, data)
        return funk
    return wrapper


def import_object(data):
    obj = Object.objects.get_or_create(pk=data['id'])[0]
    obj.name = json.dumps(data)
    obj.save()
    return obj

@require_model(User)
def update_user(user, data):
    pass 


class Parser(object):
    def __init__(self, app):
        self.app = app

    def realtime_update(self, data):
        if data['object'] == 'user':
            for entry in data['entry']:
                obj = self.import_user_entry(entry)
                acc = acua.account(JESSE_ZWAAN)
                #acc.stories.fire(target=obj, name='realtime_facebook')
                stories.story('facebook_realtime', acc, obj)
                return obj, acc
        elif data['object'] == 'page':
            pass

    def import_user(self, entry):
        user, created = User.objects.get_or_create(pk=entry['uid'])
        req = self.service.suspend.GET(entry['uid'])
        if created:
            data = req()
        else:
            data = req(fields=','.join(entry['fields_changed']))
        return update_user(data) 

    def import_user_entry(self, entry):
        obj = Object.objects.get_or_create(pk=entry['uid'])[0]
        obj.name = json.dumps(entry)
        obj.save()
        return obj
        self.service.GET(entry['uid'], fields=','.join(entry['changed_fields']))



        if data['uid'] == PAGE_TAB.pk:
            obj._type = 'page_tab'
        else:
            obj._type = 'other'
