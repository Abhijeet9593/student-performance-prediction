import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Page configuration for a professional look
st.set_page_config(
    page_title="Academic Performance AI",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    .prediction-box {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Load the model
@st.cache_resource
def load_model():
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

model = load_model()

# Header Section
st.markdown("<h1 style='text-align: center; color: #1e3d59;'>🎓 Student Success Analytics</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>Predict academic outcomes using Machine Learning</p>", unsafe_allow_html=True)
st.divider()

# Input Form
with st.container():
    st.subheader("📊 Student Profile Information")
    
    # Organize inputs into three clean columns
    col1, col2, col3 = st.columns(3)

    with col1:
        gender = st.selectbox("Gender", ["No", "Yes"], help="Is the student Male (Yes) or Female (No)?") [cite: 1]
        age = st.number_input("Age", min_value=10, max_value=100, value=20) [cite: 1]
        parent_edu = st.selectbox("Parent Education Level", [0, 1, 2, 3], help="Higher values indicate higher education levels.") [cite: 1]

    with col2:
        attendance = st.slider("Attendance Rate (%)", 0, 100, 85) [cite: 1]
        study_hours = st.number_input("Weekly Study Hours", min_value=0, max_value=168, value=15) [cite: 1]
        internet = st.selectbox("Has Internet Access?", ["No", "Yes"]) [cite: 1]

    with col3:
        extracurricular = st.selectbox("Extracurricular Activities", ["No", "Yes"]) [cite: 1]
        prev_score = st.number_input("Previous Grade Score", min_value=0, max_value=100, value=70) [cite: 1]
        final_score = st.number_input("Recent Exam Score", min_value=0, max_value=100, value=75) [cite: 1]

# Prediction Action
st.markdown("---")
if st.button("Generate Performance Analysis"):
    # Prepare data for prediction
    input_data = pd.DataFrame({
        'gender': [1 if gender == "Yes" else 0],
        'age': [age],
        'study_hours_per_week': [study_hours],
        'attendance_rate': [attendance],
        'parent_education': [parent_edu],
        'internet_access': [1 if internet == "Yes" else 0],
        'extracurricular': [1 if extracurricular == "Yes" else 0],
        'previous_score': [prev_score],
        'final_score': [final_score]
    }) [cite: 1]

    prediction = model.predict(input_data) [cite: 1]
    
    # Attractive Prediction Display
    st.subheader("🎯 Prediction Result")
    if prediction[0] == "Yes": [cite: 1]
        st.balloons()
        st.markdown("""<div class='prediction-box' style='background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb;'>
                    🚀 The student is predicted to PASS successfully!</div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class='prediction-box' style='background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;'>
                    ⚠️ The student is at risk. Academic intervention suggested.</div>""", unsafe_allow_html=True)

# Footer
st.markdown("<br><hr><center>Developed for AI/ML Portfolio | Pune, Maharashtra</center>", unsafe_allow_html=True)
