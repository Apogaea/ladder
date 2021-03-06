# Django settings for ladder project.
import os
import excavator
import django_cache_url
import dj_database_url
import pytz
import datetime


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ADMINS = (
    ('Piper', 'pipermerriam@gmail.com'),
)

DEFAULT_FROM_EMAIL = excavator.env_string(
    'DJANGO_DEFAULT_FROM_EMAIL', default='ladder@apogaea.com',
)

MANAGERS = ADMINS

DEBUG = TEMPATE_DEBUG = excavator.env_bool('DJANGO_DEBUG', default=False)

# Allowed Hosts
ALLOWED_HOSTS = excavator.env_list('DJANGO_ALLOWED_HOSTS', required=not DEBUG)


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

SITE_ID = int(excavator.env_string('DJANGO_SITE_ID', default=1))

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# File Storage
DEFAULT_FILE_STORAGE = excavator.env_string(
    'DJANGO_DEFAULT_FILE_STORAGE',
    default='django.core.files.storage.FileSystemStorage',
)
STATICFILES_STORAGE = excavator.env_string(
    'DJANGO_STATICFILES_STORAGE',
    default='django.contrib.staticfiles.storage.StaticFilesStorage',
)

# User-uploaded files
MEDIA_ROOT = excavator.env_string('DJANGO_MEDIA_ROOT')
MEDIA_URL = excavator.env_string('DJANGO_MEDIA_URL', default='/media/')

# Static files
STATIC_ROOT = excavator.env_string('DJANGO_STATIC_ROOT')
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
    'pipeline.finders.PipelineFinder',
)

# Django Pipeline Settings
PIPELINE_DISABLE_WRAPPER = excavator.env_bool(
    'DJANGO_PIPELINE_DISABLE_WRAPPER', default=True,
)
PIPELINE_ENABLED = excavator.env_bool('DJANGO_PIPELINE_ENABLED', default=not DEBUG)
PIPELINE_CSS = {
    'base': {
        'source_filenames': (
            "css/bootstrap.css",
            "css/bootstrap-responsive.css",
            "css/bootstrap-black.css",
            "css/ladder.css",
        ),
        'output_filename': 'base.css',
    },
}

PIPELINE_JS = {
    'base': {
        'source_filenames': (
            "js/jquery-2.1.0.js",
            "js/underscore-1.6.0.js",
            "js/handlebars.js",
            "js/backbone.js",
            "js/bootstrap.js",
            "js/ladder.js",
        ),
        'output_filename': 'base.js',
    },
    'rollbar': {
        'source_filenames': (
            "js/rollbar.js",
        ),
        'output_filename': 'js/rollbar.js',
    },
}
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.NoopCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.NoopCompressor'

# Production installs need to have this environment variable set
SECRET_KEY = excavator.env_string('DJANGO_SECRET_KEY', required=True)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'ladder.apps.accounts.middleware.LogoutIfInactiveMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'ladder.apps.exchange.context_processors.exchange_stats',
    'ladder.core.context_processors.rollbar',
)
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "ladder", "templates"),
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

# Registration Window
REGISTRATION_OPEN_DATE = datetime.datetime(
    year=2016, month=3, day=21, hour=11, tzinfo=pytz.timezone(TIME_ZONE),
)
REGISTRATION_CLOSE_DATE = datetime.datetime(
    year=2016, month=5, day=30, hour=0, tzinfo=pytz.timezone(TIME_ZONE),
)

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ladder.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Main App
    'ladder.core',

    # Project Apps
    'ladder.apps.accounts',
    'ladder.apps.exchange',

    # 3rd Party
    'pipeline',
    'storages',
    'authtools',
    'argonauts',
    's3_folder_storage',
    'bootstrap3',
    'manifesto',
]

try:
    # Sentry error reporting.
    import raven  # NOQA
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')
    RAVEN_CONFIG = {
        'dsn': excavator.env_string('SENTRY_DSN', default=None)
    }
except ImportError:
    pass


if DEBUG:
    try:
        import django_extensions  # NOQA
        INSTALLED_APPS.append('django_extensions')
    except ImportError:
        pass
    try:
        import debug_toolbar  # NOQA
        INSTALLED_APPS.append('debug_toolbar')
    except ImportError:
        pass

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
AWS_ACCESS_KEY_ID = excavator.env_string('AWS_ACCESS_KEY_ID', default=None)
AWS_SECRET_ACCESS_KEY = excavator.env_string('AWS_SECRET_ACCESS_KEY', default=None)
AWS_STORAGE_BUCKET_NAME = excavator.env_string('AWS_STORAGE_BUCKET_NAME', default=None)

DEFAULT_S3_PATH = "media"
STATIC_S3_PATH = "static"

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
if 'MEMCACHIER_SERVERS' in os.environ:
    # Special case for memcachier on heroku.
    os.environ.setdefault('MEMCACHE_USERNAME', os.environ.get('MEMCACHIER_USERNAME'))
    os.environ.setdefault('MEMCACHE_PASSWORD', os.environ.get('MEMCACHIER_PASSWORD'))
    os.environ.setdefault(
        'CACHE_URL',
        'djangopylibmc://{0}'.format(os.environ['MEMCACHIER_SERVERS']),
    )

CACHES = {
    'default': django_cache_url.config(),
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# used cached template loader
# TODO: bad for dev.
if DEBUG:
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )
else:
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )

# Rollbar
# https://rollbar.com/
try:
    import rollbar  # NOQA
    MIDDLEWARE_CLASSES.append('rollbar.contrib.django.middleware.RollbarNotifierMiddleware')

    ROLLBAR = {
        'access_token': excavator.env_string('ROLLBAR_ACCESS_TOKEN', default=None),
        'environment': excavator.env_string('ROLLBAR_ENVIRONMENT', default='development'),
        'branch': excavator.env_string('ROLLBAR_GIT_BRANCH', default='master'),
        'root': BASE_DIR,
    }
except ImportError:
    pass

# django-rest-framework configuration.
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissions',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    # -- Global Pagination --
    # Default to 10
    'PAGINATE_BY': 10,
    # Allow client to override, using `?page_size=xxx`.
    'PAGINATE_BY_PARAM': 'page_size',
    # Maximum limit allowed when using `?page_size=xxx`.
    'MAX_PAGINATE_BY': 100,
}

# =============
# Debug Toolbar
# =============

# Implicit setup can often lead to problems with circular imports, so we
# explicitly wire up the toolbar
DEBUG_TOOLBAR_PATCH_SETTINGS = False
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    # https://github.com/django-debug-toolbar/django-debug-toolbar/pull/674
    # 'debug_toolbar.panels.templates.TemplatesPanel',
    'template_timings_panel.panels.TemplateTimings.TemplateTimings',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]


# This is required to silence `1_6.W001` system check.
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
