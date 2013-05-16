from .models import Token

import parsers

from celery import Celery
celery = Celery()

@celery.task
def import_user(token_pk):
    token = Token.objects.get(pk=token_pk)
    data = token.api.me()
    parsers.import_user(data)

@celery.task
def import_playbacks(token_pk, *artist_pks):
    token = Token.objects.get(pk=token_pk)
    for artist in artist_pks:
        data = token.api.get_user_tracks(artist)
        parsers.import_tracks(data, token.user)

@celery.task
def backfill(token_id, since_id=None, max_id=None):
    """
    Backfill the timeline of authenticated user with the REST api.
    """
    token = Token.objects.get(pk=token_id)
    #TODO: since_id/max_id
    data = token.api.get_my_own_activities()
    print data
    return parsers.import_activities(data)

