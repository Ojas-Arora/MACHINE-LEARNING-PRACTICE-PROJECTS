import pandas as pd
import datetime as dt
import plotly.express as px
import streamlit as st

# Load data
file_path = 'rfm_data.csv'  # Change this to the actual path if necessary
data = pd.read_csv(file_path)

# Convert PurchaseDate to datetime
data['PurchaseDate'] = pd.to_datetime(data['PurchaseDate'])

# Define reference date for recency calculation
reference_date = dt.datetime(2023, 7, 1)

# Calculate RFM metrics
rfm = data.groupby('CustomerID').agg({
    'PurchaseDate': lambda x: (reference_date - x.max()).days,
    'OrderID': 'count',
    'TransactionAmount': 'sum'
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

# Filter out non-positive monetary values
rfm = rfm[rfm['Monetary'] > 0]

# Define RFM score thresholds
rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, ['1', '2', '3', '4'])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, ['4', '3', '2', '1'])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 4, ['4', '3', '2', '1'])

# Concatenate RFM score to a single RFM segment
rfm['RFM_Segment'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
rfm['RFM_Score'] = rfm[['R_Score', 'F_Score', 'M_Score']].sum(axis=1).astype(int)

# Define RFM segments
def rfm_segment(df):
    if df['RFM_Score'] >= 9:
        return 'Champions'
    elif df['RFM_Score'] >= 8:
        return 'Loyal Customers'
    elif df['RFM_Score'] >= 7:
        return 'Potential Loyalists'
    elif df['RFM_Score'] >= 6:
        return 'Recent Customers'
    elif df['RFM_Score'] >= 5:
        return 'Promising'
    elif df['RFM_Score'] >= 4:
        return 'Need Attention'
    elif df['RFM_Score'] >= 3:
        return 'At Risk'
    else:
        return 'Lost'

rfm['RFM_Segment'] = rfm.apply(rfm_segment, axis=1)

# Count of customers in each segment
segment_counts = rfm['RFM_Segment'].value_counts().reset_index()
segment_counts.columns = ['RFM_Segment', 'Count']

# Streamlit Dashboard
st.title("RFM Analysis Dashboard")

# Dropdown for analysis type
analysis_type = st.selectbox("Analyze customer segments based on RFM scores:", [
    "Comparison of RFM Segments",
    "RFM Value Segment Distribution",
    "Distribution of RFM Values within Customer Segment",
    "Correlation Matrix of RFM Values within Champions Segment"
])

# Plot based on selection
if analysis_type == "Comparison of RFM Segments":
    fig = px.bar(segment_counts, x='RFM_Segment', y='Count', title='Count of Customers in Each RFM Segment')
    st.plotly_chart(fig)
elif analysis_type == "RFM Value Segment Distribution":
    fig = px.histogram(rfm, x='RFM_Score', title='RFM Score Distribution')
    st.plotly_chart(fig)
elif analysis_type == "Distribution of RFM Values within Customer Segment":
    segment = st.selectbox("Select RFM Segment:", rfm['RFM_Segment'].unique())
    segment_data = rfm[rfm['RFM_Segment'] == segment]
    fig = px.histogram(segment_data, x='Recency', title=f'Recency Distribution in {segment} Segment')
    st.plotly_chart(fig)
    fig = px.histogram(segment_data, x='Frequency', title=f'Frequency Distribution in {segment} Segment')
    st.plotly_chart(fig)
    fig = px.histogram(segment_data, x='Monetary', title=f'Monetary Distribution in {segment} Segment')
    st.plotly_chart(fig)
elif analysis_type == "Correlation Matrix of RFM Values within Champions Segment":
    champions_data = rfm[rfm['RFM_Segment'] == 'Champions']
    correlation_matrix = champions_data[['Recency', 'Frequency', 'Monetary']].corr()
    fig = px.imshow(correlation_matrix, text_auto=True, title='Correlation Matrix of RFM Values within Champions Segment')
    st.plotly_chart(fig)
