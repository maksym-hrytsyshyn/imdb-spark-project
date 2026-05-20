from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def describe_dataset(df: DataFrame, name: str):
    print(f"\n=== {name} ===")
    print(f"Rows: {df.count()}, Columns: {len(df.columns)}")
    df.printSchema()
    df.show(5)


def cast_columns(title_basics: DataFrame) -> DataFrame:
    return title_basics \
        .withColumn("startYear", F.expr("try_cast(startYear AS INT)")) \
        .withColumn("endYear", F.expr("try_cast(endYear AS INT)")) \
        .withColumn("runtimeMinutes", F.expr("try_cast(runtimeMinutes AS INT)")) \
        .withColumn("isAdult", F.when(F.col("isAdult") == "1", True)
                                .when(F.col("isAdult") == "0", False)
                                .otherwise(None))


def numeric_stats(df: DataFrame, name: str):
    print(f"\n=== Numeric stats: {name} ===")
    numeric_cols = [f.name for f in df.schema.fields
                    if str(f.dataType) in ("IntegerType()", "DoubleType()", "BooleanType()")]
    if numeric_cols:
        df.select(numeric_cols).describe().show()
    else:
        print("No numeric columns found")


def analyze_and_check_nulls(df: DataFrame, name: str):
    print(f"\n=== Null analysis: {name} ===")
    total = df.count()
    null_counts = df.select([
        F.count(F.when(F.col(c).isNull(), c)).alias(c)
        for c in df.columns
    ]).collect()[0]

    for col in df.columns:
        null_count = null_counts[col]
        null_pct = round(null_count / total * 100, 2)
        decision = ""
        if col == "endYear":
            decision = "→ залишаємо: NULL за визначенням для не-серіалів"
        elif col == "runtimeMinutes":
            decision = "→ залишаємо NULL: відсутність значима (серіали, ігри)"
        elif col == "genres":
            decision = "→ залишаємо NULL: не видаляємо щоб не втрачати дані"
        elif col == "startYear":
            decision = "→ залишаємо NULL: історичні дані можуть бути відсутні"
        elif col == "isAdult":
            decision = "→ заповнимо False"
        elif col == "primaryTitle":
            decision = "→ видалимо рядки: без назви запис беззмістовний"
        print(f"  {col}: {null_count} nulls ({null_pct}%) {decision}")


def check_duplicates(df: DataFrame, name: str):
    total = df.count()
    distinct = df.select("tconst").distinct().count()
    print(f"\n=== Duplicates in {name} ===")
    print(f"Total: {total}, Distinct by tconst: {distinct}, Duplicates: {total - distinct}")


def handle_nulls(title_basics: DataFrame) -> DataFrame:
    print("\n=== Handling nulls ===")
    result = title_basics \
        .fillna({"isAdult": False}) \
        .filter(F.col("primaryTitle").isNotNull())
    print(f"Rows after null handling: {result.count()}")
    return result
