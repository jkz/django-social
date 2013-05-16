from .models import Token
from celery import Celery
celery = Celery()
import parser

@celery.task
def import_post(blog, post_id, token_id):
    token = Token.objects.get(pk=token_id)
    data = token.api.get_post(blog, post_id)
    return parser.import_post(data)
