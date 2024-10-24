.DEFAULT_GOAL := all

NAME := ${AWS_ECR_ACCOUNT_URL}/${NAMESPACE}/${APP_NAME}
TAG := latest
REPLICA_COUNT := 1
IMG := ${NAME}
LATEST := ${NAME}:${TAG}
HELM_ARGS := --set image.repository=${NAME},image.tag=${TAG},app.node_env=${APP_ENV},replicaCount=${REPLICA_COUNT}

# Push built image to ECR
.PHONY: push
push: build
	@echo "Pushing image"
	@echo ""
	@docker push ${LATEST}

# Login to ECR
.PHONY: login
login:
	docker login -u AWS -p ${PASS} ${AWS_ECR_ACCOUNT_URL}

# Build and tag image
.PHONY: build
build:
	@echo "Building and tagging image"
	@docker build -t ${IMG} .
	@docker tag ${IMG} ${LATEST}

# Deploy to k8s cluster via helm
.PHONY: deploy
deploy:
	@echo "Installing app in K8s cluster"
	@helm repo add tvl ${CHART_URL}
	@helm repo update
	@helm upgrade ${APP_NAME} tvl/${APP_NAME} --install --debug ${HELM_ARGS} --namespace ${APP_ENV}

# Clean deployment resources
.PHONY: clean
clean: 
	@echo "Cleaning up workspace"
	@rm -f ./kubeconfig

deploy-local:
	@echo "Installing app in K8s cluster"
	@helm install ${APP_NAME} ./charts  --debug ${HELM_ARGS} --namespace ${APP_ENV}

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
	@echo "Starting randomiser on port ${PORT}..."
	uvicorn src.randomiser_service.main:app --reload --port ${PORT}
else
	@echo "Starting randomiser on default port 8000"
	uvicorn src.randomiser_service.main:app --reload
endif

start-api:
ifdef PORT
	@echo "Starting api on port ${PORT}..."
	uvicorn src.benchmark_service.main:app --reload --port ${PORT}
else
	@echo "Starting api on port 8001"
	uvicorn src.benchmark_service.main:app --reload --port 8001
endif

help:
	@echo "Available commands"
	@echo "  make migrate    		- Run all migrations"
	@echo "  make migration-down    - Undo the latest migration"
	@echo "  make migration  		- Create a migration"
	@echo "  make lint           	- Lint all files"
	@echo "  make install           - Install packages"
	@echo "  make tests   			- Run tests
	@echo "  make start-randomiser  - Start randomiser service"
	@echo "  make start-api  		- Start api service"
