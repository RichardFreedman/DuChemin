# Django settings for duchemin project.
import os
from .settings_production import *

DEBUG = True  # Should be not be True for production
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    '127.0.0.1',
    '.haverford.edu',
    '.digitalduchemin.org',
    '*'
]

PROJECT_DIR = os.path.dirname(__file__)

ADMINS = (
    # ('Edgar Leon', 'eleon@haverford.edu'),
)

ADMIN_EMAIL = 'admin@digitalduchemin.org'

MANAGERS = ADMINS

AUTH_PROFILE_MODULE = "duchemin.DCUserProfile"
LOGIN_URL = '/login/'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

DATE_FORMAT = 'Y-m-d'

TIME_FORMAT = 'H:m'

DATETIME_FORMAT = 'Y-m-d, H:m'

SHORT_DATETIME_FORMAT = 'Y-m-d, H:m'

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Make it acceptable for users to leave off a slash in URLs
APPEND_SLASH = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = 'uploads/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

MEI_ROOT = os.path.join(PROJECT_DIR, 'uploads/mei')

MP3_ROOT = os.path.join(PROJECT_DIR, 'uploads/audio')

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

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
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '-bpbyo7m3d0rsvek5qrh2$3862(2#t4yoe3wc6341r)6z256i9'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
            # Always use forward slashes, even on Windows.
            # Don't forget to use absolute paths, not relative paths.
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
            
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.request",
                "django.template.context_processors.debug",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.csrf",
                "django.contrib.messages.context_processors.messages",
                "duchemin.context_processors.admin_email",
            ],
        },
    },
]


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware'
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'duchemin.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'duchemin.wsgi.application'


INSTALLED_APPS = (

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    # Uncomment the next line to enable the admin:
    'duchemin',
    'django.contrib.admin',
    'bootstrap_pagination',
    'django_extensions',
    #'south',
    'crispy_forms',
    'rest_framework',
    'rest_framework.authtoken'
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)


SOLR_CONNECTIONS = {
    'default': {
        'URL': 'http://solr:8080/duchemin-solr',
        'COLLECTION': 'name',
        'CONFIGSET': '_default'
    }
}



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

CRISPY_TEMPLATE_PACK = "bootstrap"

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



SOLR_NUM_SEARCH_RESULTS = 10

SOLR_FACET_FIELDS = [
    'contributor',
    'composer',
    'is_cadence',
    'cadence_final_tone',
    'cadence_alter',
    'cadence_kind',
    'text_treatment',
    'repeat_kind',
    'book_id_title',
    'book_title'
]

# The mapping between the search form parameters and the
# Solr fields.
SEARCH_PARAM_MAP = {
    'q': 'q',
    'b': 'book_id',
    'p': 'composer',
    'r': 'contributor',
    'f': 'cadence_final_tone',
    'k': 'cadence_kind',
    'm': 'cadence_alter',
    't': 'text_treatment',
    'lf': 'repeat_kind',
    'cadence_role_cantz': 'cadence_role_cantz',
    'cadence_role_tenz': 'cadence_role_tenz',
    'intpatt_other': 'other_formulas',
    'intpatt_p6_up': 'voices_p6_up',
    'intpatt_p6_lo': 'voices_p6_lo',
    'intpatt_p3_up': 'voices_p3_up',
    'intpatt_p3_lo': 'voices_p3_lo',
    'intpatt_53_up': 'voices_53_up',
    'intpatt_53_lo': 'voices_53_lo',
    'prestype_nim_up1': 'voice_role_up1_nim',
    'prestype_nim_lo1': 'voice_role_lo1_nim',
    'prestype_nim_up2': 'voice_role_up2_nim',
    'prestype_nim_lo2': 'voice_role_lo2_nim',
    'prestype_free_dux': 'voice_role_dux1',
    'prestype_free_comes': 'voice_role_com1',
    'prestype_imduet_dux1': 'voice_role_dux1',
    'prestype_imduet_comes1': 'voice_role_com1',
    'prestype_imduet_dux2': 'voice_role_dux2',
    'prestype_imduet_comes2': 'voice_role_com2',

    'prestype_entry_p_dux1': 'voice_role_dux1',
    'prestype_entry_p_comes1': 'voice_role_com1',
    'prestype_entry_p_dux2': 'voice_role_dux2',
    'prestype_entry_p_comes2': 'voice_role_com2',

    'prestype_entry_t_dux1': 'voice_role_dux1',
    'prestype_entry_t_comes1': 'voice_role_com1',
    'prestype_entry_t_dux2': 'voice_role_dux2',
    'prestype_entry_t_comes2': 'voice_role_com2',

    'prestype_entry_s_dux1': 'voice_role_dux1',
    'prestype_entry_s_comes1': 'voice_role_com1',
    'prestype_entry_s_dux2': 'voice_role_dux2',
    'prestype_entry_s_comes2': 'voice_role_com2',
}

DISPLAY_FACETS = {
    'composer': ("p", "Composer"),
    'contributor': ("r", "Analyst"),
    'cadence_final_tone': ("f", "Cadence Final Tone"),
    'cadence_kind': ("k", "Cadence Kind"),
    'cadence_alter': ("m", "Cadence Alter"),
    'repeat_kind': ("lf", "Repeat Kind"),
    'book_id_title': ("b", "Book Title"),
    'text_treatment': ("t", "Text Treatment")
}
