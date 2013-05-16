"""
Providers are third party apps which can be used for authentication or api
consumption.
"""
from django.conf import settings

settings.PROVIDERS = getattr(settings, 'PROVIDERS', {})

# Automagically add all providers in settings.PROVIDERS to installed apps
for provider, params in settings.PROVIDERS.items():
    INSTALLED_APPS += params.get('app', '.'.join((__name__, provider))),

