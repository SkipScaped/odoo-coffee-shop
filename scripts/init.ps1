$ErrorActionPreference = 'Stop'

if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host 'Created .env from .env.example'
}

docker compose --env-file .env up -d

docker compose --env-file .env exec -T odoo sh -c "python3 /mnt/scripts/init/init_db.py"

Write-Host ''
Write-Host 'Open: http://localhost:8069/web?db=coffee_shop'
Write-Host 'Login: admin / admin'
