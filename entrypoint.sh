#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
  echo "Waiting for postgres to start"

  while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
    sleep 0.1
  done

  echo "Postgres is running"
fi

#python manage.py flush --no-input
#python manage.py migrate

exec "$@"
