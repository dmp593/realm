#!/bin/bash

rm -rf db.sqlite3

# rm -rf houses/migrations/__pycache__
# rm -rf houses/migrations/0*.py

poetry run python manage.py setup_app -u admin -p secret
poetry run python manage.py runserver
