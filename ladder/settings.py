# Django settings for ladder project.
import os
import excavator

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ADMINS = (
    ('Piper', 'piper@thefuckingunicorns.com'),
)

DEFAULT_FROM_EMAIL = 'ladder@apogaea.com'

MANAGERS = ADMINS

import herokuify

DEBUG = TEMPATE_DEBUG = excavator.env_bool('DJANGO_DEBUG', default=False)

# Allowed Hosts
ALLOWED_HOSTS = excavator.env_list('DJANGO_ALLOWED_HOSTS', required=True)


# Database setup
DATABASES = {
    'default': dj_database_url.parse(excavator.env_string('DATABASE_URL', required=True)),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Denver'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# File Storage
DEFAULT_FILE_STORAGE = excavator.env_string('DJANGO_DEFAULT_FILE_STORAGE', required=True)
STATICFILES_STORAGE = excavator.env_string('DJANGO_STATICFILES_STORAGE', required=True)

# User-uploaded files
MEDIA_ROOT = excavator.env_string('DJANGO_MEDIA_ROOT')
MEDIA_URL = excavator.env_string('DJANGO_MEDIA_URL', default='/media/')

# Static files
STATIC_ROOT = excavator.env_string('DJNGO_STATIC_ROOT')
STATIC_URL = excavator.env_string('DJANGO_STATIC_URL', default='/static/')

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'ladder', 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Production installs need to have this environment variable set
SECRET_KEY = excavator.env_string('DJANGO_SECRET_KEY', required=True)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'ladder.urls'

# Twilio
# These codes should be eithe set in an untracked settings file.
TWILIO_ACCOUNT_SID = excavator.env_string('TWILIO_ACCOUNT_SID', required=True)
TWILIO_AUTH_TOKEN = excavator.env_string('TWILIO_AUTH_TOKEN', required=True)
TWILIO_PHONE_NUMBER = excavator.env_string('TWILIO_PHONE_NUMBER', required=True)

# Global Pagination
PAGINATE_BY = 10

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/account/'
LOGIN_ERROR_URL = '/login-error/'

AUTH_USER_MODEL = 'accounts.User'

# The amount of time in seconds that a user has to accept a match.
ONE_DAY_IN_SECONDS = 24 * 60 * 60
DEFAULT_ACCEPT_TIME = 2 * ONE_DAY_IN_SECONDS

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ladder.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Toolbox
    'compressor',
    'django_extensions',
    'storages',
    'authtools',
    'raven.contrib.django.raven_compat',

    # Main App
    'ladder',
    # Project Apps
    'accounts',
    'exchange',
)

SESSION_COOKIE_HTTPONLY = True


# Email Settings
EMAIL_LAYOUT = 'mail/base.html'
EMAIL_BACKEND = excavator.env_string(
    'DJANGO_EMAIL_BACKEND',
    default='django.core.mail.backends.smtp.EmailBackend',
)
EMAIL_HOST = excavator.env_string('EMAIL_HOST', default='localhost')
EMAIL_HOST_USER = excavator.env_string('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = excavator.env_string('EMAIL_HOST_PASSWORD', default='')
EMAIL_PORT = excavator.env_string('EMAIL_PORT', default='25')
EMAIL_USE_TLS = excavator.env_bool('EMAIL_USE_TLS')
EMAIL_USE_SSL = excavator.env_bool('EMAIL_USE_SSL')


# AWS Config
AWS_ACCESS_KEY_ID = excavator.env_string('AWS_ACCESS_KEY_ID', required==True)
AWS_SECRET_ACCESS_KEY = excavator.env_string'AWS_SECRET_ACCESS_KEY', required==True)
AWS_STORAGE_BUCKET_NAME = excavator.env_string'AWS_STORAGE_BUCKET_NAME', required==True)

# TODO: is this stuff needed?
AWS_REDUCED_REDUNDANCY = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = True
AWS_S3_SECURE_URLS = True
AWS_IS_GZIPPED = False
AWS_PRELOAD_METADATA = True
AWS_HEADERS = {
    "Cache-Control": "public, max-age=86400",
}

# Cache setup
CACHES = herokuify.get_cache_config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# used cached template loader
# TODO: bad for dev.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

# Sentry error reporting.
RAVEN_CONFIG = {
    'dsn': excavator.env_string('SENTRY_DSN', default=None)
}
