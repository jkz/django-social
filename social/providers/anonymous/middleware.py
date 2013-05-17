from django.conf import settings
from django.utils.translation import ugettext as _

from ..auth import views

if not ('django.contrib.sessions.middleware.SessionMiddleware' in
        settings.MIDDLEWARE_CLASSES):
    #XXX proper exception would be nice
    raise Exception(_("django.contrib.sessions.middleware.SessionMiddleware is
            required for AnonymousMiddleware"))

class AnonymousMiddleware:
    """
    This middleware makes sure there is an authenticated user present on every
    request, by creating a User object for the session_key when needed.
    """
    def process_request(self, request):
        #TODO set some conditions to not create a shitload of session users for
        # robots and jokers
        if not request.user.is_authenticated():
            if not request.session.get(views.PROVIDER_SESSION_KEY, False):
                views.connect(request, provider='session')
                views.callback(request)

