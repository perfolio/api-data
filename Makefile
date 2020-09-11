.ONESHELL:

test:
	poetry run src/manage.py test src/

format:
	poetry run black .

type:
	poetry run mypy src
