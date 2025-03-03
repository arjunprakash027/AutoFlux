"""
Author : Arjun P
"""

from pathlib import Path
from typing import List
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
import pandas as pd

def traverse_folder(dir:str) -> List:
    
    return [f"{dir}/{f.name}" for f in Path(dir).iterdir() if f.is_file()]

def ingest_spark(
        files: List
) -> None:
    builder = (
        SparkSession.builder
        .appName("PySparkWithStandaloneMetastore")
        .master("spark://spark-server:7077")
        .config("spark.sql.warehouse.dir", "file:///spark-warehouse")
        .config("spark.sql.catalogImplementation", "hive")
        .config("hive.metastore.uris", "thrift://metastore-db:9083")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .enableHiveSupport()
    )

    spark = configure_spark_with_delta_pip(builder).getOrCreate()

    # Spark expects schemas to be present before writing to it
    schema_name = "raw"
    spark.sql(f"CREATE DATABASE IF NOT EXISTS {schema_name}")

    for file in files:

        try:
            df = spark.read.csv(file, 
                                header=True, 
                                inferSchema=True
                                )

            table_name = f"{schema_name}.{file.split('/')[-1].split('.')[0]}"

            df.write.format("delta").mode("overwrite").saveAsTable(table_name)

            print(f"{table_name} table created in delta lake!")

        except Exception as e:
            print(e)
