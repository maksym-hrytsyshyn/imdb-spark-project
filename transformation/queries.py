from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def q1_rating_by_decade(title_basics: DataFrame, title_ratings: DataFrame) -> DataFrame:
    """Як змінювався середній рейтинг топ-фільмів по десятиліттях"""
    window = Window.orderBy("decade").rowsBetween(-2, 2)
    return title_basics \
        .filter(F.col("titleType") == "movie") \
        .filter(F.col("startYear").isNotNull()) \
        .join(title_ratings, "tconst") \
        .filter(F.col("numVotes") >= 1000) \
        .withColumn("decade", (F.col("startYear") / 10).cast("int") * 10) \
        .groupBy("decade") \
        .agg(
            F.round(F.avg("averageRating"), 2).alias("avg_rating"),
            F.count("tconst").alias("total_movies"),
            F.round(F.avg("numVotes"), 0).alias("avg_votes")
        ) \
        .withColumn("moving_avg", F.round(F.avg("avg_rating").over(window), 2)) \
        .orderBy("decade")


def q2_genre_quality_vs_popularity(title_basics: DataFrame, title_ratings: DataFrame) -> DataFrame:
    """Залежність між популярністю жанру і його якістю"""
    return title_basics \
        .filter(F.col("genres").isNotNull()) \
        .filter(~F.col("titleType").isin("tvEpisode")) \
        .join(title_ratings, "tconst") \
        .withColumn("genre", F.explode(F.split(F.col("genres"), ","))) \
        .filter(F.col("genre") != "Adult") \
        .groupBy("genre") \
        .agg(
            F.round(F.avg("averageRating"), 2).alias("avg_rating"),
            F.count("tconst").alias("total_titles"),
            F.round(F.avg("numVotes"), 0).alias("avg_votes")
        ) \
        .filter(F.col("total_titles") >= 1000) \
        .orderBy(F.col("avg_rating").desc())


def q3_consistent_directors(title_crew: DataFrame, title_basics: DataFrame,
                             title_ratings: DataFrame, name_basics: DataFrame) -> DataFrame:
    """Режисери з найвищим відсотком фільмів >= 7.0 серед тих хто зняв > 10 фільмів"""
    all_movies = title_crew \
        .filter(F.col("directors").isNotNull()) \
        .join(title_basics.filter(F.col("titleType") == "movie"), "tconst") \
        .join(title_ratings, "tconst") \
        .groupBy("directors") \
        .agg(
            F.count("tconst").alias("total_movies"),
            F.sum(F.when(F.col("averageRating") >= 7.0, 1).otherwise(0)).alias("quality_movies"),
            F.round(F.avg("averageRating"), 2).alias("avg_rating")
        ) \
        .filter(F.col("total_movies") >= 10) \
        .withColumn("quality_pct", F.round(F.col("quality_movies") / F.col("total_movies") * 100, 1))

    return all_movies \
        .join(name_basics.select("nconst", "primaryName"),
              F.col("directors") == F.col("nconst")) \
        .orderBy(F.col("quality_pct").desc()) \
        .select("primaryName", "total_movies", "quality_movies", "quality_pct", "avg_rating") \
        .limit(10)


def q4_outstanding_films(title_basics: DataFrame, title_ratings: DataFrame) -> DataFrame:
    """Фільми що найбільше перевищують середній рейтинг окремого жанру (мін. 10,000 голосів)"""
    window = Window.partitionBy("genre")
    return title_basics \
        .filter(F.col("titleType") == "movie") \
        .filter(F.col("genres").isNotNull()) \
        .join(title_ratings, "tconst") \
        .filter(F.col("numVotes") >= 10000) \
        .withColumn("genre", F.explode(F.split(F.col("genres"), ","))) \
        .filter(F.col("genre") != "Adult") \
        .withColumn("genre_avg_rating", F.round(F.avg("averageRating").over(window), 2)) \
        .withColumn("diff_from_avg", F.round(F.col("averageRating") - F.col("genre_avg_rating"), 2)) \
        .select("primaryTitle", "startYear", "genre", "averageRating",
                "genre_avg_rating", "diff_from_avg", "numVotes") \
        .orderBy(F.col("diff_from_avg").desc()) \
        .dropDuplicates(["primaryTitle", "genre"]) \
        .limit(15)


def q5_live_vs_voice_actors(title_principals: DataFrame, name_basics: DataFrame,
                             title_ratings: DataFrame, title_basics: DataFrame) -> DataFrame:
    """Порівняння топ живих акторів і голосових акторів за к-стю якісних тайтлів"""
    non_episode = title_basics.filter(~F.col("titleType").isin("tvEpisode"))

    live = title_principals \
        .filter(F.col("category").isin("actor", "actress")) \
        .join(non_episode.filter(
            F.col("genres").isNull() | ~F.col("genres").contains("Animation")
        ), "tconst") \
        .join(title_ratings, "tconst") \
        .filter(F.col("averageRating") >= 8.0) \
        .groupBy("nconst") \
        .agg(F.count("tconst").alias("high_rated_count")) \
        .join(name_basics.select("nconst", "primaryName"), "nconst") \
        .orderBy(F.col("high_rated_count").desc()) \
        .select(F.lit("live").alias("type"), "primaryName", "high_rated_count") \
        .limit(10)

    voice = title_principals \
        .filter(F.col("category").isin("actor", "actress")) \
        .join(non_episode.filter(
            F.col("genres").isNotNull() & F.col("genres").contains("Animation")
        ), "tconst") \
        .join(title_ratings, "tconst") \
        .filter(F.col("averageRating") >= 8.0) \
        .groupBy("nconst") \
        .agg(F.count("tconst").alias("high_rated_count")) \
        .join(name_basics.select("nconst", "primaryName"), "nconst") \
        .orderBy(F.col("high_rated_count").desc()) \
        .select(F.lit("voice").alias("type"), "primaryName", "high_rated_count") \
        .limit(10)

    return live.union(voice)


def q6_genre_best_films(title_basics: DataFrame, title_ratings: DataFrame) -> DataFrame:
    """Еталонний фільм кожного жанру за рейтингом (мін. 5000 голосів)"""
    window = Window.partitionBy("genre").orderBy(F.col("averageRating").desc())
    return title_basics \
        .filter(F.col("titleType") == "movie") \
        .filter(F.col("genres").isNotNull()) \
        .join(title_ratings, "tconst") \
        .filter(F.col("numVotes") >= 5000) \
        .withColumn("genre", F.explode(F.split(F.col("genres"), ","))) \
        .filter(F.col("genre") != "Adult") \
        .withColumn("rank_in_genre", F.rank().over(window)) \
        .filter(F.col("rank_in_genre") == 1) \
        .select("genre", "primaryTitle", "startYear", "averageRating", "numVotes") \
        .orderBy("genre")
