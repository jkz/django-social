from datetime import datetime
from django.dispatch import receiver

from .models import Token
from celery import Celery
celery = Celery()
import parser

@celery.task
def statusstream(token_id, **kwargs):
    @receiver(parser.data_signal)
    def listener(data, **kwargs):
        statusstream.backend.store_result(
            task_id=statusstream.request.id,
            result={'timestamp': datetime.now()},
            status=(str(token_id) + ' ' + str(data)))
            #status=[(obj.__class__.__name__, obj.pk) for obj in data])

    print 'USERSTREAM LOCALS', locals()

    token = Token.objects.get(pk=token_id)
    token.statusstream.filter(**kwargs)

@celery.task
def userstream(token_id, **kwargs):
    @receiver(parser.data_signal)
    def listener(data, **kwargs):
        userstream.backend.store_result(
            task_id=userstream.request.id,
            result={'timestamp': datetime.now()},
            status=(str(token_id) + ' ' + str(data)))
            #status=[(obj.__class__.__name__, obj.pk) for obj in data])

    token = Token.objects.get(pk=token_id)
    token.userstream(**kwargs)

def userstream_status(task_id):
    return userstream.AsyncResult(task_id).state

def list_streams(name):
    active = celery.control.inspect().active()
    return [task['id']
            for name, worker in active.iteritems()
            for task in worker
            if task['name'] == 'external.twitter.tasks.' + name]

def userstream_status(task_id):
    return userstream.AsyncResult(task_id).state

def stop_stream(task_id):
    celery.control.revoke(task_id, terminate=True, signal='SIGKILL')
    return 'SUCCESS'

@celery.task
def import_user(user_id, token_id):
    token = Token.objects.get(pk=token_id)
    data = token.api.get_user(user_id)
    return parser.import_user(data)


@celery.task
def backfill(token_id, since_id=None, max_id=None):
    """
    Backfill the timeline of authenticated user with the REST api.
    """
    token = Token.objects.get(pk=token_id)
    data = token.api.get_timeline(token.user.pk, since_id=since_id,
            max_id=max_id)
    return parser.import_data(data)

