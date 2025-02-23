docker-compose down

if [ "$1" == "no-transformation" ]; then
    echo "Building without transformation"
    docker-compose build spark spark_worker metastore-db ml
else
    echo "Building with transformation"
    docker-compose build spark spark_worker metastore-db transformation ml
    docker-compose up -d transformation
fi

docker-compose up -d ml