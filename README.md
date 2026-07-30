# Odoo 17 Coffee Shop Setup

A clean, local-first Odoo 17 template for a small coffee shop business.

It includes:
- Docker Compose setup for `odoo` and `postgres`
- persistent Docker volumes for the database and filestore
- a custom `coffee_shop` addon with POS categories, starter products, and basic inventory-friendly setup
- helper commands for starting, stopping, logging, and resetting the stack

## What you get

The seeded coffee shop module includes:
- a starter POS configuration: `Main Counter`
- drinks, pastries, and retail products
- POS categories for coffee shop items
- product categories, tags, and a simple product classification field
- Pakistan-based company defaults with PKR currency
- a bundled coffee shop logo asset inside the addon

---

## Requirements

Before you start, make sure you have:

- Docker Desktop installed
- Docker Compose available
- `make` available in your shell, or use the scripts in `scripts/`

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
│       ├── __init__.py
│       ├── __manifest__.py
│       └── README.md
├── config/
│   └── odoo.conf.template
├── scripts/
├── .env.example
├── docker-compose.yml
├── Makefile
└── README.md
```

---

## Step-by-step local setup

### 1. Clone the repository

```sh
git clone https://github.com/SkipScaped/odoo-coffee-shop.git
cd Odoo-Fix
```

If you already downloaded the folder, just open it in your terminal.

### 2. Create your local environment file

Copy the example file:

```sh
cp .env.example .env
```

Then open `.env` and update these values:

- `POSTGRES_PASSWORD`
- `ODOO_DB_PASSWORD`
- `ODOO_ADMIN_PASSWORD`

Important:
- `POSTGRES_USER` must match `ODOO_DB_USER`
- `POSTGRES_PASSWORD` must match `ODOO_DB_PASSWORD`

The repository keeps secrets out of Git by using `.env` locally and committing only `.env.example`.

### 3. Start the containers

Using `make`:

```sh
make up
```

Or using the shell script:

```sh
sh scripts/up.sh
```

This starts:
- PostgreSQL
- Odoo 17 Community

### 4. Create the database and install the module

The easiest option is the automated setup:

```sh
make init-db
```

That creates the `coffee_shop` database and installs the `coffee_shop` addon automatically.

By default, the automated setup now creates the database with Pakistan as the country context, and the addon sets the main company currency to PKR.

### 5. Open Odoo in your browser

Go to:

```text
http://localhost:8069/web?db=coffee_shop
```

Using the `?db=coffee_shop` part helps avoid logging into the wrong database if you have more than one.

### 6. Log in

Use these credentials:

- **Email:** `admin`
- **Password:** `admin`

If you are asked for the **master password** during database management, use the value from `.env`:

- `ODOO_ADMIN_PASSWORD`

If you are using the local setup I created during testing, that value is:

- `odoo_master_dev_password`

### 7. Open the POS

After logging in:

1. Go to **Point of Sale**
2. Open **Main Counter**
3. Start a session
4. You should see the seeded coffee shop items in the POS screen

---

## Manual setup option

If you do **not** want to use `make init-db`, you can do it manually.

1. Open:
   - `http://localhost:8069`
2. Create a new database with:
   - **Master Password:** value of `ODOO_ADMIN_PASSWORD` from `.env`
   - **Database Name:** `coffee_shop`
   - **Email:** `admin`
   - **Password:** `admin`
3. Log in
4. Install the `Coffee Shop Setup` app if needed

---

## Seeded products

The template includes a larger sample menu so the system feels usable right away.

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

---

## Inventory behavior

The starter products are created as `consu` products.

This keeps the setup simple for local use while still allowing products to appear in Odoo sales, POS, and inventory-related flows. If you want strict stock valuation later, you can convert selected items into storable products.

---

## Common commands

```sh
make init-env   # copy .env.example to .env
make up         # start Odoo and PostgreSQL
make down       # stop containers
make logs       # show service logs
make init-db    # create the coffee_shop database and install the addon
make reset-db   # remove containers and Docker volumes
```

Equivalent scripts are available in `scripts/`.

---

## Logs and troubleshooting

### Show logs

```sh
make logs
```

### Reset everything and start fresh

```sh
make reset-db
make up
make init-db
```

This fully removes:
- PostgreSQL data
- Odoo filestore data

### Common first-run problems and fixes

#### 1. `.env` file is missing

Symptom:
- Docker Compose says a variable is missing
- services fail to start correctly

Fix:

```sh
cp .env.example .env
```

