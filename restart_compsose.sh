docker-compose down

docker-compose build spark spark_worker metastore-db

docker-compose up -d transformation