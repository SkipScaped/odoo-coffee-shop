#!/bin/sh
set -eu

docker compose --env-file .env up -d
