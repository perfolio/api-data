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

get-terraform:
	curl -o terraform.zip https://releases.hashicorp.com/terraform/0.12.19/terraform_0.12.19_linux_amd64.zip
	unzip -o terraform.zip
	rm terraform.zip