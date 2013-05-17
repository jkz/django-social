"""
Accounts are User objects bound to a composite user object.
This allows authentication by multiple providers for a single user.
"""
from django.conf import settings

settings.USE_ACCOUNTS = True
