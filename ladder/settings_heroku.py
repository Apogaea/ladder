from settings_base import *  # NOQA

from ladder.settings_aws import *  # NOQA

DEBUG = False

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

import os

# S3 Storage Stuff
DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
DEFAULT_S3_PATH = "media"

STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
STATIC_S3_PATH = "static"

# Django Compressor
COMPRESS_ENABLED = True
COMPRESS_URL = STATIC_URL
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_STORAGE = STATICFILES_STORAGE

MEDIA_ROOT = "/{0}/".format(DEFAULT_S3_PATH)
MEDIA_URL = '//s3.amazonaws.com/{0}/media/'.format(AWS_STORAGE_BUCKET_NAME)

STATIC_ROOT = '/{0}/'.format(STATIC_S3_PATH)
STATIC_URL = COMPRESS_URL

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# Twilio credentials
TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE_NUMBER = '+12404282876'

if DEBUG is False:
    # Sanity check to be sure that we aren't running production without a
    # secure secret key.
    assert not SECRET_KEY == 'not-really-a-very-good-secret-key-now-is-it-so-set-a-better-one'

# Sendgrid Email settings
DEFAULT_FROM_EMAIL = 'app16920803@heroku.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']
