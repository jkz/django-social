from . import models as m

def import_user(data):
    user = m.User(**data)
    user.save()
    return user

def import_status(data):
    pass
