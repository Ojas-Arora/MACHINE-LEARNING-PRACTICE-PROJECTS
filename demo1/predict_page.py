import os
import streamlit as st
import pickle
import numpy as np

def load_model():
    try:
        file_path = 'saved_steps.pkl'
        if not os.path.exists(file_path):
            st.error(f"File '{file_path}' not found.")
            return None
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
        return data
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

data = load_model()
if data:
    regressor = data["model"]
    le_country = data["le_country"]
    le_education = data["le_education"]
else:
    st.stop()

def show_predict_page():
    st.title("Software Developer Salary Prediction")
    st.write("""### We need some information to predict the salary""")

    countries = (
        "United States", "India", "United Kingdom", "Germany", "Canada",
        "Brazil", "France", "Spain", "Australia", "Netherlands", "Poland",
        "Italy", "Russian Federation", "Sweden",
    )

    education = (
        "Less than a Bachelors", "Bachelor’s degree", "Master’s degree", "Post grad",
    )

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)
    experience = st.slider("Years of Experience", 0, 50, 3)

    ok = st.button("Calculate Salary")
    if ok:
        X = np.array([[country, education, experience]])
        X[:, 0] = le_country.transform([X[:, 0]])[0]
        X[:, 1] = le_education.transform([X[:, 1]])[0]
        X = X.astype(float)
        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")

show_predict_page()
