import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import squarify

sns.set_theme(style="whitegrid")
COLORS = sns.color_palette("muted", 12)


def plot_q1_rating_by_decade(df_pandas, output_path):
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.bar(df_pandas["decade"], df_pandas["total_movies"],
            color=COLORS[1], alpha=0.4, label="Кількість фільмів")
    ax1.set_ylabel("Кількість фільмів", color=COLORS[1])
    ax1.tick_params(axis="y", labelcolor=COLORS[1])

    ax2 = ax1.twinx()
    ax2.plot(df_pandas["decade"], df_pandas["avg_rating"],
             color=COLORS[0], marker="o", linewidth=2, label="Середній рейтинг")
    ax2.plot(df_pandas["decade"], df_pandas["moving_avg"],
             color=COLORS[2], linestyle="--", linewidth=2, label="Ковзне середнє")
    ax2.set_ylabel("Середній рейтинг", color=COLORS[0])
    ax2.set_ylim(5.5, 7.5)
    ax2.tick_params(axis="y", labelcolor=COLORS[0])

    ax1.set_xlabel("Десятиліття")
    ax1.set_title("Середній рейтинг фільмів по десятиліттях\n(фільми з мін. 1000 голосів)", fontsize=13)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    plt.tight_layout()
    plt.savefig(f"{output_path}/q1_rating_by_decade.png", dpi=150)
    plt.close()
    print("Q1 chart saved")


def plot_q2_genre_quality(df_pandas, output_path):
    fig, ax = plt.subplots(figsize=(12, 8))

    scatter = ax.scatter(
        df_pandas["avg_votes"],
        df_pandas["avg_rating"],
        s=df_pandas["total_titles"] / 5000,
        c=df_pandas["avg_rating"],
        cmap="RdYlGn",
        alpha=0.7,
        edgecolors="white",
        linewidth=0.5
    )

    for _, row in df_pandas.iterrows():
        ax.annotate(row["genre"],
                    (row["avg_votes"], row["avg_rating"]),
                    fontsize=8, ha="center", va="bottom",
                    xytext=(0, 6), textcoords="offset points")

    plt.colorbar(scatter, ax=ax, label="Середній рейтинг")
    ax.set_xlabel("Середня кількість голосів на тайтл (популярність)")
    ax.set_ylabel("Середній рейтинг (якість)")
    ax.set_title("Якість vs Популярність жанрів\n(розмір кола = кількість тайтлів)", fontsize=13)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

    plt.tight_layout()
    plt.savefig(f"{output_path}/q2_genre_quality.png", dpi=150)
    plt.close()
    print("Q2 chart saved")


def plot_q3_directors(df_pandas, output_path):
    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.barh(df_pandas["primaryName"], df_pandas["avg_rating"],
                   color=COLORS, edgecolor="white")

    for bar, (_, row) in zip(bars, df_pandas.iterrows()):
        ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height() / 2,
                f"{row['avg_rating']} ({int(row['total_movies'])} фільмів)",
                va="center", fontsize=9)

    ax.set_xlabel("Середній рейтинг")
    ax.set_title("Топ режисерів за середнім рейтингом\n(мін. 10 фільмів, 100% якість >= 7.0)", fontsize=13)
    ax.set_xlim(0, 10)
    ax.invert_yaxis()

    plt.tight_layout()
    plt.savefig(f"{output_path}/q3_directors.png", dpi=150)
    plt.close()
    print("Q3 chart saved")


def plot_q4_outstanding(df_pandas, output_path):
    fig, ax = plt.subplots(figsize=(12, 8))

    df_sorted = df_pandas.sort_values("diff_from_avg")
    colors = [COLORS[0] if d >= 2.5 else COLORS[1] for d in df_sorted["diff_from_avg"]]

    ax.hlines(df_sorted["primaryTitle"], 0, df_sorted["diff_from_avg"],
              color="grey", alpha=0.4, linewidth=1.5)
    ax.scatter(df_sorted["diff_from_avg"], df_sorted["primaryTitle"],
               color=colors, s=80, zorder=3)

    for _, row in df_sorted.iterrows():
        ax.text(row["diff_from_avg"] + 0.02, row["primaryTitle"],
                f"+{row['diff_from_avg']} ({row['genre']})",
                va="center", fontsize=8)

    ax.set_xlabel("Відхилення від середнього рейтингу жанру")
    ax.set_title("Фільми що найбільше перевищують середній рейтинг жанру\n(мін. 10,000 голосів)", fontsize=13)
    ax.axvline(x=0, color="black", linestyle="-", linewidth=0.8)

    plt.tight_layout()
    plt.savefig(f"{output_path}/q4_outstanding.png", dpi=150)
    plt.close()
    print("Q4 chart saved")


def plot_q5_actors(df_pandas, output_path):
    live = df_pandas[df_pandas["type"] == "live"].head(10)
    voice = df_pandas[df_pandas["type"] == "voice"].head(10)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    ax1.barh(live["primaryName"], live["high_rated_count"],
             color=COLORS[0], edgecolor="white")
    ax1.set_title("Живі актори", fontsize=12)
    ax1.set_xlabel("Кількість якісних тайтлів (>= 8.0)")
    ax1.invert_yaxis()

    ax2.barh(voice["primaryName"], voice["high_rated_count"],
             color=COLORS[2], edgecolor="white")
    ax2.set_title("Голосові актори (анімація)", fontsize=12)
    ax2.set_xlabel("Кількість якісних тайтлів (>= 8.0)")
    ax2.invert_yaxis()

    fig.suptitle("Топ акторів за кількістю якісних тайтлів", fontsize=13)
    plt.tight_layout()
    plt.savefig(f"{output_path}/q5_actors.png", dpi=150)
    plt.close()
    print("Q5 chart saved")


def plot_q6_treemap(df_pandas, output_path):
    df_unique = df_pandas.drop_duplicates("genre").head(20)

    fig, ax = plt.subplots(figsize=(14, 8))
    labels = [f"{row['genre']}\n{row['primaryTitle']}\n⭐{row['averageRating']}"
              for _, row in df_unique.iterrows()]
    sizes = df_unique["averageRating"].values
    colors = plt.cm.RdYlGn(
        (df_unique["averageRating"] - df_unique["averageRating"].min()) /
        (df_unique["averageRating"].max() - df_unique["averageRating"].min())
    )

    squarify.plot(sizes=sizes, label=labels, color=colors,
                  alpha=0.85, ax=ax, text_kwargs={"fontsize": 8})
    ax.set_title("Еталонний фільм кожного жанру (розмір = рейтинг)", fontsize=13)
    ax.axis("off")

    plt.tight_layout()
    plt.savefig(f"{output_path}/q6_treemap.png", dpi=150)
    plt.close()
    print("Q6 chart saved")
