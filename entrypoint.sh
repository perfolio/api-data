#!/bin/sh

set -eu

poetry run ./manage.py makemigrations
poetry run ./manage.py migrate

poetry run uvicorn --host 0.0.0.0 api.asgi:application
