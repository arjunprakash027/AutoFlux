docker-compose down

if [ "$1" == "no-transformation" ]; then
    echo "Building without transformation"
    docker-compose build ml
else
    echo "Building with transformation"
    docker-compose build transformation ml
    docker-compose up -d transformation
fi

docker-compose up -d ml