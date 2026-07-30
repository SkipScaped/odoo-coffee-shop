import os
import sys
import time
import xmlrpc.client

host = os.environ.get("ODOO_INIT_HOST", "http://localhost:8069")
db = os.environ.get("ODOO_INIT_DB", "coffee_shop")
master_password = os.environ["ODOO_ADMIN_PASSWORD"]
admin_login = os.environ.get("ODOO_INIT_ADMIN_LOGIN", "admin")
admin_password = os.environ.get("ODOO_INIT_ADMIN_PASSWORD", "admin")
language = os.environ.get("ODOO_INIT_LANG", "en_US")
country_code = os.environ.get("ODOO_INIT_COUNTRY", "US")
phone = os.environ.get("ODOO_INIT_PHONE", "")
modules = [m.strip() for m in os.environ.get("ODOO_INIT_MODULES", "coffee_shop").split(",") if m.strip()]

common = xmlrpc.client.ServerProxy(f"{host}/xmlrpc/2/common")
db_service = xmlrpc.client.ServerProxy(f"{host}/xmlrpc/db")
object_service = xmlrpc.client.ServerProxy(f"{host}/xmlrpc/2/object")

for _ in range(30):
    try:
        version = common.version()
        if version:
            break
    except OSError:
        time.sleep(2)
else:
    print("Odoo did not become ready in time", file=sys.stderr)
    sys.exit(1)

existing_dbs = db_service.list()
if db not in existing_dbs:
    db_service.create_database(
        master_password,
        db,
        False,
        language,
        admin_password,
        admin_login,
        country_code,
        phone,
    )

uid = common.authenticate(db, admin_login, admin_password, {})
if not uid:
    print("Failed to authenticate after database creation", file=sys.stderr)
    sys.exit(1)

module_ids = object_service.execute_kw(
    db,
    uid,
    admin_password,
    "ir.module.module",
    "search",
    [[("name", "in", modules)]],
)

if module_ids:
    object_service.execute_kw(
        db,
        uid,
        admin_password,
        "ir.module.module",
        "button_immediate_install",
        [module_ids],
    )

print(f"Database '{db}' is ready and modules were requested: {', '.join(modules)}")
