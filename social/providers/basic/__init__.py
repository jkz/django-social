"""
This is a small wrapper around Django's contrib.auth models. It serves as the
core User object provider for the social framework.
"""
from django.conf import settings

if not hasattr(settings, 'AUTH_USER_MODEL'):
    settings.AUTH_USER_MODEL = 'basic.User'
