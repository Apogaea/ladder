from settings_base import *  # NOQA

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Amazon S3 Stuff
AWS_ACCESS_KEY_ID = 'AKIAIQ3JWY6YCMRCXPDA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'apo-ladder'

# S3 Storage Stuff
DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
DEFAULT_S3_PATH = "media"

STATICFILES_STORAGE = 's3_folder_storage.s3.DefaultStorage'
STATIC_S3_PATH = "static"

MEDIA_ROOT = "/{0}/".format(DEFAULT_S3_PATH)
MEDIA_URL = '//s3.amazonaws.com/{0}/media/'.format(AWS_STORAGE_BUCKET_NAME)

STATIC_ROOT = '/{0}/'.format(STATIC_S3_PATH)
COMPRESS_URL = '//s3.amazonaws.com/{0}/'.format(AWS_STORAGE_BUCKET_NAME)
STATIC_URL = COMPRESS_URL

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
