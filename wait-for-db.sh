#!/bin/bash

# wait-for-db.sh
set -e

host="$1"
shift
cmd="$@"

until psql "postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$host/$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd
