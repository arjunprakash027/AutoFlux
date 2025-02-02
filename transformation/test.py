from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = (
    SparkSession.builder.appName("MyApp")
    .config("spark.master", "spark://spark-server:7077")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.2.0,io.delta:delta-storage:2.2.0")
)

spark = configure_spark_with_delta_pip(builder).getOrCreate()


# builder = SparkSession.builder \
#     .appName("YourAppName") \
#     .master("spark://spark-server:7077") \
#     .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
#     .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

# spark = configure_spark_with_delta_pip(builder).getOrCreate()

print("Warehouse Path:", spark.conf.get("spark.sql.warehouse.dir"))
print("Catalog:", spark.conf.get("spark.sql.catalog.spark_catalog"))
print("Loaded JARs:", spark.conf.get("spark.jars"))

schema_name = "source"
table_name = "column_description"

df = spark.read.format("delta").load(f"/spark-warehouse/{schema_name}.db/{table_name}")

# df.show()
# df.printSchema()
