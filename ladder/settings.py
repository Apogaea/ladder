# Django settings for ladder project.
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ADMINS = (
    ('Piper', 'piper@thefuckingunicorns.com'),
)

DEFAULT_FROM_EMAIL = 'ladder@apogaea.com'

MANAGERS = ADMINS

import herokuify

DEBUG = TEMPATE_DEBUG = os.environ.get('DJANGO_DEBUG') == 'True'

# Allowed Hosts
ALLOWED_HOSTS = []
ALLOWED_HOSTS += filter(
    bool,
    os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(','),
)

# Database setup
DATABASES = herokuify.get_db_config()
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


# User-uploaded files
STATIC_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'ladder', 'public'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'compressor.finders.CompressorFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Production installs need to have this environment variable set
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

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
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_PHONE_NUMBER = os.environ['TWILIO_PHONE_NUMBER']

# Global Pagination
PAGINATE_BY = 10

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/account/'
LOGIN_ERROR_URL = '/login-error/'

AUTH_USER_MODEL = 'accounts.User'

# The amount of time in seconds that a user has to accept a match.
DEFAULT_ACCEPT_TIME = 2 * 24 * 60 * 60

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

SCSS_IMPORTS = (
    STATICFILES_DIRS[0] + '/css',
)

COMPRESS_ENABLED = True
COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/less', 'lessc {infile} {outfile}'),
    ('text/x-sass', 'sass {infile} {outfile}'),

    # requires pyScss
    ('text/x-scss', 'pyscss {infile} -o {outfile} %s' %
     '-I ' + ' '.join(['"%s"' % d for d in SCSS_IMPORTS])
     )
)

FORCE_SCRIPT_NAME = ''

# <https://www.owasp.org/index.php/HTTPOnly#Browsers_Supporting_HttpOnly>
SESSION_COOKIE_HTTPONLY = True

# Debug Toolbar Settings
INTERNAL_IPS = (
    '127.0.0.1',
    '63.228.88.83',
    '209.181.77.56',
)

# Email Settings
EMAIL_LAYOUT = 'mail/base.html'
EMAIL_BACKEND = os.environ.get(
    'DJANGO_EMAIL_BACKEND',
    'django.core.mail.backends.smtp.EmailBackend',
)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = os.environ.get('EMAIL_PORT', '25')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS') == 'True'
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL') == 'True'

# PEP8 testing
TEST_PEP8_DIRS = [BASE_DIR]

TEST_PEP8_EXCLUDE = [
    'migrations',
]
TEST_PEP8_IGNORE = ['E501']
