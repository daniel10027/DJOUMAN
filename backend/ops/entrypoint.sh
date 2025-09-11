#!/usr/bin/env bash
set -euo pipefail

# Attendre Postgres
if [ -n "${DB_HOST:-}" ]; then
  echo "⏳ Attente de la base de données $DB_HOST:$DB_PORT..."
  until python - <<'PY'
import sys, os, psycopg2
host=os.getenv("DB_HOST"); port=os.getenv("DB_PORT","5432"); db=os.getenv("DB_NAME"); user=os.getenv("DB_USER"); pwd=os.getenv("DB_PASSWORD")
try:
    psycopg2.connect(host=host, port=port, dbname=db, user=user, password=pwd).close()
    print("✅ DB OK")
except Exception as e:
    print("DB KO:", e)
    sys.exit(1)
PY
  do sleep 2; done
fi

# Migrations (auto en local/staging, manuelles possibles en prod via env)
if [ "${MIGRATE_ON_START:-true}" = "true" ]; then
  echo "➡️  Migrate"
  python manage.py migrate --noinput
fi

# collectstatic (idempotent)
if [ "${COLLECT_STATIC:-true}" = "true" ]; then
  echo "➡️  collectstatic"
  python manage.py collectstatic --noinput
fi

exec "$@"
