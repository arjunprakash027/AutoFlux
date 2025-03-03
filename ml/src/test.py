from src import build_spark
#spark = builder.enableHiveSupport().getOrCreate()

spark = build_spark()

spark.sql("SELECT * FROM default_staging.stg_full limit 100;").show()
