from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = (
    SparkSession.builder
    .appName("PySparkWithStandaloneMetastore")
    .master("spark://spark-server:7077")
    .config("hive.metastore.uris", "thrift://spark-server:9083")  # Use the Metastore Service
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)


spark = configure_spark_with_delta_pip(builder).getOrCreate()

spark = builder.enableHiveSupport().getOrCreate()

print(spark.sql("SHOW DATABASES").show())
