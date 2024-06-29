#!/bin/bash

rm -rf db.sqlite3

rm -rf houses/migrations/__pycache__
rm -rf houses/migrations/0*.py

poetry run python manage.py makemigrations
poetry run python manage.py setupapp -u admin -p secret

poetry run python manage.py runserver
