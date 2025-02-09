#!/bin/bash
# spark/entrypoint.sh

# Start Spark Master
/spark/sbin/start-master.sh \
    -h 0.0.0.0 \
    --port 7077 \
    --webui-port 8080

# wait for postgres
echo "Waiting for hive metastore server to start..."
until nc -z -v -w30 metastore-db 9083
do
    echo "Waiting hive connection..."
    sleep 5
done
echo "Postgres started"

# Start Thrift Server with limited resources
/spark/sbin/start-thriftserver.sh \
    --master "spark://spark-server:7077" \
    --hiveconf hive.server2.thrift.port=10000 \
    --hiveconf hive.server2.thrift.bind.host=0.0.0.0 \
    --hiveconf hive.metastore.uris=thrift://metastore-db:9083 \
    --conf spark.sql.warehouse.dir=file:///spark-warehouse \
    --conf spark.sql.catalogImplementation=hive \
    --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
    --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog \
    --conf spark.driver.host=spark-server \
    --conf spark.driver.bindAddress=0.0.0.0 \
    --hiveconf hive.server2.transport.mode=binary \
    --hiveconf hive.server2.authentication=NOSASL \
    --conf spark.sql.hive.thriftServer.singleSession=true \
    --conf spark.sql.hive.metastore.jars=builtin \
    --conf spark.driver.memory=1g \
    --conf spark.driver.cores=2 \
    --conf spark.executor.cores=2 \
    --conf spark.executor.memory=1g \
    --conf spark.executor.instances=1 \
    --conf spark.cores.max=2 \
    --conf spark.dynamicAllocation.enabled=false

# Keep container alive
tail -f /dev/null