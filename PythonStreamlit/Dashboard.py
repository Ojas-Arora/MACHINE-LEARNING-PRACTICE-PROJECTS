import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(page_title="Superstore EDA", page_icon=":bar_chart:", layout="wide")

# Title and styling
st.title(":bar_chart: Sample SuperStore EDA")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# File upload section
fl = st.file_uploader(":file_folder: Upload a file", type=["csv", "txt", "xlsx", "xls"])

if fl is not None:
    filename = fl.name
    st.write(filename)

    # Load data based on file type
    if filename.endswith(".csv") or filename.endswith(".txt"):
        df = pd.read_csv(fl, encoding="ISO-8859-1")
    elif filename.endswith(".xlsx") or filename.endswith(".xls"):
        df = pd.read_excel(fl)
else:
    default_path = r"C:\Users\AEPAC\Desktop\Streamlit\Superstore.csv"  # Adjust the path as needed

    if os.path.exists(default_path):
        df = pd.read_csv(default_path, encoding="ISO-8859-1")
    else:
        st.error("No file uploaded and default file path not found.")
        st.stop()

# Ensure all required columns are present
required_columns = ['Order Date', 'Category', 'Sales', 'Profit', 'Quantity', 'Segment', 'Sub-Category']
if all(col in df.columns for col in required_columns):
    df["Order Date"] = pd.to_datetime(df["Order Date"])

    # Date range selection
    startDate = pd.to_datetime(df["Order Date"]).min()
    endDate = pd.to_datetime(df["Order Date"]).max()

    col1, col2 = st.columns(2)

    with col1:
        date1 = st.date_input("Start Date", startDate)

    with col2:
        date2 = st.date_input("End Date", endDate)

    # Filter data based on date range
    df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

    # Sidebar filters
    st.sidebar.header("Choose your filter:")

    region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())
    df2 = df if not region else df[df["Region"].isin(region)]

    state = st.sidebar.multiselect("Pick the State", df2["State"].unique())
    df3 = df2 if not state else df2[df2["State"].isin(state)]

    city = st.sidebar.multiselect("Pick the City", df3["City"].unique())
    filtered_df = df3 if not city else df3[df3["City"].isin(city)]

    # Data visualization and analysis
    if filtered_df.empty:
        st.warning("No data available with the selected filters.")
    else:
        category_df = filtered_df.groupby(by=["Category"], as_index=False)["Sales"].sum()

        col1, col2 = st.columns((1, 1))

        with col1:
            st.subheader("Category wise Sales")
            fig = px.bar(category_df, x="Category", y="Sales", text=['${:,.2f}'.format(x) for x in category_df["Sales"]],
                         template="seaborn")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Region wise Sales")
            fig = px.pie(filtered_df, values="Sales", names="Region", hole=0.5)
            fig.update_traces(text=filtered_df["Region"], textposition="outside")
            st.plotly_chart(fig, use_container_width=True)

        # Additional data exploration
        cl1, cl2 = st.columns((1, 1))

        with cl1:
            with st.expander("Category_ViewData"):
                st.write(category_df.style.background_gradient(cmap="Blues"))
                csv = category_df.to_csv(index=False).encode('utf-8')
                st.download_button("Download Data", data=csv, file_name="Category.csv", mime="text/csv",
                                   help='Click here to download the data as a CSV file')

        with cl2:
            with st.expander("Region_ViewData"):
                region_summary = filtered_df.groupby(by="Region", as_index=False)["Sales"].sum()
                st.write(region_summary.style.background_gradient(cmap="Oranges"))
                csv = region_summary.to_csv(index=False).encode('utf-8')
                st.download_button("Download Data", data=csv, file_name="Region.csv", mime="text/csv",
                                   help='Click here to download the data as a CSV file')

        # Time series analysis
        filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")
        st.subheader('Time Series Analysis')
        linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
        fig2 = px.line(linechart, x="month_year", y="Sales", labels={"Sales": "Amount"}, height=500, width=1000, template="gridon")
        st.plotly_chart(fig2, use_container_width=True)

        with st.expander("View Data of TimeSeries:"):
            st.write(linechart.T.style.background_gradient(cmap="Blues"))
            csv = linechart.to_csv(index=False).encode("utf-8")
            st.download_button('Download Data', data=csv, file_name="TimeSeries.csv", mime='text/csv')

        # Hierarchical view of Sales using TreeMap
        st.subheader("Hierarchical view of Sales using TreeMap")
        fig3 = px.treemap(filtered_df, path=["Region", "Category", "Sub-Category"], values="Sales", hover_data=["Sales"],
                          color="Sub-Category")
        fig3.update_layout(width=800, height=650)
        st.plotly_chart(fig3, use_container_width=True)

        # Segment and Category wise Sales
        chart1, chart2 = st.columns((2, 2))

        with chart1:
            st.subheader('Segment wise Sales')
            fig = px.pie(filtered_df, values="Sales", names="Segment", template="plotly_dark")
            fig.update_traces(text=filtered_df["Segment"], textposition="inside")
            st.plotly_chart(fig, use_container_width=True)

        with chart2:
            st.subheader('Category wise Sales')
            fig = px.pie(filtered_df, values="Sales", names="Category", template="gridon")
            fig.update_traces(text=filtered_df["Category"], textposition="inside")
            st.plotly_chart(fig, use_container_width=True)

        # Summary table and scatter plot
        import plotly.figure_factory as ff

        st.subheader(":point_right: Month wise Sub-Category Sales Summary")
        with st.expander("Summary_Table"):
            df_sample = df[0:5][["Region", "State", "City", "Category", "Sales", "Profit", "Quantity"]]
            fig = ff.create_table(df_sample, colorscale="Cividis")
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("Month wise sub-Category Table")
            filtered_df["month"] = filtered_df["Order Date"].dt.month_name()
            sub_category_Year = pd.pivot_table(data=filtered_df, values="Sales", index=["Sub-Category"], columns="month")
            st.write(sub_category_Year.style.background_gradient(cmap="Blues"))

        data1 = px.scatter(filtered_df, x="Sales", y="Profit", size="Quantity")
        data1['layout'].update(title="Relationship between Sales and Profits using Scatter Plot.",
                               titlefont=dict(size=20), xaxis=dict(title="Sales", titlefont=dict(size=19)),
                               yaxis=dict(title="Profit", titlefont=dict(size=19)))
        st.plotly_chart(data1, use_container_width=True)

        with st.expander("View Data"):
            st.write(filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges"))

        # Download original dataset
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button('Download Data', data=csv, file_name="Data.csv", mime="text/csv")

else:
    st.warning("Required columns (Order Date, Category, Sales, Profit, Quantity, Segment, Sub-Category) are missing.")
