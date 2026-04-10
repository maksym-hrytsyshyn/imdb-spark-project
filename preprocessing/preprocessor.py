from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType


def describe_dataset(df: DataFrame, name: str):
    print(f"\n=== {name} ===")
    print(f"Rows: {df.count()}, Columns: {len(df.columns)}")
    df.printSchema()
    df.show(5)


def numeric_stats(df: DataFrame, name: str):
    print(f"\n=== Numeric stats: {name} ===")
    df.describe().show()


def cast_columns(title_basics: DataFrame) -> DataFrame:
    return title_basics \
        .withColumn("startYear", F.expr("try_cast(startYear AS INT)")) \
        .withColumn("endYear", F.expr("try_cast(endYear AS INT)")) \
        .withColumn("runtimeMinutes", F.expr("try_cast(runtimeMinutes AS INT)")) \
        .withColumn("isAdult", F.when(F.col("isAdult") == "1", True).when(F.col("isAdult") == "0", False).otherwise(None))

def drop_uninformative(title_basics: DataFrame) -> DataFrame:
    return title_basics.drop("endYear")


def check_nulls(df: DataFrame, name: str):
    print(f"\n=== Nulls in {name} ===")
    df.select([
        F.count(F.when(F.col(c).isNull(), c)).alias(c)
        for c in df.columns
    ]).show()


def check_duplicates(df: DataFrame, name: str):
    total = df.count()
    distinct = df.distinct().count()
    print(f"\n=== Duplicates in {name} ===")
    print(f"Total: {total}, Distinct: {distinct}, Duplicates: {total - distinct}")