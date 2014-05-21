# Django settings for access_web project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('Andrea Biancini', 'andrea.biancini@garr.it'),
    ('Marco Malavolti', 'marco.malavolti@garr.it'),
)

MANAGERS = ADMINS

BASE_DIR = os.path.dirname(os.path.realpath(__file__)) 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',   # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'django',                       # Or path to database file if using sqlite3.
        'USER': 'django',                       # Not used with sqlite3.
        'PASSWORD': 'ciaodjango',               # Not used with sqlite3.
        'HOST': 'localhost',                    # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                         # Set to empty string for default. Not used with sqlite3.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Rome'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'it-it'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

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
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '9uqo5d00h-l0a45!a6fq*e$y+lxw3&^34-#%18z4ci5^s1t3=o'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'oidc_django.middleware.OpenIdMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'djangomako.middleware.MakoMiddleware',
)

#SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

#SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#    }
#}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'oidc_django.backends.OpenIdUserBackend',
)

LOGIN_URL = '/openid'

ROOT_URLCONF = 'django_rp.urls'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'oic.utils.webfinger': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'oic.utils.keyio': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'oic.oauth2.message': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
	},
        'oidc_django.oidc': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
	},
    }
}
