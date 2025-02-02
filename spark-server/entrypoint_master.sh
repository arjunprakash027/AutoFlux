#!/bin/bash
# spark/entrypoint.sh

# Start Spark Master
/spark/sbin/start-master.sh \
    -h 0.0.0.0 \
    --port 7077 \
    --webui-port 8080

# Start Thrift Server with Delta config
/spark/sbin/start-thriftserver.sh \
    --master "spark://spark-server:7077" \
    --hiveconf hive.server2.thrift.port=10000 \
    --hiveconf hive.server2.thrift.bind.host=0.0.0.0 \
    --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
    --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog \
    --conf spark.driver.host=spark-server \
    --conf spark.driver.bindAddress=0.0.0.0 \
    --hiveconf hive.server2.transport.mode=binary \
    --hiveconf hive.server2.authentication=NOSASL \
    --conf spark.sql.hive.thriftServer.singleSession=true

# Keep container alive
tail -f /dev/null