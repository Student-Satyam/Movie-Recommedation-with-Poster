import streamlit as st
import requests
import joblib
import pandas as pd

# ✅ Load Saved Files
movies = joblib.load('movies.pkl')
similarity = joblib.load('similarity.pkl')

API_KEY = "b6eb16bf29cf3d3a4ad3865c8ebee5bf"  # ✅ Replace with your TMDB API key

st.title("🎬 Movie Recommender System by Satyam")

selected_movie = st.selectbox(
    "Select a movie to get recommendations:",
    movies['title_x'].values
)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    movie_index = movies[movies['title_x'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title_x)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

if st.button("Recommend 🎯"):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
