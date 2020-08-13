.ONESHELL:

migrate: makemigrations
	cd api
	python manage.py migrate

makemigrations:
	cd api
	python manage.py makemigrations


run:
	cd api
	python manage.py runserver