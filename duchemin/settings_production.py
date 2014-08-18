DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'duchemin_webapp',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

#SOLR_SERVER = "http://duchemin-dev.haverford.edu:8080/duchemin-solr"
SOLR_SERVER = "http://localhost:8080/duchemin-solr/"
VEXF_SERVER = "http://duchemin-dev.haverford.edu:8080/notation"
