import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict/"

st.title("Prediction App")

gender_mapping = {'Female': 0, 'Male': 1}
academic_performance_mapping = {'Average': 0, 'Below average': 1, 'Excellent': 2, 'Good': 3}
taking_notes_mapping = {'No': 0, 'Sometimes': 1, 'Yes': 2}
challenges_mapping = {'No': 0, 'Sometimes': 1, 'Yes': 2}
like_presentation_mapping = {'No': 0, 'Yes': 1}
like_new_things_mapping = {'No': 0, 'Yes': 1}

st.header("Enter your details:")

Age = st.number_input("Age", min_value=0.0, max_value=100.0, value=23.0)
SleepPerDayHours = st.number_input("Sleep Per Day (Hours)", min_value=0.0, max_value=24.0, value=8.0)
NumberOfFriend = st.number_input("Number of Friends", min_value=0.0, max_value=200.0, value=10.0)

Gender = st.radio("Gender", options=["Female", "Male"], index=1)
Gender = gender_mapping[Gender]

AcademicPerformance = st.selectbox("Academic Performance", options=["Average", "Below average", "Excellent", "Good"], index=0)
AcademicPerformance = academic_performance_mapping[AcademicPerformance]

TakingNoteInClass = st.selectbox("Taking Notes in Class", options=["No", "Sometimes", "Yes"], index=0)
TakingNoteInClass = taking_notes_mapping[TakingNoteInClass]

FaceChallangesToCompleteAcademicTask = st.selectbox("Face Challenges to Complete Academic Tasks", options=["No", "Sometimes", "Yes"], index=0)
FaceChallangesToCompleteAcademicTask = challenges_mapping[FaceChallangesToCompleteAcademicTask]

LikePresentation = st.radio("Likes Presentations", options=["No", "Yes"], index=1)
LikePresentation = like_presentation_mapping[LikePresentation]
LikeNewThings = st.radio("Likes New Things", options=["No", "Yes"], index=1)
LikeNewThings = like_new_things_mapping[LikeNewThings]

input_data = {
    "Age": Age,
    "SleepPerDayHours": SleepPerDayHours,
    "NumberOfFriend": NumberOfFriend,
    "Gender": Gender,
    "AcademicPerformance": AcademicPerformance,
    "TakingNoteInClass": TakingNoteInClass,
    "FaceChallangesToCompleteAcademicTask": FaceChallangesToCompleteAcademicTask,
    "LikePresentation": LikePresentation,
    "LikeNewThings": LikeNewThings
}

if st.button("Predict"):
    try:
        response = requests.post(API_URL, json=input_data)
        
        if response.status_code == 200:
            result = response.json()
            st.write(f"Prediction: {result['prediction']}")
        else:
            st.error("Error in prediction request.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
