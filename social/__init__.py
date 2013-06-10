"""
Providers are third party apps which can be used for authentication or api
consumption.
"""
from django.conf import settings
from django.utils.importlib import import_module
from django.db.models.loading import get_models, register_models

settings.PROVIDERS = getattr(settings, 'PROVIDERS', {})

# Automagically add all providers in settings.PROVIDERS to installed apps
for provider, params in settings.PROVIDERS.items():
    module = params.get('app', '.'.join((__name__, 'providers', provider)))
    #settings.INSTALLED_APPS += module,
    import_module('.'.join((__name__, 'auth.backends', provider)))

