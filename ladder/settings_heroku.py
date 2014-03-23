import os
from settings import *  # NOQA

import herokuify

from herokuify.common import *  # NOQA
from herokuify.aws import *  # NOQA
from herokuify.mail.sendgrid import *  # NOQA

from ladder.settings_aws import *  # NOQA

# Cache setup
CACHES = herokuify.get_cache_config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SSL
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# used cached template loader
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

DATABASES = herokuify.get_db_config()
CACHES = herokuify.get_cache_config()

DEBUG = os.environ.get('DJANGO_DEBUG') == 'True'
TEMPLATE_DEBUG = DEBUG

# Set your DSN value
RAVEN_CONFIG = {
    'dsn': os.environ['SENTRY_DSN'],
}

MIDDLEWARE_CLASSES = (
    'sslify.middleware.SSLifyMiddleware',
) + MIDDLEWARE_CLASSES
