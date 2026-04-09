from extraction.reader import get_spark, read_datasets

DATA_PATH = "/datasets"

spark = get_spark()

title_basics, title_ratings, title_principals, name_basics, title_crew = read_datasets(spark, DATA_PATH)

print("=== title_basics ===")
title_basics.show(5)
print(f"Rows: {title_basics.count()}")

print("=== title_ratings ===")
title_ratings.show(5)

spark.stop()