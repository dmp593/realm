#!/bin/bash

rm -rf db.sqlite3

rm -rf houses/migrations/__pycache__
rm -rf houses/migrations/0*.py

poetry run python manage.py makemigrations
poetry run python manage.py migrate

poetry run python manage.py loaddata auth/users

poetry run python manage.py loaddata houses/countries
poetry run python manage.py loaddata houses/districts
poetry run python manage.py loaddata houses/municipalities
poetry run python manage.py loaddata houses/parishes
poetry run python manage.py loaddata houses/locales

poetry run python manage.py loaddata houses/conditions
poetry run python manage.py loaddata houses/types
poetry run python manage.py loaddata houses/typologies
poetry run python manage.py loaddata houses/energies-cerficates

# poetry run python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@realm.earth', 'secret', first_name='Alcina', last_name='Roque')"

poetry run python manage.py runserver
