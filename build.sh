#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip3 install -r requirements.txt

cd /opt/render/project/src/HTeamML/mysite

# Convert static asset files
python3 manage.py collectstatic --no-input

# Apply any outstanding database migrations
python3 manage.py migrate && python3 manage.py createsuperuser --no-input ||
echo "Superuser already exists"
