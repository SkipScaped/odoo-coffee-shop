ENV_FILE ?= .env
COMPOSE = docker compose --env-file $(ENV_FILE)

.PHONY: up down logs reset-db init-env init-db

init-env:
	cp .env.example .env

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f odoo db

init-db:
	python scripts/init/init_db.py

reset-db:
	$(COMPOSE) down -v
