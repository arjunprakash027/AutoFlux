from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = (
    SparkSession.builder
    .appName("RemoteSparkSession")
    .master("spark://spark-server:7077")  # Connect to remote Spark Master
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.hadoop.hive.metastore.uris", "thrift://spark-server:9083")
    .config("spark.sql.warehouse.dir", "/spark-warehouse")
    .config("spark.sql.hive.thriftServer.singleSession", "true")
    .config("javax.jdo.option.ConnectionURL", "jdbc:derby:;databaseName=metastore_db;create=true")

    #.config("spark.driver.host", "spark-server")
    #.config("spark.jars", ":///spark/jars/delta-core_2.12-2.2.0.jar,file:///spark/jars/delta-storage-2.2.0.jar")  # Ensure JARs are available
    #.config("spark.driver.host", "transformation")  # This is important for distributed execution
)


spark = configure_spark_with_delta_pip(builder).getOrCreate()

print("Spark Master:", spark.conf.get("spark.master"))
print("Loaded JARs:", spark.conf.get("spark.jars"))


schema_name = "default_source"
table_name = "column_description"

spark.sql(f"CREATE DATABASE IF NOT EXISTS {schema_name}")
spark.sql(
    f"CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} USING DELTA LOCATION '/spark-warehouse/{schema_name}/{table_name}'"
)

print(spark.sql(f"SHOW TABLES IN {schema_name}").show())
# df = spark.read.format("delta").table(f"{schema_name}.{table_name}")

# df.show()
# df.printSchema()
