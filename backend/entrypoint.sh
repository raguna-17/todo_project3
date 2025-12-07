#!/bin/sh
set -e

: "${POSTGRES_HOST:=db}"
: "${POSTGRES_PORT:=5432}"

echo "Waiting for postgres at ${POSTGRES_HOST}:${POSTGRES_PORT}..."

# 最大リトライ回数を設定する場合（例: 60回）
MAX_RETRIES=60
i=0
until nc -z "${POSTGRES_HOST}" "${POSTGRES_PORT}"; do
  i=$((i+1))
  if [ $i -ge $MAX_RETRIES ]; then
    echo "Postgres is still unavailable after $MAX_RETRIES attempts, exiting."
    exit 1
  fi
  echo "Postgres is unavailable - sleeping ($i/$MAX_RETRIES)"
  sleep 1
done

echo "Postgres is up - running migrations"
python manage.py migrate --noinput

exec "$@"

