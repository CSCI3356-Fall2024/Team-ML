#!/usr/bin/env bash
# Exit on error
set -o errexit

cd $(dirname "$0")

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip3 install -r requirements.txt

# Convert static asset files
python3 manage.py collectstatic --no-input

# Apply any outstanding database migrations
python3 manage.py migrate