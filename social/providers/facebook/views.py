import json

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from . import errors

@csrf_exempt
def realtime_callback(request, verify_token):
    """
    hub.mode
    hub.challenge
    hub.verify_token
    """
    print 'calling back'
    if request.method == 'GET':
        if (verify_token == request.GET.get('hub.verify_token', None)
        and request.GET.get('hub.mode', None)):
            return HttpResponse(request.GET.get('hub.challenge', None))
        return HttpResponse('')
    elif request.method =='POST':
        print 'POST'
        #TODO: verify sha1 signature
        #meta.HTTP_X_HUB_SIGNATURE
        try:
            data = json.loads(request.body)

        #XXX: Not sure if this is the exception raised, maybe log something?
        except ValueError:
            raise

        try:
            #data = Parser(request.client).realtime_update(data)
            pass
        except errors.ParseError:
            #TODO: log
            raise
        return HttpResponse(str(data))
