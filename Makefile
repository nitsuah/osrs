# Makefile for osrs: Docker, test, coverage, lint, build

.PHONY: all test coverage lint build docker-test docker-build

all: test

test:
	pytest

coverage:
	pytest --cov

lint:
	flake8 .

build:
	pyinstaller --onefile -n osrs-bot bot/core.py

docker-test:
	docker build --no-cache -t osrs-test:py .
	docker run --rm -it osrs-test:py /opt/venv/bin/python -m pytest --cov

docker-build:
	docker build -t osrs:latest .
