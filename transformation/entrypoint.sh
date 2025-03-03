#!/bin/bash
# Run the dbt processes in entry

echo "Running deps"
dbt deps

until nc -zv -w30 spark-server 10000
do
    echo "Waiting for spark server to start..."
    sleep 5
done

# Pulling the data from kaggle using python
python ingestion

# Seeding data
echo "Running Seed"
dbt seed

echo "Data Loaded"
# dbt run

# echo "Transformation Done!"

# Keep the container hanging
exec tail -f /dev/null

