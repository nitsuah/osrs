# Makefile for osrs: Docker, test, coverage, lint, build

.PHONY: all test coverage lint build docker-test docker-build

all: test

test:
	pytest -c config/pytest.ini --rootdir=.

coverage:
	pytest -c config/pytest.ini --rootdir=. --cov

lint:
	flake8 --config config/.flake8 .

build:
	pyinstaller --onefile -n osrs-bot bot/core.py

docker-test:
	docker build --no-cache -t osrs-test:py .
	docker run --rm osrs-test:py xvfb-run -a /opt/venv/bin/python -m pytest -c config/pytest.ini --rootdir=. --cov

docker-build:
	docker build -t osrs:latest .
