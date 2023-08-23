#!/bin/bash

set -e

# Start Solr service using the provided command
# cd /app/solr/
# mvn tomcat:run-war &


# Wait for Solr to start (adjust this delay as needed)
# sleep 10
# cd ..
python manage.py makemigrations
python manage.py migrate
# Apply migrations and run the Django development server
# python manage.py loaddata /app/duchemin/data/duchemin_dcperson.json
# python manage.py loaddata /app/duchemin/data/duchemin_dcbook.json
# python manage.py loaddata /app/duchemin/data/duchemin_dccontentblock.json
# python manage.py loaddata /app/duchemin/data/duchemin_dcpiece.json
# python manage.py loaddata /app/duchemin/data/duchemin_dcreconstruction.json
# python manage.py loaddata /app/duchemin/data/duchemin_dcphrase.json
# python manage.py loaddata /app/duchemin/data/duchemin_dcanalysis.json
# python manage.py loaddata /app/duchemin/data/duchemin_dcnote.json


#python manage.py runserver 0.0.0.0:8000
gunicorn duchemin.wsgi:application --bind 0.0.0.0:8000