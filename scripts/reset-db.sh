#!/bin/sh
set -eu

# Drops named volumes so Odoo and PostgreSQL start from a clean state.
docker compose --env-file .env down -v
