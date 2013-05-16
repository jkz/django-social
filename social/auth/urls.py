from django.conf.urls import url, patterns
from django.conf import settings

from . import views as v


urlpatterns = patterns('',
    url(r'^{}$'.format(settings.LOGIN_URL.lstrip('/')), v.connect,
        name='auth_request'),

    url(r'^{}$'.format(settings.LOGIN_CALLBACK_URL.lstrip('/')), v.callback,
        name='auth_callback'),

    url(r'^{}$'.format(settings.LOGOUT_URL.lstrip('/')), v.disconnect,
        name='auth_disconnect'),
)

if settings.USE_ACCOUNTS:
    providers = '|'.join(settings.PROVIDERS.keys())

    urlpatterns += url(r'^{}/(?P<provider>{})/$'.format(
        settings.LOGIN_URL.strip('/'), providers),
            v.connect, name='auth_request'),

    urlpatterns += url(r'^{}/(?P<provider>{})/$'.format(
        settings.LOGOUT_URL.strip('/'), providers),
            v.disconnect, name='auth_disconnect'),
