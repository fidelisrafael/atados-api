# -*- coding: utf-8 -*-
# Django settings for atados project.
import os

AWS_EB = []
if 'PARAM1' in os.environ:
    import json
    def decode_param1(data):
        return dict([(key.encode('utf-8'), value) for key, value in data.iteritems()])
    AWS_EB = json.loads(os.environ['PARAM1'], object_hook=decode_param1)

DEBUG = False if 'debug' in AWS_EB and not AWS_EB['debug'] else True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = (
    'beta.atados.com.br',
    'www.atados.com.br',
)

ADMINS = (
    ('Rogério Yokomizo', 'me@ro.ger.io'),
)

MANAGERS = ADMINS

if 'RDS_HOSTNAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'atados.sqlite',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-BR'

LANGUAGES = (
    ('en-US', 'English'),
    ('pt-BR', 'Português'),
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
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
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
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'atados.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'atados.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.markup',
    'flatblocks',
    'atados_core',
    'atados_nonprofit',
    'atados_volunteer',
    'atados_project',
    'atados_legacy',
    'registration',
    'bootstrap_toolkit',
    'south',
    'sorl.thumbnail',
    'haystack',
    'django_nose',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
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
    'atados_core.backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = "/"

HTTPS_SUPPORT = True

ACCOUNT_ACTIVATION_DAYS = 7

LOGIN_URL = '/sign-in'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "atados_core.context_processors.site",
    "atados_nonprofit.context_processors.nonprofit",
    "atados_volunteer.context_processors.volunteer",
)

if all(var in AWS_EB for var in('email_user', 'email_password')):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = AWS_EB['email_user']
    EMAIL_HOST_PASSWORD = AWS_EB['email_password']
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = 'no-reply@atados.com.br'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'no-reply@atados.com.br'

THUMBNAIL_DEBUG = DEBUG

# Drupal legacy sucks :/
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
)


if all (var in os.environ for var in ('AWS_STORAGE_BUCKET_NAME',
                                      'AWS_ACCESS_KEY_ID',
                                      'AWS_SECRET_KEY')):
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    AWS_S3_SECURE_URLS = False
    AWS_HEADERS = {
        'Expires': 'Thu, 1 Dec 2015 00:00:01 GMT',
    }

"""HAYSTACK_SITECONF = 'atados.search_indexes'

if '_solr_endpoint' in AWS_EB:
    HAYSTACK_SOLR_URL = 'http://%s/solr' % (AWS_EB['solr_endpoint'])
    HAYSTACK_SEARCH_ENGINE = 'atados_core.search'
else:
    HAYSTACK_SEARCH_ENGINE = 'simple'"""

if 'solr_endpoint' in AWS_EB:
    HAYSTACK_CONNECTIONS = {
            'default': {
                #'ENGINE': 'atados_core.search_backend.SearchEngine',
                'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
                'URL': 'http://%s/solr' % (AWS_EB['solr_endpoint']),
                },
            }
else:
    HAYSTACK_CONNECTIONS = {
            'default': {
                'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
                },
            }

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

HAYSTACK_SEARCH_RESULTS_PER_PAGE = 15

SOUTH_AUTO_FREEZE_APP = True

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

if 'memcached_endpoint' in AWS_EB:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': AWS_EB['memcached_endpoint']
        },
    }

    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        },
    }

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = 'atados'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

if 'facebook_application_id' in AWS_EB:
    AUTHENTICATION_BACKENDS =  ('social_auth.backends.facebook.FacebookBackend',) + AUTHENTICATION_BACKENDS
    INSTALLED_APPS = INSTALLED_APPS + ('social_auth',)
    FACEBOOK_APP_ID = AWS_EB['facebook_application_id']
    FACEBOOK_API_SECRET = AWS_EB['facebook_application_secret']
