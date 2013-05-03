Django Auths is a framework for social authentication within Django.

Several third party backends are included.

Installation
------------

  #settings.py

  # When more than one service is specified, multiple accounts can be connected
  # to a single composite user.
  AUTHS = {
    'facebook': {
      'app': 'social.facebook',
      'creds': {
        'key': 'YOURAPPKEY',
        'secret': 'YOURAPPSECRET',
    }
    'twitter': {
      'app': 'social.twitter',
      'creds': {
        'key': 'YOURAPPKEY',
        'secret': 'YOURAPPSECRET',
    }
    'googleplus': {
      'app': 'social.googleplus',
      'creds': {
        'key': 'YOURAPPKEY',
        'secret': 'YOURAPPSECRET',
    }
  }

  AUTHS['default'] = AUTHS['facebook']

  MIDDLEWARE_CLASSES += ('auths.middleware.AuthMiddleware',)

  AUTHENTICATION_BACKENDS += ('auths.backends.UserBackend',)

  INSTALLED_APPS += ('social.facebook', 'social.twitter', 'social.googleplus')

