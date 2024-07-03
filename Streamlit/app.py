import streamlit as st
from utils import PrepProcesor, columns
import os

import numpy as np
import pandas as pd
import joblib

# Load the model from the uploaded path
model_path = './xgbpipe.joblib'
model = joblib.load(model_path)

# Set the page config
st.set_page_config(page_title='Passenger Survival Prediction', layout='wide')

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        color: #333;
        font-family: 'Roboto', sans-serif;
    }
    .block-container {
        padding: 2rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 1rem;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        border: none;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>div>input {
        font-size: 1rem;
        padding: 0.5rem;
        border-radius: 0.25rem;
        border: 1px solid #ccc;
    }
    .stSelectbox>div>div>select {
        font-size: 1rem;
        padding: 0.5rem;
        border-radius: 0.25rem;
        border: 1px solid #ccc;
    }
    .stSlider>div>div>div>div>div>div {
        font-size: 1rem;
    }
    .stNumberInput>div>div>input {
        font-size: 1rem;
        padding: 0.5rem;
        border-radius: 0.25rem;
        border: 1px solid #ccc;
    }
    .stAlert {
        font-size: 1.2rem;
        padding: 1rem;
        border-radius: 0.25rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title('Did they make it through? :ship:')

# Input fields
passengerid = st.text_input("PASSENGER ID ENTRY", '123456')
pclass = st.selectbox("CLASS SELECTION", [1, 2, 3])
name = st.text_input("PASSENGER NAME ENTRY", 'Jason Brown')
sex = st.select_slider("SEXUAL IDENTITY", ['male', 'female'])
age = st.slider("YOUR AGE", 0, 100)
sibsp = st.slider("SIBLINGS SELECTION", 0, 10)
parch = st.slider("PARENTS/CHILDREN ONBOARD", 0, 2)
ticket = st.text_input("INPUT TICKET NUMBER", "12345")
fare = st.number_input("FARE PRICE INPUT", 0, 1000)
cabin = st.text_input("INPUT CABIN", "C52")
embarked = st.select_slider("DID THEY SET SAIL?", ['S', 'C', 'Q'])

def predict():
    row = [passengerid, pclass, name, sex, age, sibsp, parch, ticket, fare, cabin, embarked]
    X = pd.DataFrame([row], columns=columns)
    preprocessor = PrepProcesor()
    preprocessor.fit(X)  # Fit the preprocessor
    X = preprocessor.transform(X)
    prediction = model.predict(X)
    if prediction[0] == 1:
        st.success('Passenger Survived :thumbsup:')
    else:
        st.error('Passenger did not Survive :thumbsdown:')

trigger = st.button('PREDICT', on_click=predict)
