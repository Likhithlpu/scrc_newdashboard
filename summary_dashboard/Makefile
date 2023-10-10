run:
	python smart_city_dashboard/manage.py runserver

db:
	docker-compose -f services/postgres/postgres.yaml up -d

mig:
	python smart_city_dashboard/manage.py makemigrations
	python smart_city_dashboard/manage.py migrate

up:
	docker-compose up --build -d

down:
	docker-compose down --remove-orphans

restart:
	make up
m:
	docker run --name postgisSmart \
	 -p 5432:5432 \
	 -e POSTGRES_PASSWORD=smart_city@admin_password \
	 -e POSTGRES_USER=smartcityadmin \
	 -e POSTGRES_DB=smartcitydb \
	 -d postgis/postgis
