# -*- coding: utf-8 -*-
# Django settings for atados project.
import os
import sys

PROJECT_ROOT = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))

if os.environ.get('ATADOS_ENV') == 'debug':
  DEBUG=True
  TEMPLATE_DEBUG=DEBUG
else:
  DEBUG=False
  TEMPLATE_DEBUG=DEBUG

# Settings for when developing on local computer
if os.environ.get('DJANGO_ENV') == 'development':
  DEVELOPMENT=True
else:
  DEVELOPMENT=False

if DEVELOPMENT:
  ALLOWED_HOSTS = (
    '.atadoslocal.com.br',
  )
else: 
  ALLOWED_HOSTS = (
    '.atados.com.br',
    '.portovoluntario.com.br'
  )

ADMINS = (
    ('Marjori Pomarole', 'marjori@atados.com.br')
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2' if 'ATADOS_DB_NAME' in os.environ else 'django.db.backends.sqlite3',
      'NAME': os.environ.get('ATADOS_DB_NAME', 'atados.sqlite'),
      'USER': os.environ.get('ATADOS_DB_USERNAME', ''),
      'PASSWORD': os.environ.get('ATADOS_DB_PASSWORD', ''),
      'HOST': os.environ.get('ATADOS_DB_HOSTNAME', ''),
      'PORT': os.environ.get('ATADOS_DB_PORT', ''),
    },
    'legacy': {                                                   
      'ENGINE': 'django.db.backends.mysql',                     
      'NAME': os.environ.get('LEGACY_DB_NAME', 'atados.sqlite'),
      'USER': os.environ.get('LEGACY_USERNAME', ''),            
      'PASSWORD': os.environ.get('LEGACY_PASSWORD', ''),        
      'HOST': os.environ.get('LEGACY_HOSTNAME', ''),            
      'PORT': os.environ.get('LEGACY_PORT', ''),                
    }                                                             
}

if 'test' in sys.argv:
  DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-BR'

LANGUAGES = (
    ('pt-BR', 'Português'),
    ('en-US', 'English'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.dirname(os.path.dirname(__file__)) + '/storage'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps's "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
      'django.template.loaders.filesystem.Loader',
      'django.template.loaders.app_directories.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
  'django.middleware.cache.UpdateCacheMiddleware',
  'django.middleware.cache.FetchFromCacheMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.gzip.GZipMiddleware',
  'django.middleware.http.ConditionalGetMiddleware',
  'corsheaders.middleware.CorsMiddleware',
  #'atados_core.middleware.ProfileMiddleware',
)

ROOT_URLCONF = 'atados.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'atados.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'grappelli.dashboard',
    'grappelli', # needs to come before django.contrib.admin
    'django.contrib.admin',

    'atados_core',
    'debug_toolbar',

    'haystack',
    'rest_framework',
    'facepy',
    'corsheaders',
    'south',
    'pyExcelerator',
    'provider',
    'provider.oauth2',
    'django_nose',
    'import_export',
    'djcelery',
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

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)

AUTH_USER_MODEL = 'atados_core.User'

HTTPS_SUPPORT = True

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' if not DEVELOPMENT else 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/atados-messages'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('ATADOS_EMAIL_USER', 'contato@atados.com.br')
EMAIL_HOST_PASSWORD = os.environ.get('ATADOS_EMAIL_PASSWORD', '')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

if all (var in os.environ for var in ('AWS_STORAGE_BUCKET_NAME',
                                      'AWS_ACCESS_KEY_ID',
                                      'AWS_SECRET_KEY')):
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    AWS_S3_SECURE_URLS = True
    AWS_S3_URL_PROTOCOL = 'https'
    AWS_HEADERS = {
        'Expires': 'Thu, 1 Dec 2015 00:00:01 GMT',
    }

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://%s/' % (os.environ.get('ATADOS_SEARCH_ENDPOINT', '127.0.0.1:9200')),
        'INDEX_NAME': 'haystack'
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

SOUTH_AUTO_FREEZE_APP = True

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': os.environ.get('ATADOS_MEMCACHED_ENDPOINT', 'localhost:11211')
    },
}
                                         
CACHE_MIDDLEWARE_SECONDS = 1200
CACHE_MIDDLEWARE_KEY_PREFIX = 'atados'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
      'rest_framework.authentication.SessionAuthentication',
      'rest_framework.authentication.OAuth2Authentication'
    ),

    'DEFAULT_PARSER_CLASSES': (
      'rest_framework.parsers.JSONParser',
      'rest_framework.parsers.MultiPartParser',
    ),

    'PAGINATE_BY': 8,
    # Allow client to override, using `?page_size=xxx`.
    'PAGINATE_BY_PARAM': 'page_size',  

    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

if DEVELOPMENT:
  CORS_ORIGIN_WHITELIST = (
    'atadoslocal.com.br',
  )
  
  CSRF_COOKIE_DOMAIN = ".atadoslocal.com.br"
  SESSION_COOKIE_DOMAIN = ".atadoslocal.com.br"
else:
  SESSION_COOKIE_DOMAIN = ".atados.com.br"
  CSRF_COOKIE_DOMAIN = ".atados.com.br"
  CORS_ORIGIN_WHITELIST = (
    'atados.com.br',
    'portovoluntario.com.br'
  )

PASSWORD_HASHERS = (
  'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher', # Drupal legacy sucks :(
  'django.contrib.auth.hashers.PBKDF2PasswordHasher'
)

GRAPPELLI_INDEX_DASHBOARD = 'atados_core.dashboard.AtadosDashboard'
EXPORT_RECORDS_LIMIT = 20000

import djcelery
djcelery.setup_loader()

BROKER_URL = 'amqp://guest@localhost:5672//'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Sao_Paulo'
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
