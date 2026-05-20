import sys
from extraction.reader import get_spark, read_datasets
from preprocessing.preprocessor import (
    describe_dataset, cast_columns, numeric_stats,
    analyze_and_check_nulls, check_duplicates, handle_nulls
)
from transformation.queries import (
    q1_rating_by_decade, q2_genre_quality_vs_popularity,
    q3_consistent_directors, q4_outstanding_films,
    q5_live_vs_voice_actors, q6_genre_best_films
)
from visualization.charts import (
    plot_q1_rating_by_decade, plot_q2_genre_quality,
    plot_q3_directors, plot_q4_outstanding,
    plot_q5_actors, plot_q6_treemap
)

DATA_PATH = "/datasets"
OUTPUT_PATH = "/output"

spark = get_spark()

title_basics, title_ratings, title_principals, name_basics, title_crew = read_datasets(spark, DATA_PATH)

# Preprocessing
describe_dataset(title_basics, "title_basics")
describe_dataset(title_ratings, "title_ratings")
title_basics = cast_columns(title_basics)
numeric_stats(title_basics, "title_basics")
numeric_stats(title_ratings, "title_ratings")
analyze_and_check_nulls(title_basics, "title_basics")
analyze_and_check_nulls(title_ratings, "title_ratings")
check_duplicates(title_basics, "title_basics")
check_duplicates(title_ratings, "title_ratings")
title_basics = handle_nulls(title_basics)


def save_explain(query, name, output_path):
    with open(f"{output_path}/explain_plans.txt", "a") as f:
        f.write(f"\n{'='*60}\n{name}\n{'='*60}\n")
        old_stdout = sys.stdout
        sys.stdout = f
        query.explain()
        sys.stdout = old_stdout


# Q1
print("\n=== Q1: Середній рейтинг фільмів по десятиліттях ===")
q1 = q1_rating_by_decade(title_basics, title_ratings)
save_explain(q1, "Q1", OUTPUT_PATH)
q1.show(20, truncate=False)
q1_pd = q1.toPandas()
plot_q1_rating_by_decade(q1_pd, OUTPUT_PATH)
q1.coalesce(1).write.mode("overwrite").option("header", True).csv(f"{OUTPUT_PATH}/q1_rating_by_decade")

# Q2
print("\n=== Q2: Якість vs популярність жанрів ===")
q2 = q2_genre_quality_vs_popularity(title_basics, title_ratings)
save_explain(q2, "Q2", OUTPUT_PATH)
q2.show(30, truncate=False)
q2_pd = q2.toPandas()
plot_q2_genre_quality(q2_pd, OUTPUT_PATH)
q2.coalesce(1).write.mode("overwrite").option("header", True).csv(f"{OUTPUT_PATH}/q2_genre_quality")

# Q3
print("\n=== Q3: Режисери з найвищим % якісних фільмів ===")
q3 = q3_consistent_directors(title_crew, title_basics, title_ratings, name_basics)
save_explain(q3, "Q3", OUTPUT_PATH)
q3.show(truncate=False)
q3_pd = q3.toPandas()
plot_q3_directors(q3_pd, OUTPUT_PATH)
q3.coalesce(1).write.mode("overwrite").option("header", True).csv(f"{OUTPUT_PATH}/q3_consistent_directors")

# Q4
print("\n=== Q4: Фільми що найбільше перевищують середній рейтинг жанру ===")
q4 = q4_outstanding_films(title_basics, title_ratings)
save_explain(q4, "Q4", OUTPUT_PATH)
q4.show(truncate=False)
q4_pd = q4.toPandas()
plot_q4_outstanding(q4_pd, OUTPUT_PATH)
q4.coalesce(1).write.mode("overwrite").option("header", True).csv(f"{OUTPUT_PATH}/q4_outstanding_films")

# Q5
print("\n=== Q5: Живі актори vs голосові актори ===")
q5 = q5_live_vs_voice_actors(title_principals, name_basics, title_ratings, title_basics)
save_explain(q5, "Q5", OUTPUT_PATH)
q5.show(20, truncate=False)
q5_pd = q5.toPandas()
plot_q5_actors(q5_pd, OUTPUT_PATH)
q5.coalesce(1).write.mode("overwrite").option("header", True).csv(f"{OUTPUT_PATH}/q5_live_vs_voice")

# Q6
print("\n=== Q6: Еталонний фільм кожного жанру ===")
q6 = q6_genre_best_films(title_basics, title_ratings)
save_explain(q6, "Q6", OUTPUT_PATH)
q6.show(30, truncate=False)
q6_pd = q6.toPandas()
plot_q6_treemap(q6_pd, OUTPUT_PATH)
q6.coalesce(1).write.mode("overwrite").option("header", True).csv(f"{OUTPUT_PATH}/q6_genre_best_films")

print("\nВсі результати збережено в /output/")
print("Графіки збережено як PNG в /output/")
spark.stop()
