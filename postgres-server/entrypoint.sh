#!/bin/bash

# postgres/entrypoint.sh

echo "Starting postgres server..."

docker-entrypoint.sh postgres &

echo "until postgres is ready"
until pg_isready -h localhost -p 5432
do
    echo "waiting for pg to start"
    sleep 5
done

echo "pg started"

psql -U user -d metastore -f /docker-entrypoint-initdb.d/hive-schema.sql

echo "Metastore initialized"

tail -f /dev/null


