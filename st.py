import streamlit as st
import pickle
import requests
import pandas as pd

df = pd.read_csv("movie dataset.csv")

st.set_page_config(page_title='Movie Recommendation System', layout='wide')

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

st.header("Movie Recommender System")

selectvalue = st.selectbox("Select movie from dropdown", movies_list)


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []

    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]].id
        movie_title = movies.iloc[i[0]].title
        movie_popularity = df.iloc[i[0]].popularity  # Assuming 'popularity' is the column name
        movie_genre = df.iloc[i[0]].genre  # Assuming 'genre' is the column name for movie genre
        recommend_movie.append({'title': movie_title, 'popularity': movie_popularity, 'genre': movie_genre})

    # Sort recommendations by popularity in descending order
    recommend_movie = sorted(recommend_movie, key=lambda x: x['popularity'], reverse=True)

    return recommend_movie


def get_movie_info(movie_name, api_key):
    base_url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": api_key,
        "query": movie_name
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data


def movie(moviename, popularity, genre):
    # Define your TMDb API key
    api_key = "679e1024ae8d7b2072c6cf22a6cbfdd0"

    movie_name = moviename
    movie_data = get_movie_info(movie_name, api_key)
    if movie_data["results"]:
        poster_path = movie_data["results"][0]["poster_path"]
        image_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        st.image(image_url, width=200)
        st.markdown(
            f"**Title:** {movie_name}  \n**Popularity:** {popularity}  \n**Genre:** {genre}",
            unsafe_allow_html=True
        )
    else:
        st.warning("Movie not found.")


if st.button("Show Recommend"):
    st.balloons()
    recommended_movies = recommend(selectvalue)
    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]

    for movie_info, col in zip(recommended_movies, columns):
        with col:
            movie(movie_info['title'], movie_info['popularity'], movie_info['genre'])
