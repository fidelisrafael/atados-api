# -*- coding: utf-8 -*-
# Django settings for atados project.
import os
import sys

PROJECT_ROOT = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))

DEBUG = os.environ.get('ATADOS_DEBUG', False)
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = (
  'atados.com.br',
)

ADMINS = (
    ('Rogério Yokomizo', 'me@ro.ger.io'),
    ('Marjori Pomarole', 'marjoripomarole@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('RDS_DB_NAME', 'atados'),
        'USER': os.environ.get('RDS_USERNAME', 'atados'),
        'PASSWORD': os.environ.get('RDS_PASSWORD', ''),
        'HOST': os.environ.get('RDS_HOSTNAME', 'localhost'),
        'PORT': os.environ.get('RDS_PORT', '3306'),
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
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '#7j@g*f*nufizr04s!f8_3+h&amp;1x!l04!q@0u@28ppkl)5kuy2^'

# List of callables that know how to import templates from various sources.
if DEBUG:
  TEMPLATE_LOADERS = (
      'django.template.loaders.filesystem.Loader',
      'django.template.loaders.app_directories.Loader',
      # 'django.template.loaders.eggs.Loader',
    )
else:
  TEMPLATE_LOADERS = (
      ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        # 'django.template.loaders.eggs.Loader',
      )),
  )

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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
    'grappelli', # needs to come before django.contrib.admin
    'django.contrib.admin',

    'haystack',
    'rest_framework',
    'facepy',
    'corsheaders',
    'south',
    'provider',
    'provider.oauth2',
    'django_nose',

    'atados_core',
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
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' if not DEBUG else 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('ATADOS_EMAIL_USER', 'marjori@atados.com.br')
EMAIL_HOST_PASSWORD = os.environ.get('ATADOS_EMAIL_PASSWORD', '')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

if not DEBUG: 
  DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

if all (var in os.environ for var in ('AWS_STORAGE_BUCKET_NAME',
                                      'AWS_ACCESS_KEY_ID',
                                      'AWS_SECRET_KEY')):
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    AWS_S3_SECURE_URLS = False
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
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 15

SOUTH_AUTO_FREEZE_APP = True

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache' if 'ATADOS_MEMCACHED_ENDPOINT' in os.environ else 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': os.environ.get('ATADOS_MEMCACHED_ENDPOINT', 'localhost:11211')
    },
}

if 'ATADOS_MEMCACHED_ENDPOINT' in os.environ:
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = 'atados'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
      'rest_framework.authentication.SessionAuthentication',
      'rest_framework.authentication.OAuth2Authentication'
    ),

    'DEFAULT_PARSER_CLASSES': (
      'rest_framework.parsers.JSONParser',
      'rest_framework.parsers.MultiPartParser',
    ),

    'PAGINATE_BY': 20,
    # Allow client to override, using `?page_size=xxx`.
    'PAGINATE_BY_PARAM': 'page_size',  
    'MAX_PAGINATE_BY': 100,

    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

CORS_ORIGIN_WHITELIST = (
    'atados.com.br',
    'atadoslocal.com.br'
)

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CSRF_COOKIE_DOMAIN = ".atadoslocal.com.br" if DEBUG else ".atados.com.br"
SESSION_COOKIE_DOMAIN = ".atadoslocal.com.br" if DEBUG else ".atados.com.br"

FACEBOOK_APP_ID = "307143646092582" #TODO: do I need this?
