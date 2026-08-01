# Odoo 17 Coffee Shop Setup

A clean, local-first Odoo 17 template for a small coffee shop business.

It includes:
- Docker Compose setup for `odoo` and `postgres`
- persistent Docker volumes for the database and filestore
- a custom `coffee_shop` addon with POS categories, starter products, and basic inventory-friendly setup
- helper commands for starting, stopping, logging, and resetting the stack
- an automated Docker-based database initializer so users do not need local Python setup

## What you get

The seeded coffee shop module includes:
- a starter POS configuration: `Main Counter`
- drinks, pastries, and retail products
- POS categories for coffee shop items
- product categories, tags, and a simple product classification field
- real product photos bundled inside the addon for every seeded product
- Pakistan-based company defaults with PKR currency
- a bundled coffee shop logo asset inside the addon

---

## Requirements

Before you start, make sure you have:

- Windows 10 or Windows 11
- Docker Desktop installed and running
- Docker Compose available through Docker Desktop
- PowerShell, Command Prompt, or Git Bash
- `make` is optional; if you do not have it, you can use the raw Docker commands shown below

---

## Project structure

```text
.
├── addons/
│   └── coffee_shop/
│       ├── data/
│       ├── models/
│       ├── security/
│       ├── views/
│       ├── static/
│       ├── __init__.py
│       ├── __manifest__.py
│       └── README.md
├── config/
│   └── odoo.conf.template
├── scripts/
│   └── init/
│       └── init_db.py
├── .env.example
├── docker-compose.yml
├── Makefile
└── README.md
```

---

## Windows installation guide

### Option A: Fastest install with Docker

If you want the easiest Windows path, use the included PowerShell script:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\init.ps1
```

That script:
- creates `.env` if missing
- starts Docker services
- creates the `coffee_shop` database
- installs the custom addon
- prints the final login URL
- please clone the repo first and go to
```cmd
cd odoo-coffee-shop
```
- & then paste the cmd.

Or follow the manual steps below if you prefer.

### 1. Clone the repository

```powershell
git clone https://github.com/SkipScaped/odoo-coffee-shop.git
cd odoo-coffee-shop
```

Important: after cloning from GitHub, the folder name will usually be `odoo-coffee-shop`, not `Odoo-Fix`.

### 2. Create the environment file

In PowerShell:

```powershell
Copy-Item .env.example .env
```

In Command Prompt:

```cmd
copy .env.example .env
```

Then open `.env` and update at least these values:
- `POSTGRES_PASSWORD`
- `ODOO_DB_PASSWORD`
- `ODOO_ADMIN_PASSWORD`

These must stay aligned:
- `POSTGRES_USER` must match `ODOO_DB_USER`
- `POSTGRES_PASSWORD` must match `ODOO_DB_PASSWORD`

### 3. Start Docker services

If you have `make`:

```powershell
make up
```

If you do not have `make`:

```powershell
docker compose --env-file .env up -d
```

### 4. Initialize the database automatically

If you have `make`:

```powershell
make init-db
```

If you do not have `make`:

```powershell
docker compose --env-file .env exec -T odoo sh -c "python3 /mnt/scripts/init/init_db.py"
```

This step is what creates the `coffee_shop` database and installs the custom module.

The initializer runs inside the Odoo container and uses the environment values already loaded from `.env`.

### 5. Open Odoo

Open:

```text
http://localhost:8069/web?db=coffee_shop
```

### 6. Log in

Use:
- **Email:** `admin`
- **Password:** `admin`

If Odoo asks for the **master password** for database management, use the value from `.env`:
- `ODOO_ADMIN_PASSWORD`

### 7. Open the POS

After login:
1. Go to **Point of Sale**
2. Open **Main Counter**
3. Start a session

---

## Why Odoo may show "Create Database" after clone

This is normal if you only run Docker and do not run the initializer yet.

Why it happens:
- Docker starts Odoo and PostgreSQL
- but Odoo does **not** automatically create a business database on its own
- the actual business database is created by the `init-db` step

So if someone clones the repo and only runs:

```powershell
docker compose --env-file .env up -d
```

then Odoo may still open on the database creation screen.

### The fix
Run the initializer:

```powershell
make init-db
```

or:

```powershell
docker compose --env-file .env exec -T odoo sh -c "python3 /mnt/scripts/init/init_db.py"
```

After that, open:

```text
http://localhost:8069/web?db=coffee_shop
```

---

## One-command-style local flow

For a clean local install after cloning, you can run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\init.ps1
```

Manual equivalent:

