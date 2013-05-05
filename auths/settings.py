from django import conf

DEFAULT_BACKEND = 'auths.backends.UserBackend'
DEFAULT_MIDDLEWARE = 'auths.backends.AuthMiddleware'

AUTHS = getattr(conf.settings, 'AUTHS', ())

APPS = set(auth['app'] for auth in AUTHS)

INSTALLED_APPS = getattr(conf.settings, 'INSTALLED_APPS', ())

conf.settings.INSTALLED_APPS = INSTALLED_APPS + tuple(APPS)

BACKENDS = getattr(conf.settings, 'AUTHENTICATION_BACKENDS', ())

if not DEFAULT_BACKEND in BACKENDS:
    conf.settings.AUTHENTICATION_BACKENDS = BACKENDS + (DEFAULT_BACKEND,)

SESSION_MIDDLEWARE = 'django.contrib.sessions.middleware.SessionMiddleware'

MIDDLEWARE_CLASSES = getattr(conf.settings, 'MIDDLEWARE_CLASSES', ())
if not SESSION_MIDDLEWARE in MIDDLEWARE_CLASSES:
    raise Exception("Auths requires {} in MIDDLEWARE_CLASSES".format(
        SESSION_MIDDLEWARE))

index = MIDDLEWARE_CLASSES.index(SESSION_MIDDLEWARE)
conf.settings.MIDDLEWARE_CLASSES = (
        MIDDLEWARE_CLASSES[:index + 1] +
        (DEFAULT_MIDDLEWARE,) +
        MIDDLEWARE_CLASSES[index + 1:])

