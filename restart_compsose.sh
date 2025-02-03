docker-compose down --volumes

docker-compose build spark spark_worker

docker-compose up -d transformation