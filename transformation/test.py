from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = (
    SparkSession.builder
    .appName("RemoteSparkSession")
    .master("spark://spark-server:7077")  # Connect to remote Spark Master
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    #.config("spark.jars", ":///spark/jars/delta-core_2.12-2.2.0.jar,file:///spark/jars/delta-storage-2.2.0.jar")  # Ensure JARs are available
    #.config("spark.driver.host", "transformation")  # This is important for distributed execution
)


spark = configure_spark_with_delta_pip(builder).getOrCreate()

print("Spark Master:", spark.conf.get("spark.master"))
print("Loaded JARs:", spark.conf.get("spark.jars"))

# df = spark.range(10)
# df.show()


# # builder = SparkSession.builder \
# #     .appName("YourAppName") \
# #     .master("spark://spark-server:7077") \
# #     .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
# #     .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

# # spark = configure_spark_with_delta_pip(builder).getOrCreate()

# print("Warehouse Path:", spark.conf.get("spark.sql.warehouse.dir"))
# print("Catalog:", spark.conf.get("spark.sql.catalog.spark_catalog"))
# print("Loaded JARs:", spark.conf.get("spark.jars"))

schema_name = "default_source"
table_name = "column_description"

df = spark.read.format("delta").load(f"/spark-warehouse/{schema_name}.db/{table_name}")

df.show()
df.printSchema()
