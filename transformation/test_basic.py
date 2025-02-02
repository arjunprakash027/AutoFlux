from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("TestBasicSpark") \
    .master("spark://spark-server:7077") \
    .config("spark.driver.memory", "1g") \
    .config("spark.executor.memory", "2g") \
    .config("spark.executor.memoryOverhead", "512m") \
    .config("spark.executor.cores", "1") \
    .config("spark.cores.max", "2") \
    .getOrCreate()

df = spark.range(10)
df.show()
