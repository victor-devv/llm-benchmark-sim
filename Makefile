.DEFAULT_GOAL := all

install:
	@echo "Installing dependencies"
	poetry install

toml_sort:
	toml-sort pyproject.toml --all --in-place

isort:
	poetry run isort .

black:
	poetry run black .

flake8:
	poetry run flake8 .

pylint:
	poetry run pylint src

mypy:
	poetry run mypy --install-types --non-interactive .

test:
	poetry run pytest

lint: toml_sort isort black flake8 mypy

tests: test

all: lint tests

migrate:
	@echo "Running migrations"
	alembic upgrade head

migrate-down:
	@echo "Reverting latest migration"
	alembic downgrade -1

migration:
	@echo "Creating migrations"
ifdef MANUAL
	# Manual migrations
	@echo "Manual migrations"
	alembic revision -m "$(MSG)"
else
	# Autogenerate migrations
	@echo "Autogenerate migrations $(MSG)"
	alembic revision --autogenerate -m "$(MSG)"
endif

start-randomiser:
ifdef PORT
	@echo "Starting app on port ${PORT}..."
	uvicorn src.randomiser_service.main:app --reload --port ${PORT}
else
	@echo "Starting app on port 8000..."
	uvicorn src.randomiser_service.main:app --reload
endif

help:
	@echo "Available commands"
	@echo "  make migrate    		- Run all migrations"
	@echo "  make migration-down    - Undo the latest migration"
	@echo "  make migration  		- Create a migration"
	@echo "  make lint           	- Lint all files"
	@echo "  make install           - Install packages"
	@echo "  make tests   			- Run tests
	@echo "  make start   			- Start app"
