.ONESHELL:

test:
	poetry run coverage run --branch --source='src/' src/manage.py test src/ && poetry run coverage report --fail-under=50

format:
	poetry run black .

type:
	poetry run mypy src

setup:
	poetry install && poetry run pre-commit install

get_poetry:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
