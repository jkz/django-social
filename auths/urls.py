from django.conf.urls import url, patterns
from django.conf import settings

from . import views as v


urlpatterns = patterns('',
    url(r'^connect/$', v.connect, name='auth_request'),
    url(r'^connect/callback/$', v.callback, name='auth_callback'),
    url(r'^disconnect/$', v.disconnect, name='auth_disconnect'),
)

if settings.AUTH_MULTI:
    namespaces = '|'.join(set(settings.AUTHS.keys()) - set(['default']))
    urlpatterns += url(r'^connect/(?P<namespace>{})/$'.format(namespaces),
            v.connect, name='auth_request'),
    urlpatterns += url(r'^disconnect/(?P<namespace>{})/$'.format(namespaces),
            v.disconnect, name='auth_disconnect'),
