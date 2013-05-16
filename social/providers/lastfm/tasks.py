from .models import Token, Artist

import parsers

from celery import Celery
celery = Celery()

@celery.task
def import_user(token_pk, *artist_pks):
    token = Token.objects.get(pk=token_pk)
    data = token.api.get_user(token.user.pk)
    user = parsers.import_user(data['user'])
    for artist in Artist.objects.filter(pk__in=artist_pks):
        data = token.api.get_library(artist.name)
        parsers.import_library(data, user)

@celery.task
def import_library(token_pk, *artist_pks):
    token = Token.objects.get(pk=token_pk)
    for artist in Artist.objects.filter(pk__in=artist_pks):
        data = token.api.get_library(artist.name)
        parsers.import_library(data, token.user)

