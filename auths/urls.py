from django.conf.urls import url, patterns

from . import views as v

urlpatterns = patterns('',
    url(r'^connect/$', v.connect, name='auth_request'),
    url(r'^connect/callback/$', v.callback, name='auth_callback'),
    url(r'^disconnect/$', v.disconnect, name='auth_disconnect'),
)