Then open `.env` and make sure these values exist:
- `POSTGRES_PASSWORD`
- `ODOO_DB_PASSWORD`
- `ODOO_ADMIN_PASSWORD`

Also make sure these pairs match:
- `POSTGRES_USER` = `ODOO_DB_USER`
- `POSTGRES_PASSWORD` = `ODOO_DB_PASSWORD`

#### 2. Port `8069` or `5432` is already in use

Symptom:
- Docker fails with a port binding error
- Odoo or PostgreSQL does not start

Fix:
Edit `.env` and change one or both ports:

```text
ODOO_PORT=8070
POSTGRES_PORT=5433
```

Then restart:

```sh
make down
make up
```

If you change `ODOO_PORT`, open Odoo using that new port in the browser.

#### 3. Odoo starts but login fails

Symptom:
- `Wrong login/password`
- Odoo opens but rejects `admin`

Fix:
Use this exact URL:

```text
http://localhost:8069/web?db=coffee_shop
```

Then log in with:
- **Email:** `admin`
- **Password:** `admin`

If that still fails, recreate the database cleanly:

```sh
make reset-db
make up
make init-db
```

#### 4. Odoo opens the wrong database screen

Symptom:
- You see the database manager or another database login page
- Odoo is not using `coffee_shop`

Fix:
Open this exact URL:

```text
http://localhost:8069/web?db=coffee_shop
```

That forces Odoo to use the expected database.

#### 5. `make init-db` fails

Symptom:
- database init script fails
- Odoo may not be ready yet
- local Python does not see the `.env` values

Fix:
First make sure the containers are up:

```sh
make up
make logs
```

Wait until Odoo shows it is serving HTTP requests, then try again:

```sh
make init-db
```

If your shell does not export `.env` variables cleanly for Python, run the manual fallback:

```sh
set -a && . ./.env && python scripts/init/init_db.py
```

#### 6. Docker starts, but the containers keep restarting

Symptom:
- `docker compose ps` shows restarting containers
- Odoo or Postgres never becomes healthy

Fix:
Check logs first:

```sh
make logs
```

Then verify:
- `.env` exists
- DB credentials match correctly
- the ports are free
- Docker Desktop is fully running

If needed, wipe everything and start clean:

```sh
make reset-db
make up
make init-db
```

#### 7. Changes to addon data are not reflected

Symptom:
- you updated XML data but Odoo still shows old values

Fix:
For a clean local demo, the easiest path is:

```sh
make reset-db
make up
make init-db
```

That guarantees the latest module data is loaded into a fresh database.

#### 8. Windows shell command differences

Symptom:
- `cp` does not work in your terminal

Fix:
Use one of these alternatives:

PowerShell:

```powershell
Copy-Item .env.example .env
```

Command Prompt:

```cmd
copy .env.example .env
```

Or just create `.env` manually by duplicating `.env.example`.

#### 9. Docker Compose says the repository is cloned but startup still fails

Fix checklist:
- Docker Desktop is running
- `.env` exists
- no port conflicts on `8069` and `5432`
- you ran `make up` before `make init-db`
- you open `http://localhost:8069/web?db=coffee_shop`

### Safe recovery flow

If a user gets stuck and just wants a guaranteed clean retry, this is the shortest reliable recovery path:

```sh
make reset-db
cp .env.example .env
make up
make init-db
```

Then open:

```text
http://localhost:8069/web?db=coffee_shop
```

Login with:
- **Email:** `admin`
- **Password:** `admin`

---

## Notes for GitHub upload

This project is ready to publish as a Git repository.

Recommended files to commit:
- `docker-compose.yml`
- `README.md`
- `.env.example`
- `addons/coffee_shop/...`
- `Makefile`
- `scripts/...`
- `.gitignore`
- `.dockerignore`
- `.gitattributes`
- `LICENSE`

Do **not** commit:
- `.env`
- local IDE settings
- container data

---

## 30-second presentation script

You can explain the project like this:

> This is a fully containerized Odoo 17 Community setup for a small coffee shop.
> It runs with Docker Compose using Odoo and PostgreSQL, keeps data persistent,
> and includes a custom addon with preloaded POS categories, products, and a
> starter counter configuration. I also localized the template for Pakistan by
> setting the company country to Pakistan and the default currency to PKR, so
> it feels closer to a real business starter kit instead of just a demo install.

## Summary

If you want the fastest path, the install flow is:

```sh
cp .env.example .env
make up
make init-db
```

Then open:

```text
http://localhost:8069/web?db=coffee_shop
```

Login with:
- **Email:** `admin`
- **Password:** `admin`
