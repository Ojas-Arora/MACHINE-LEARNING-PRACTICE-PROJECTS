import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Load Netflix data
netflix_data = pd.read_csv('netflix_titles.csv')

# Fill missing descriptions with empty strings
netflix_data['description'] = netflix_data['description'].fillna('')

# Create TF-IDF matrix
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(netflix_data['description'])

# Compute cosine similarity
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Create reverse mapping of indices and movie titles
indices = pd.Series(netflix_data.index, index=netflix_data['title']).drop_duplicates()

def get_recommendations(title, cosine_sim=cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return netflix_data.iloc[movie_indices]

def Table(df):
    fig = go.Figure(go.Table(
        columnorder=[1, 2, 3],
        columnwidth=[10, 28],
        header=dict(values=['Title', 'Description'],
                    line_color='black', font=dict(color='black', size=19), height=40,
                    fill_color='#dd571c', align=['left', 'center']),
        cells=dict(values=[df.title, df.description],
                   fill_color='#ffdac4', line_color='grey',
                   font=dict(color='black', family="Lato", size=16), align='left')
    ))
    fig.update_layout(height=500, title={'text': "Top 10 Movie Recommendations", 'font': {'size': 22}}, title_x=0.5)
    return st.plotly_chart(fig, use_container_width=True)

# Streamlit app
st.header('Netflix Movie Recommendation System')

# Load and display Lottie animation
lottie_coding = load_lottiefile("m4.json")
st_lottie(lottie_coding, speed=1, reverse=False, loop=True, quality="low", height=220)

# Dropdown for movie selection
movie_list = netflix_data['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Display recommendations on button click
if st.button('Show Recommendation'):
    recommended_movie_names = get_recommendations(selected_movie)
    Table(recommended_movie_names)

# Checkbox for EDA link
EDA = st.checkbox('Show Netflix Exploratory Data Analysis')
if EDA:
    st.write("Check out this [link](https://www.kaggle.com/code/rushikeshdane20/in-depth-analysis-of-netflix-with-plotly)")
