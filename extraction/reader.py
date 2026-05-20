from pyspark.sql import SparkSession
from pyspark.sql.types import *


def get_spark():
    return SparkSession.builder \
        .appName("IMDB Project") \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.driver.memory", "4g") \
        .config("spark.executor.memory", "4g") \
        .getOrCreate()


def read_datasets(spark, data_path):
    title_basics_schema = StructType([
        StructField("tconst", StringType()),
        StructField("titleType", StringType()),
        StructField("primaryTitle", StringType()),
        StructField("originalTitle", StringType()),
        StructField("isAdult", StringType()),
        StructField("startYear", StringType()),
        StructField("endYear", StringType()),
        StructField("runtimeMinutes", StringType()),
        StructField("genres", StringType()),
    ])

    title_ratings_schema = StructType([
        StructField("tconst", StringType()),
        StructField("averageRating", DoubleType()),
        StructField("numVotes", IntegerType()),
    ])

    title_principals_schema = StructType([
        StructField("tconst", StringType()),
        StructField("ordering", IntegerType()),
        StructField("nconst", StringType()),
        StructField("category", StringType()),
        StructField("job", StringType()),
        StructField("characters", StringType()),
    ])

    name_basics_schema = StructType([
        StructField("nconst", StringType()),
        StructField("primaryName", StringType()),
        StructField("birthYear", StringType()),
        StructField("deathYear", StringType()),
        StructField("primaryProfession", StringType()),
        StructField("knownForTitles", StringType()),
    ])

    title_crew_schema = StructType([
        StructField("tconst", StringType()),
        StructField("directors", StringType()),
        StructField("writers", StringType()),
    ])

    options = {"sep": "\t", "header": "true", "nullValue": "\\N"}

    title_basics = spark.read.options(**options).schema(title_basics_schema).csv(f"{data_path}/title.basics.tsv")
    title_ratings = spark.read.options(**options).schema(title_ratings_schema).csv(f"{data_path}/title.ratings.tsv")
    title_principals = spark.read.options(**options).schema(title_principals_schema).csv(f"{data_path}/title.principals.tsv")
    name_basics = spark.read.options(**options).schema(name_basics_schema).csv(f"{data_path}/name.basics.tsv")
    title_crew = spark.read.options(**options).schema(title_crew_schema).csv(f"{data_path}/title.crew.tsv")

    return title_basics, title_ratings, title_principals, name_basics, title_crew
