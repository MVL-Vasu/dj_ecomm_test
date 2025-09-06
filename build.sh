#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations to create tables
python manage.py migrate

# Load initial data from fixture
# python manage.py loaddata all_data.json
