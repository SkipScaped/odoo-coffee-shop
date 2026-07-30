#!/bin/sh
set -eu

docker compose --env-file .env logs -f odoo db
