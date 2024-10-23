import os

# Should be not be True for production
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    '127.0.0.1',
    'django',
    'django_app',
    '.haverford.edu',
    '.digitalduchemin.org',
]

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE':   'django.db.backends.postgresql',
        # FIXME: These need to be changed from the default values and the username/password need to come from a secret (and synched with the values in docker-compose)
        'NAME':     'postgres',
        'USER':     'postgres',
        'PASSWORD': 'postgres',
        'HOST':     'db',                       # Set to empty string for localhost. Not used with sqlite3.
        'PORT':     '5432',                     # Set to empty string for default. Not used with sqlite3.
    }
}


#SOLR_SERVER = "http://duchemin-dev.haverford.edu:8080/duchemin-solr"
SOLR_SERVER = "http://solr:8080/duchemin-solr/"
# VEXF_SERVER = "http://localhost:8080/notation"