```powershell
Copy-Item .env.example .env
docker compose --env-file .env up -d
docker compose --env-file .env exec -T odoo sh -c "python3 /mnt/scripts/init/init_db.py"
```

Then open:

```text
http://localhost:8069/web?db=coffee_shop
```

Login with:
- **Email:** `admin`
- **Password:** `admin`

---

## Seeded products

Examples include:
- Espresso
- Americano
- Cappuccino
- Latte
- Mocha
- Iced Latte
- Hot Tea
- Orange Juice
- Butter Croissant
- Blueberry Muffin
- Chocolate Chip Cookie
- Banana Bread Slice
- Granola Parfait
- House Blend Beans 250g
- Reusable Tumbler

Every seeded product ships with a real product photo bundled inside the addon at `addons/coffee_shop/static/img/products/`. When the module is installed, the photos are stored on the `image_1920` field of each product.

Product photos are sourced from [Unsplash](https://unsplash.com) and are free to use under the [Unsplash License](https://unsplash.com/license).

---

## Common commands

With `make`:

```sh
make init-env
make up
make down
make logs
make init-db
make reset-db
```

Without `make`:

```powershell
docker compose --env-file .env up -d
docker compose --env-file .env down
docker compose --env-file .env logs -f odoo db
docker compose --env-file .env exec -T odoo sh -c "python3 /mnt/scripts/init/init_db.py"
docker compose --env-file .env down -v
```

---

## Troubleshooting

### 1. `.env` is missing or Docker says `key cannot contain a space`

Fix:

```powershell
Copy-Item .env.example .env
```

If Docker still says:

```text
failed to read .env: line 1: key cannot contain a space
```

then your local `.env` file was copied from a bad or older version. Delete it, recreate it, and make sure line 1 starts exactly like this with no spaces before the key:

```text
COMPOSE_PROJECT_NAME=coffee-shop-odoo
```

Fast reset:

```powershell
Remove-Item .env
Copy-Item .env.example .env
```

### 2. Ports are already in use

If `8069` or `5432` is busy, edit `.env`:

```text
ODOO_PORT=8070
POSTGRES_PORT=5433
```

Then restart:

```powershell
docker compose --env-file .env down
docker compose --env-file .env up -d
```

### 3. Wrong login/password

Use this exact URL:

```text
http://localhost:8069/web?db=coffee_shop
```

Then log in with:
- **Email:** `admin`
- **Password:** `admin`

If it still fails:

```powershell
docker compose --env-file .env down -v
docker compose --env-file .env up -d
docker compose --env-file .env exec -T odoo sh -c "python3 /mnt/scripts/init/init_db.py"
```

### 4. Docker is running but Odoo still shows Create Database

That means the app stack is running, but the `coffee_shop` database has not been initialized yet.

Run:

```powershell
docker compose --env-file .env exec -T odoo sh -c "python3 /mnt/scripts/init/init_db.py"
```

### 5. `make init-db` or Docker init fails with `KeyError: 'ODOO_ADMIN_PASSWORD'`

This means the running Odoo container was started before the latest environment values were available inside the service definition.

Fix it with a clean recreate:

```powershell
docker compose --env-file .env down
docker compose --env-file .env up -d --force-recreate
docker compose --env-file .env exec -T odoo sh -c "python3 /mnt/scripts/init/init_db.py"
```

That recreates the container with the required environment values available to the init script.

### 6. Containers keep restarting

Check logs:

```powershell
docker compose --env-file .env logs -f odoo db
```

Then verify:
- Docker Desktop is running
- `.env` exists
- ports are free
- DB credentials match

### 7. Guaranteed clean recovery flow

If someone gets stuck, this is the safest recovery path:

```powershell
docker compose --env-file .env down -v
Copy-Item .env.example .env
docker compose --env-file .env up -d
docker compose --env-file .env exec -T odoo sh -c "python3 /mnt/scripts/init/init_db.py"
```

Then open:

```text
http://localhost:8069/web?db=coffee_shop
```

---

## Notes for GitHub upload

Commit these:
- `docker-compose.yml`
- `README.md`
- `.env.example`
- `addons/coffee_shop/...`
- `scripts/...`
- `Makefile`
- `.gitignore`
- `.dockerignore`
- `.gitattributes`
- `LICENSE`

Do not commit:
- `.env`
- local IDE files
- Docker data

---

## Summary

Fastest Windows flow:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\init.ps1
```

Then open:

```text
http://localhost:8069/web?db=coffee_shop
```

Login with:
- **Email:** `admin`
- **Password:** `admin`
