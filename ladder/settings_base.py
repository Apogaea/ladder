# Django settings for ladder project.
import os
import socket
import re

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

HOST_NAME = socket.gethostname()

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}


ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'sqlite_database',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

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
MEDIA_ROOT = os.path.join(PROJECT_PATH, '..', 'media')
MEDIA_URL = '/media/'

# Static files
STATIC_ROOT = os.path.join(PROJECT_PATH, '..', "static")
STATIC_URL = '/static/'
# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'public'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'compressor.finders.CompressorFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Secret key generation that is the same as django uses in startproject.
from django.utils.crypto import get_random_string


def generate_secret_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return get_random_string(50, chars)

# Generate secret key file that is unique for each installation.  This way we
# don't have to worry about having the key in github.
try:
    from secret_key import SECRET_KEY
except ImportError:
    SETTINGS_DIR = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(SETTINGS_DIR, 'secret_key.py'), 'w') as secret_key_file:
        secret_key_file.write("SECRET_KEY = '{0}'".format(generate_secret_key()))

    from secret_key import SECRET_KEY  # NOQA

#SECRET_KEY = '9p=xzq1kk(h(4mpxag(^&amp;i=hf#4zt3#!)06ofd%8y@@g+5o+&amp;c'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
  # 'fusionbox.middleware.GenericTemplateFinderMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'ladder.urls'

# Twilio
# These codes should be eithe set in an untracked settings file.
#TWILIO_ACCOUNT_SID =
#TWILIO_AUTH_TOKEN =

TWILIO_CODE_MAX_ATTEMPTS = 3
TWILIO_CODE_EXPIRE_MINUTES = 60 * 24
TWILIO_RESEND_MINUTES = 60

# Activation Code

ACTIVATION_CODE_LENGTH = 6

# The name that google displays in the 'allow authentication' screen
GOOGLE_DISPLAY_NAME = 'Apogaea Ticket Exchange'

GOOGLE_OAUTH2_CLIENT_ID = '312201970433.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'WxEGK5b5-TQlzdMx1ykBCyci'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/account/'
LOGIN_ERROR_URL = '/login-error/'

SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/account/edit/'

SOCIAL_AUTH_CREATE_USERS = True

SOCIAL_AUTH_USER_MODEL = 'accounts.User'
AUTH_USER_MODEL = 'accounts.User'

DEFAULT_ACCEPT_TIME = 2 * 24 * 60 * 60

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ladder.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    # Toolbox
    'debug_toolbar',
    'compressor',
    'fusionbox',
    'south',
    'django_extensions',
    'storages',
    's3_folder_storage',
    'authtools',

    # Project Apps
    'accounts',
    'exchange',
    'ladder',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

SEND_BROKEN_LINK_EMAILS = True

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

EMAIL_LAYOUT = 'mail/base.html'

IGNORABLE_404_URLS = (
    re.compile(r'\.(php|cgi)$'),
    re.compile(r'/null/?$'),  # This could be being caused by us.  Investigate?
    re.compile(r'^/phpmyadmin/', re.IGNORECASE),
    re.compile(r'^/wp-admin/'),
    re.compile(r'^/cgi-bin/'),
    re.compile(r'^(?!/static/).*\.(css|js)/?$'),
)

try:
    from settings_local import *  # NOQA
except ImportError:
    pass

DATABASE_ENGINE = DATABASES['default']['ENGINE']

# This must go _after_ the cache backends are configured, which could be in
# local settings

if not DEBUG:
    # if not `running in runserver` would be a better condition here
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
    )
