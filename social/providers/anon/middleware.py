import auths

from . import models

class AnonMiddleware:
    def process_request(self, request):
        if request.user.is_authenticated():
            return

        request.consumer = models.Consumer()
        request.provider = models.Provider()
        auths.callback(request)

