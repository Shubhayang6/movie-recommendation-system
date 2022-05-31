import streamlit as st
import pickle
import pandas as pd
import requests
import os

from dotenv import load_dotenv
load_dotenv()


API_KEY=os.getenv('API_KEY')


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=834956f67059f048d5c331a1a9156955&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path'] #poster path

def recommend(movie):
    movie_idx=movies[movies['title']==movie].index[0]
    distances=similarity[movie_idx]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster of movies from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters 



movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))



st.title('Movie Recommendation System')



selected_movie = st.selectbox(
     'Select your favourite movie    😄',
    movies['title'].values)     

st.write('Movie:', selected_movie)




if st.button('Recommend'):
    names,posters=recommend(selected_movie)
    
    col1, col2, col3,col4,col5 = st.columns(5)

    with col1:
        st.markdown(names[0])
        st.image(posters[0])

    with col2:
        st.markdown(names[1])
        st.image(posters[1])

    with col3:
        st.markdown(names[2])
        st.image(posters[2])

    with col4:
        st.markdown(names[3])
        st.image(posters[3])

    with col5:
        st.markdown(names[4])
        st.image(posters[4])
