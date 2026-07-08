# model training and recommendation generation
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

MAX_FEATURES = 5000


def train_model(movies):
    """Vectorize movie tags and compute pairwise cosine similarity between movies.

    Args:
        movies: pd.DataFrame with a "tags" column (output of data_cleaner.clean_data).

    Returns:
        np.ndarray: an (n_movies x n_movies) similarity matrix, where
                    similarity[i][j] is how similar movie i is to movie j.
    """
    vec = CountVectorizer(max_features=MAX_FEATURES, stop_words="english")
    tag_vector = vec.fit_transform(movies["tags"]).toarray()
    return cosine_similarity(tag_vector)


def recommend(movie, movies, similarity, count=5):
    """Recommend similar movies to the given title.

    Args:
        movie: str, exact title to base recommendations on.
        movies: pd.DataFrame with movie_id/title columns, same row order used
                to train the similarity matrix.
        similarity: np.ndarray, output of train_model().
        count: int, how many recommendations to return.

    Returns:
        pd.DataFrame: the top `count` most similar rows from `movies`
                      (excluding the input movie itself).
    """
    matches = movies[movies["title"] == movie]
    if matches.empty:
        raise ValueError(f"'{movie}' not found in movies dataframe")

    index = matches.index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    top_indices = [i[0] for i in distances[1:count + 1]]

    return movies.iloc[top_indices]


def save_model(movies, similarity, movies_path="models/movies_info.pkl", similarity_path="models/recommender.pkl"):
    """Persist the cleaned movies dataframe and similarity matrix to disk.

    Args:
        movies: pd.DataFrame to pickle.
        similarity: np.ndarray to pickle.
        movies_path: str, output path for the movies pickle.
        similarity_path: str, output path for the similarity matrix pickle.
    """
    with open(movies_path, "wb") as f:
        pickle.dump(movies, f)

    with open(similarity_path, "wb") as f:
        pickle.dump(similarity, f)