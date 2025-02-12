from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = (
    SparkSession.builder
    .appName("PySparkWithStandaloneMetastore")
    .master("spark://spark-server:7077")
    .config("spark.sql.warehouse.dir", "file:///spark-warehouse")
    .config("hive.metastore.uris", "thrift://metastore-db:9083")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .enableHiveSupport()
)


spark = configure_spark_with_delta_pip(builder).getOrCreate()

#spark = builder.enableHiveSupport().getOrCreate()

spark.sql("SELECT * FROM test limit 100;").show()
