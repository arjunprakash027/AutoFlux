docker-compose down
docker-compose build spark spark_worker metastore-db transformation ml
docker-compose up -d ml