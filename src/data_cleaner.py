import data_utils as du
def parse_json_columns(movies):
    """Convert the JSON-string columns (genres, keywords, cast, crew) into
    clean lists of names, and strip spaces so multi-word tags stay intact.

    Args:
        movies: pd.DataFrame from data_loader.parse_data(), with raw
                genres/keywords/cast/crew columns still as JSON strings.

    Returns:
        pd.DataFrame with genres/keywords/cast/crew as space-stripped lists.
    """
    
    fields = ["genres", "keywords", "cast", "crew"]

    for field in fields[:2]:
        movies[field] = movies[field].apply(du.convert)
    
    movies["cast"] = movies["cast"].apply(du.castconvert)
    movies["crew"] = movies["crew"].apply(du.director)
    
    for field in fields:
        movies[field] = movies[field].apply(du.remove_spaces)

    return movies

def build_tags(movies):
    """Combine overview + genres + keywords + cast + crew into a single
    'tags' string per movie, ready for vectorization.

    Args:
        movies: pd.DataFrame with parsed genres/keywords/cast/crew columns
                (i.e. output of parse_json_columns).

    Returns:
        pd.DataFrame with columns: movie_id, title, tags (tags is a str).
    """

    movies.dropna(inplace = True)
    movies["overview"] = movies["overview"].apply(du.splitter)

    movies["tags"] = movies["overview"] + movies["genres"] + movies["keywords"] + movies["cast"] + movies["crew"]

    movies = movies[["movie_id", "title", "tags"]].copy()

    movies["tags"] = movies["tags"].apply(du.joiner)

    return movies


def clean_data(movies):
    """Full cleaning pipeline: raw merged dataframe -> final tagged dataframe.

    Args:
        movies: pd.DataFrame from data_loader.parse_data().

    Returns:
        pd.DataFrame with columns: movie_id, title, tags.
    """
    movies = parse_json_columns(movies)
    movies = build_tags(movies)
    return movies