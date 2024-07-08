import streamlit as st
import pickle
import requests

st.set_page_config(page_title='Movie Recommendation System')

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list=movies['title'].values

st.header("Movie Recommender System")

selectvalue=st.selectbox("Select movie from dropdown",movies_list)



def recommend(movie):
    index=movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommend_movie=[]
    for i in distance[1:6]:
        movies_id=movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
    return recommend_movie


def get_movie_info(movie_name, api_key):
    base_url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key":api_key,
        "query": movie_name
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

def movie(moviename):
    # Define your TMDb API key
    api_key = "25441d21e07e9e9f56eb130b54144a1b"

    movie_name = moviename
    movie_data = get_movie_info(movie_name, api_key)
    if movie_data["results"]:
        poster_path = movie_data["results"][0]["poster_path"]
        image_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        st.image(image_url)
    else:
        st.warning("Movie not found.")

if st.button("Show Recommend"):
    st.balloons()
    movie_name = recommend(selectvalue)
    col1,col2,col3,col4,col5=st.columns(5)
    columns = [col1,col2,col3,col4,col5]
    for movies , col in zip(movie_name,columns):
        with col:
            st.text(movies)
            movie(movies)
        
        