import streamlit as st
import time
import pandas as pd
import plotly.express as px
import random
from database import insert_data, fetch_yt_video, get_table_download_link, connection, cursor

def run():
    st.title("Resume and Interview Preparation")

    # User Side
    resume_data = st.session_state.get('resume_data', {})
    resume_score = st.session_state.get('resume_score', 0)
    resume_videos = ['url1', 'url2', 'url3']  # Replace with actual video URLs
    interview_videos = ['url1', 'url2', 'url3']  # Replace with actual video URLs

    if resume_data:
        st.subheader("**Resume Score📝**")

        # Progress bar for resume score
        st.markdown(
            """
            <style>
                .stProgress > div > div > div > div {
                    background-color: #d73b5c;
                }
            </style>""",
            unsafe_allow_html=True,
        )
        my_bar = st.progress(0)
        score = 0
        for percent_complete in range(resume_score):
            score += 1
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1)
        st.success(f'**Your Resume Writing Score: {score}**')
        st.warning("**Note: This score is calculated based on the content that you have added in your Resume.**")
        st.balloons()

        # Insert data into database
        insert_data(
            resume_data['name'], resume_data['email'], str(resume_score), resume_data['timestamp'],
            str(resume_data['no_of_pages']), resume_data['reco_field'], resume_data['cand_level'],
            str(resume_data['skills']), str(resume_data['recommended_skills']), str(resume_data['rec_course'])
        )

        # Resume writing video
        st.header("**Bonus Video for Resume Writing Tips💡**")
        resume_vid = random.choice(resume_videos)
        res_vid_title = fetch_yt_video(resume_vid)
        st.subheader(f"✅ **{res_vid_title}**")
        st.video(resume_vid)

        # Interview Preparation Video
        st.header("**Bonus Video for Interview👨‍💼 Tips💡**")
        interview_vid = random.choice(interview_videos)
        int_vid_title = fetch_yt_video(interview_vid)
        st.subheader(f"✅ **{int_vid_title}**")
        st.video(interview_vid)

        connection.commit()
    else:
        # Admin Side
        st.success('Welcome to Admin Side')
        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')

        if st.button('Login'):
            if ad_user == 'machine_learning_hub' and ad_password == 'mlhub123':
                st.success("Welcome Kushal")

                # Display Data
                cursor.execute('SELECT * FROM user_data')
                data = cursor.fetchall()
                st.header("**User's👨‍💻 Data**")
                df = pd.DataFrame(data, columns=[
                    'ID', 'Name', 'Email', 'Resume Score', 'Timestamp', 'Total Page',
                    'Predicted Field', 'User Level', 'Actual Skills', 'Recommended Skills', 'Recommended Course'
                ])
                st.dataframe(df)
                st.markdown(get_table_download_link(df, 'User_Data.csv', 'Download Report'), unsafe_allow_html=True)

                # Admin Side Data
                query = 'SELECT * FROM user_data'
                plot_data = pd.read_sql(query, connection)

                # Pie chart for predicted field recommendations
                labels = plot_data['Predicted_Field'].unique()
                values = plot_data['Predicted_Field'].value_counts()
                st.subheader("📈 **Pie-Chart for Predicted Field Recommendations**")
                fig = px.pie(plot_data, values=values, names=labels, title='Predicted Field according to the Skills')
                st.plotly_chart(fig)

                # Pie chart for User's Experienced Level
                labels = plot_data['User_Level'].unique()
                values = plot_data['User_Level'].value_counts()
                st.subheader("📈 **Pie-Chart for User's👨‍💻 Experienced Level**")
                fig = px.pie(plot_data, values=values, names=labels, title="Pie-Chart📈 for User's👨‍💻 Experienced Level")
                st.plotly_chart(fig)

            else:
                st.error("Wrong ID & Password Provided")

if __name__ == "__main__":
    run()
