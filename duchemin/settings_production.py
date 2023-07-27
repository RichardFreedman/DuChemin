import os
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}


#SOLR_SERVER = "http://duchemin-dev.haverford.edu:8080/duchemin-solr"
SOLR_SERVER = "http://solr:8080/duchemin-solr/"
# VEXF_SERVER = "http://localhost:8080/notation"
