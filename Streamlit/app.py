import streamlit as st
from utils import PrepProcesor, columns

import numpy as np
import pandas as pd
import joblib

model = joblib.load('xgbpipe.joblib')
st.title('Did they make it through? :ship:')

# Input fields
passengerid = st.text_input("PASSENGER ID ENTRY", '123456')
pclass = st.selectbox("CLASS SELECTION", [1,2,3])
name = st.text_input("PASSENGER NAME ENTRY", 'Jason Brown')
sex = st.select_slider("SEXUAL IDENTITY", ['male','female'])
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
    X = preprocessor.transform(X)
    prediction = model.predict(X)
    if prediction[0] == 1:
        st.success('Passenger Survived :thumbsup:')
    else:
        st.error('Passenger did not Survive :thumbsdown:')

trigger = st.button('PREDICT', on_click=predict)
