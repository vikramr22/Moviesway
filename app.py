import streamlit as st
import pandas as pd
import pickle
import requests

st. set_page_config(layout="wide")
#Backend

movies_dict = pickle.load(open("movies_dict.pkl","rb"))
movies =pd.DataFrame(movies_dict)

vote_info=pickle.load(open("vote_info.pkl","rb"))
vote=pd.DataFrame(vote_info)

# @st.cache
# def similarity():
#     return pickle.load(open("similarity.pkl","rb"))

# similarity =pickle.load(open("similarity.pkl","rb"))
similarity =pickle.load(open("similarity.pkl","rb"))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:6]
    recommend_movies_names=[]
    recommend_posters=[]
    movie_ids=[]
    for i in movies_list:
        temp_Mov_id = movies.iloc[i[0]].movie_id
        movie_ids.append(temp_Mov_id)
        #fetch poster
        recommend_posters.append(fetch_poster(temp_Mov_id))
        recommend_movies_names.append(movies.iloc[i[0]].title)
    return recommend_movies_names,recommend_posters,movie_ids

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=your_api_kpi')
    data =response.json()
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]


#Frontend
st.write(""" <h2> <b style="color:red"> MoviesWay</b> </h2>""",unsafe_allow_html=True)
st.write("###")

st.write(""" <p> Hii, welcome to <b style="color:red">MoviesWay</b>, this free movie recommendation engine suggests films based on your interest </p>""",unsafe_allow_html=True)
st.write("##")
my_expander = st.expander("Tap to Select a Movie  🌐️")
selected_movie_name = my_expander.selectbox("",movies["title"].values[:-3])


if my_expander.button("Recommend"):
    st.text("Here are few Recommendations..")
    st.write("#")
    names,posters,movie_ids=recommend(selected_movie_name)
    col1,col2,col3,col4,col5=st.columns(5)
    cols=[col1,col2,col3,col4,col5]
    for i in range(0,5):
            with cols[i]:
                st.write(f' <b style="color:#E50914"> {names[i]} </b>',unsafe_allow_html=True)
                # st.write("#")
                st.image(posters[i])
                id=movie_ids[i]
                st.write("________")
                vote_avg, vote_count = vote[vote["id"] == id].vote_average , vote[vote["id"] == id].vote_count
                st.write(f'<b style="color:#DB4437">Rating</b>:<b> {list(vote_avg.values)[0]}</b>',unsafe_allow_html=True)
                st.write(f'<b style="color:#DB4437">   Votes  </b>: <b> {list(vote_count.values)[0]} <b> ',unsafe_allow_html=True)

st.write("##")
tab1 ,tab2 = st.tabs(["About","Working"])

with tab1:
    st.caption('This a Content Based Movie Recommendation System')
    st.caption('In upcoming versions new movies would be added :sunglasses:')
with tab2:
    st.caption('It Contains Movies data from The Movie Data Base (TMDB)')
    st.caption("For more infos and ⭐ at https://github.com/vikramr22/Moviesway ")


