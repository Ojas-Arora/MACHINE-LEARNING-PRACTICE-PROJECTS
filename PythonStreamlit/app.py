import streamlit as st
import pandas as pd
import os

# Set page configuration
st.set_page_config(page_title="Simple Data Analysis", layout="wide")

# Title and styling
st.title("Simple Data Analysis with Streamlit")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# File upload section
fl = st.file_uploader("Upload a file", type=["csv", "txt", "xlsx", "xls"])

if fl is not None:
    filename = fl.name
    st.write(f"File Name: {filename}")

    # Load data based on file type
    if filename.endswith(".csv") or filename.endswith(".txt"):
        df = pd.read_csv(fl, encoding="ISO-8859-1")
    elif filename.endswith(".xlsx") or filename.endswith(".xls"):
        df = pd.read_excel(fl)

    # Display first few rows of the dataframe
    st.write("Sample Data:")
    st.write(df.head())

    # Date range selection
    startDate = pd.to_datetime(df["Order Date"]).min()
    endDate = pd.to_datetime(df["Order Date"]).max()

    col1, col2 = st.columns(2)

    with col1:
        date1 = st.date_input("Start Date", startDate)

    with col2:
        date2 = st.date_input("End Date", endDate)

    # Filter data based on date range
    filtered_df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

    # Display filtered data
    st.subheader("Filtered Data:")
    st.write(filtered_df)

    # Download filtered data as CSV
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button('Download Filtered Data', data=csv, file_name="Filtered_Data.csv", mime="text/csv")

else:
    st.warning("Please upload a file.")

