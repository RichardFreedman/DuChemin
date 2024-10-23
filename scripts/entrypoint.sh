#!/bin/bash

set -e

# Navigate to the project directory
cd /app

# Activate virtual environment (if you're using one)
# source venv/bin/activate

# Load data into the database
./load_data.sh

# Start the Django application using Gunicorn
gunicorn duchemin.wsgi:application --bind 0.0.0.0:8000