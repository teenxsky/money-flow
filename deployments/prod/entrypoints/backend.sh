#!/bin/sh

poetry run python manage.py migrate
poetry run python manage.py load_reference
poetry run python manage.py collectstatic --no-input

exec "$@"
