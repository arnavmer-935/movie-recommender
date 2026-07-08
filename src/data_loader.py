import pandas as pd

def parse_data():
    """Load and merge the TMDB movies/credits datasets.

    Returns:
        pd.DataFrame with columns: movie_id, title, overview, genres, keywords, cast, crew
    """
    movies = pd.read_csv("data/tmdb_5000_movies.csv")
    credits = pd.read_csv("data/tmdb_5000_credits.csv", encoding="latin1")

    movies = movies.merge(credits, on="title")

    if len(movies) < min(len(movies), len(credits)) * 0.9:
        raise ValueError(
            f"Merge dropped too many rows: {len(movies)} remain "
            f"(movies had {len(movies)}, credits had {len(credits)})"
        )

    movies = movies[["movie_id", "title", "overview", "genres", "keywords", "cast", "crew"]]

    return movies

