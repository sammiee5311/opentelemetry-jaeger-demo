create-venv:
	python3 venv venv

install-venv:
	source venv/bin/activate &&\
		pip install -r requirements.txt

setup: create-venv install-venv

run-app:
	source venv/bin/activate &&\
		python app.py

run-docker:
	docker-compose up -d

run: run-docker run-app

stop:
	docker-compose down

all: setup run
