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

hive --service metastore --hiveconf hive.metastore.uris=thrift://0.0.0.0:9083

tail -f /dev/null


