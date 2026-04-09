from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("IMDB Project") \
    .getOrCreate()

data = [("Alice", 25), ("Bob", 30), ("Carol", 22)]
df = spark.createDataFrame(data, ["name", "age"])
df.show()

spark.stop()