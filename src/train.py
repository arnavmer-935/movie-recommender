import os

from data_loader import parse_data
from data_cleaner import clean_data
from recommendation import train_model, save_model

MODELS_DIR = "models"

def main():
    os.makedirs(MODELS_DIR, exist_ok=True)

    print("Loading data...")
    movies = parse_data()

    print("Cleaning data...")
    movies = clean_data(movies)

    print(f"Training model on {len(movies)} movies...")
    similarity = train_model(movies)

    print("Saving model artifacts...")
    save_model(
        movies,
        similarity,
        movies_path=os.path.join(MODELS_DIR, "movies_info.pkl"),
        similarity_path=os.path.join(MODELS_DIR, "recommender.pkl"),
    )

    print(f"Done. Saved to {MODELS_DIR}/")

if __name__ == "__main__":
    main()