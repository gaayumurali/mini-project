import streamlit as st
import requests
def get_movie_info(movie_name, api_key):
    base_url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key":api_key,
        "query": movie_name
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data


# Define your TMDb API key
api_key = "25441d21e07e9e9f56eb130b54144a1b"

movie_name = st.text_input("Enter the movie:")
if st.button("Recommend"):
    movie_data = get_movie_info(movie_name, api_key)
    if movie_data["results"]:
        poster_path = movie_data["results"][0]["poster_path"]
        image_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        st.image(image_url, caption="Movie Poster")
    else:
        st.warning("Movie not found.")


