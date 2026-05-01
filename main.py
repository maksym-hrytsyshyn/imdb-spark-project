from extraction.reader import get_spark, read_datasets
from preprocessing.preprocessor import (
    describe_dataset, cast_columns, numeric_stats,
    analyze_and_check_nulls, check_duplicates, handle_nulls
)

DATA_PATH = "/datasets"

spark = get_spark()

title_basics, title_ratings, title_principals, name_basics, title_crew = read_datasets(spark, DATA_PATH)

# 1. Загальна статистика
describe_dataset(title_basics, "title_basics")
describe_dataset(title_ratings, "title_ratings")

# 2. Привести до потрібних типів
title_basics = cast_columns(title_basics)

# 3. Числова статистика (після cast, щоб типи були правильні)
numeric_stats(title_basics, "title_basics")
numeric_stats(title_ratings, "title_ratings")

# 4. Аналіз інформативності + NULL аналіз
analyze_and_check_nulls(title_basics, "title_basics")
analyze_and_check_nulls(title_ratings, "title_ratings")

# 5. Дублікати
check_duplicates(title_basics, "title_basics")
check_duplicates(title_ratings, "title_ratings")

# 6. Обробка пропущених значень
title_basics = handle_nulls(title_basics)
analyze_and_check_nulls(title_basics, "title_basics after handling")

spark.stop()
