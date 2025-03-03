from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

_spark = None

def build_spark() -> SparkSession:
    global _spark
    
    if _spark is None:

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

        _spark = configure_spark_with_delta_pip(builder).getOrCreate()
    
    return _spark