import streamlit as st
import requests
import joblib
from sklearn.metrics.pairwise import cosine_similarity

movies = joblib.load('movies.pkl')
vectors = joblib.load('vectors.pkl')
cv = joblib.load('vectorizer.pkl')

API_KEY = "b6eb16bf29cf3d3a4ad3865c8ebee5bf"

st.title("🎬 Movie Recommender System by Satyam")

selected_movie = st.selectbox(
    "Select a movie:",
    movies['title_x'].values
)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    return "https://image.tmdb.org/t/p/w500" + poster_path if poster_path else ""

def recommend(movie):
    index = movies[movies['title_x'] == movie].index[0]
    distances = cosine_similarity(vectors[index].reshape(1, -1), vectors).flatten()
    movie_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]

    names, posters = [], []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        names.append(movies.iloc[i[0]].title_x)
        posters.append(fetch_poster(movie_id))
    return names, posters

if st.button("Recommend 🎯"):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
