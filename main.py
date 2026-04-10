from extraction.reader import get_spark, read_datasets
from preprocessing.preprocessor import (
    describe_dataset, numeric_stats, cast_columns,
    drop_uninformative, check_nulls, check_duplicates
)

DATA_PATH = "/datasets"

spark = get_spark()

title_basics, title_ratings, title_principals, name_basics, title_crew = read_datasets(spark, DATA_PATH)

describe_dataset(title_basics, "title_basics")
describe_dataset(title_ratings, "title_ratings")

numeric_stats(title_ratings, "title_ratings")
numeric_stats(title_basics, "title_basics")

title_basics = cast_columns(title_basics)

title_basics = drop_uninformative(title_basics)

check_nulls(title_basics, "title_basics")
check_nulls(title_ratings, "title_ratings")

check_duplicates(title_basics, "title_basics")
check_duplicates(title_ratings, "title_ratings")

spark.stop()