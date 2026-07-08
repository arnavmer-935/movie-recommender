import pickle
import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv
import os

from recommendation import recommend

load_dotenv()
API_KEY = os.getenv("API_KEY")

def fetch_poster(movie_id):
    """Fetch a movie's poster image URL from the TMDB API.

    Args:
        movie_id: int, the TMDB movie ID (from the movies dataframe).

    Returns:
        str: a full poster image URL, or a placeholder image URL if the
             request fails, times out, or the movie has no poster on TMDB.
    """
    placeholder = "https://placehold.co/500x750?text=No+Poster"
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key={}".format(movie_id, API_KEY)
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if not poster_path:
            return placeholder
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    except requests.exceptions.RequestException:
        return placeholder


st.header('Movie Recommender System')
movies = pickle.load(open("models/movies_info.pkl",'rb'))
similarity = pickle.load(open('models/recommender.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    results = recommend(selected_movie, movies, similarity)
    cols = st.columns(5)
    for col, (_, row) in zip(cols, results.iterrows()):
        with col:
            st.text(row['title'])
            st.image(fetch_poster(row['movie_id']))