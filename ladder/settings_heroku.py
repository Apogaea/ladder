from settings_base import *  # NOQA

DEBUG = False

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

import os
# Amazon S3 Stuff
# These values should be set as environment variables for Heroku.
AWS_ACCESS_KEY_ID = os.environ.setdefault("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.setdefault("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = 'apo-ladder'

# S3 Storage Stuff
DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
DEFAULT_S3_PATH = "media"

STATICFILES_STORAGE = 's3_folder_storage.s3.DefaultStorage'
STATIC_S3_PATH = "static"

MEDIA_ROOT = "/{0}/".format(DEFAULT_S3_PATH)
MEDIA_URL = '//s3.amazonaws.com/{0}/media/'.format(AWS_STORAGE_BUCKET_NAME)

STATIC_ROOT = '/{0}/'.format(STATIC_S3_PATH)
STATIC_URL = COMPRESS_URL

# Django Compressor
COMPRESS_ENABLED = True
COMPRESS_URL = '//s3.amazonaws.com/{0}/'.format(AWS_STORAGE_BUCKET_NAME)
#COMPRESS_ROOT = STATIC_ROOT
COMPRESS_STORAGE = STATICFILES_STORAGE

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# Twilio credentials
TWILIO_ACCOUNT_SID = os.environ.setdefault("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.setdefault("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = '+12404282876'
